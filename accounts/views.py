from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import get_user_model, login
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView

from .forms import MyUserCreationForm, CustomPasswordChangeForm

from .models import User


class CustomLoginView(LoginView):
    template_name = 'accounts/sign-in.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super(CustomLoginView, self).dispatch(request, *args, **kwargs)


class CustomRegisterView(FormView):
    template_name = 'accounts/sign-up.html'
    form_class = MyUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(CustomRegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('dashboard')
        return super(CustomRegisterView, self).get(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super(CustomRegisterView, self).dispatch(request, *args, **kwargs)


class UserDetail(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile_detail.html'
    model = User
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(UserDetail, self).dispatch(request, *args, **kwargs)


class UserUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile_update.html'
    model = User
    fields = ['description', 'avatar', 'bio', 'city', 'phoneNumber', 'first_name', 'last_name']
    context_object_name = 'profile'
    success_url = reverse_lazy('profile-detail')

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy('profile-detail')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(UserUpdate, self).dispatch(request, *args, **kwargs)


class UserInfo(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile_info.html'
    model = User
    context_object_name = 'profile'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(UserInfo, self).dispatch(request, *args, **kwargs)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/change_password.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('profile-detail')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(CustomPasswordChangeView, self).dispatch(request, *args, **kwargs)


class EmailChangeView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/change_email.html'
    model = User
    context_object_name = 'profile'
    fields = ['email']
    success_url = reverse_lazy('profile-detail')

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy('profile-detail')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(EmailChangeView, self).dispatch(request, *args, **kwargs)

