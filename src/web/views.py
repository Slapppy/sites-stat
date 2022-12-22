from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from .forms import CreateUserForm
from .forms import AddCounterForm


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
            return redirect("/add")  ##TODO redict на личный кабинет
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
