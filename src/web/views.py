from django.urls import reverse
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    View,
    DetailView,
    UpdateView,
    TemplateView,
)
from .models import Counter
from .forms import CreateUserForm, AddCounterForm, AuthForm
from .services import (
    get_user_list_of_counters,
    add_parameters_into_counters,
)


class CountersListView(ListView, LoginRequiredMixin):
    template_name = "web/counters_list.html"

    def get_queryset(self):
        self.search = self.request.GET.get("search", None)
        queryset = get_user_list_of_counters(self.request.user)
        add_parameters_into_counters(queryset)
        if self.search:
            queryset = queryset.filter(name__icontains=self.search)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        return super(CountersListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
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
            messages.success(request, "Вы успешно зарегистрировались")
            return redirect("auth")
        context = {"form": form}
        return render(request, "web/registration.html", context)


def auth_page(request):
    form = AuthForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("counters")
            else:
                messages.error(request, "Неверный Логин или Пароль !")
        else:
            messages.error(request, "Некорректные данные !")
    return render(request, "web/auth.html", context={"form": form})


class CounterCreate(CreateView):
    form_class = AddCounterForm
    template_name = "web/add_counter.html"
    success_url = reverse_lazy("add")
    info_sended = True

    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(CounterCreate, self).form_valid(form)
        data = {
            "id": self.object.id,
        }
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        ctx = super(CounterCreate, self).get_context_data(**kwargs)
        return ctx


class CounterDetailView(DetailView):
    template_name = "web/counter.html"

    def get_queryset(self):
        return get_user_list_of_counters(self.request.user)


class MainView(TemplateView):
    template_name = "web/main.html"


class CounterEditView(UpdateView):
    template_name = "web/edit_counter.html"
    slug_field = "id"
    slug_url_kwarg = "id"
    form_class = AddCounterForm

    def get_queryset(self):
        return get_user_list_of_counters(self.request.user)

    def get_success_url(self):
        return reverse("counters")

    def get_context_data(self, *, object_list=None, **kwargs):
        return {**super(CounterEditView, self).get_context_data(**kwargs)}


class CounterDeleteView(View):
    def get(self, request, pk):
        counter = get_object_or_404(Counter, pk=pk)
        if counter and counter.user == request.user:
            counter.delete()
            return redirect("counters")
        # TODO сделать ридерект на страницу ошибки
        return redirect("counters")
