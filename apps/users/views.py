from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from rest_framework import generics
from .serializers import UserSerializer
from .forms import CustomUserCreationForm
from .models import CustomUser

@login_required
def home(request):
    if request.user.role == 'cliente':
        return redirect('catalog')
    else:
        return redirect('inventory:product_list')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso.')
            return redirect('catalog')  # or home
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        if 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Contraseña cambiada exitosamente.')
                return redirect('profile')
        elif request.user.role == 'admin':
            # Handle role updates for admin
            user_id = request.POST.get('user_id')
            new_role = request.POST.get('role')
            if user_id and new_role:
                try:
                    user = CustomUser.objects.get(id=user_id)
                    user.role = new_role
                    user.save()
                    messages.success(request, f'Rol de {user.username} actualizado a {new_role}.')
                except CustomUser.DoesNotExist:
                    messages.error(request, 'Usuario no encontrado.')
            return redirect('profile')

    users = CustomUser.objects.all() if request.user.role == 'admin' else None
    return render(request, 'users/profile.html', {'users': users, 'password_form': password_form})

class UserRegistrationView(generics.CreateAPIView):
    queryset = UserSerializer.Meta.model.objects.all()
    serializer_class = UserSerializer
