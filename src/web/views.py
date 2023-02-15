from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, View, DetailView

from .models import Counter
from .forms import CreateUserForm, AddCounterForm


class CountersListView(ListView):
    template_name = "web/profile.html"
    model = Counter

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Counter.objects.none()
        queryset = Counter.objects.filter(user=self.request.user).order_by("-created_at")
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
            return redirect("profile")
        else:
            messages.info(request, "Неверный Логин или Пароль")

    context = {}
    return render(request, "web/auth.html", context)


class CounterCreate(CreateView):
    form_class = AddCounterForm
    template_name = "web/add_counter.html"
    success_url = "/profile"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super(CounterCreate, self).form_valid(form)


class CounterDetailView(DetailView):
    template_name = "web/counter.html"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Counter.objects.none()
        return Counter.objects.filter(user=self.request.user)


def main_page(request):
    return render(request, "web/main.html")


def edit_view(request, id):
    counter = get_object_or_404(Counter, user=request.user, id=id)
    form = AddCounterForm(instance=counter)
    if request.method == "POST":
        form = AddCounterForm(request.POST, instance=counter, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect("profile")
    return render(
        request,
        "web/edit_counter.html",
        {
            "form": form,
            "id": id,
        },
    )
