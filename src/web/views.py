from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import ListView

from .models import Counter
from .forms import CreateUserForm


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


def registration_page(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались")
            return redirect("auth")
        else:
            messages.error(request, "Ошибка регистрации")
    context = {"form": form}
    return render(request, "web/registration.html", context)


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


def main_page(request):
    return render(request, "web/main.html")
