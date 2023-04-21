from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    CreateView,
    View,
    DetailView,
    UpdateView,
    TemplateView,
)
from .forms import CreateUserForm, AddCounterForm
from .services import (
    get_user_list_of_counters,
    add_parameters_into_counters,
    filter_counters_with_search,
    get_user_counter,
)


class CountersListView(ListView, LoginRequiredMixin):
    template_name = "web/profile.html"

    def get_queryset(self):
        self.search = self.request.GET.get("search", None)
        queryset = get_user_list_of_counters(self.request.user)
        add_parameters_into_counters(queryset)
        if self.search:
            queryset = filter_counters_with_search(queryset, self.search)
        return queryset

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
        if request.user.is_authenticated:
            return redirect("main")
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
    if request.user.is_authenticated:
        return redirect("main")

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
    success_url = reverse_lazy("add")
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
        return {
            **super(CounterEditView, self).get_context_data(**kwargs),
            "id_counter": self.kwargs[self.slug_url_kwarg],
        }


class CounterDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        obj = get_user_counter(pk, request.user)
        if obj:
            obj.delete()
            return redirect("counters")
        """TODO сделать ридерект на страницу ошибки"""
        return redirect("counters")
