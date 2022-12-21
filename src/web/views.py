from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from .forms import CreateUserForm


def registration_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('auth')
        else:
            messages.error(request, 'Ошибка регистрации')
    context = {'form': form}
    return render(request, 'web/registration.html', context)


def auth_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('login') ##TODO redict на личный кабинет
        else:
            messages.info(request, 'Неверный Логин или Пароль')

    context = {}
    return render(request, 'web/auth.html', context)
