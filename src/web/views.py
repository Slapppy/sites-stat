from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    CreateView,
    View,
    DetailView,
    UpdateView,
    TemplateView,
)
from app.clickhouse import create_connection
from datetime import datetime

from .clickhouse_models import ViewInDay, VisitInDay, VisitorInDay
from .models import Counter
from .forms import CreateUserForm, AddCounterForm


class CountersListView(ListView, LoginRequiredMixin):
    template_name = "web/profile.html"
    model = Counter

    @staticmethod
    def get_data(model, field_name, counter_id, start_date, end_date):
        db = create_connection()
        queryset = (
            model.objects_in(db)
            .filter(created_at__between=(start_date, end_date), counter_id=counter_id)
            .aggregate("counter_id", sum_stat=f"sum({field_name})")
        )
        if queryset:
            queryset = queryset[0].sum_stat
            return queryset
        return 0

    def get_parameters(self, queryset):
        end_date = datetime.now().strftime("%Y-%m-%d")
        for query in queryset:
            start_date = query.created_at.strftime("%Y-%m-%d")
            query.count_views = self.get_data(ViewInDay, "count_views", query.id, start_date, end_date)
            query.count_visits = self.get_data(VisitInDay, "count_visits", query.id, start_date, end_date)
            query.count_visitors = self.get_data(VisitorInDay, "count_visitors", query.id, start_date, end_date)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Counter.objects.none()
        queryset = Counter.objects.filter(user=self.request.user).order_by("-created_at")
        self.get_parameters(queryset)
        return self.filter_queryset(queryset)

    def filter_queryset(self, counters):
        self.search = self.request.GET.get("search", None)

        if self.search:
            counters = counters.filter(name__icontains=self.search)
        return counters

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("auth")
        return super(CountersListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        if not self.request.user.is_authenticated:
            return {}
        return {
            **super(CountersListView, self).get_context_data(**kwargs),
            "search": self.search,
        }


class RegistrationView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, "web/registration.html", {"form": form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            storage = messages.get_messages(request)
            self.clear_messages(storage)
            messages.success(request, "Вы успешно зарегистрировались")
            return redirect("auth")
        else:
            storage = messages.get_messages(request)
            self.clear_messages(storage)
            messages.error(request, "Ошибка регистрации")
        context = {"form": form}
        return render(request, "web/registration.html", context)

    def clear_messages(self, storage):
        for _ in storage:
            pass
        if len(storage._loaded_messages) == 1:
            del storage._loaded_messages[0]


def auth_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("counters")
        else:
            messages.info(request, "Неверный Логин или Пароль")

    context = {}
    return render(request, "web/auth.html", context)


class CounterCreate(CreateView):
    form_class = AddCounterForm
    template_name = "web/add_counter.html"
    success_url = "/counters/add"
    info_sended = True

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            self.object = form.save()
            response_data = {"success": True, "counter": self.object.id}
            return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        ctx = super(CounterCreate, self).get_context_data(**kwargs)
        return ctx


class CounterDetailView(DetailView):
    template_name = "web/counter.html"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Counter.objects.none()
        return Counter.objects.filter(user=self.request.user)


class MainView(TemplateView):
    template_name = "web/main.html"


class CounterEditView(UpdateView):
    template_name = "web/edit_counter.html"
    slug_field = "id"
    slug_url_kwarg = "id"
    form_class = AddCounterForm

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Counter.objects.none()
        return Counter.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("counters")

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            **super(CounterEditView, self).get_context_data(**kwargs),
            "id_counter": self.kwargs[self.slug_url_kwarg],
        }


class CounterDeleteView(View):
    def get(self, request, pk):
        obj = get_object_or_404(Counter, pk=pk)
        if obj in Counter.objects.filter(user=request.user):
            obj.delete()
            return redirect("counters")
        else:
            """TODO сделать ридерект на страницу ошибки"""
            return redirect("counters")
