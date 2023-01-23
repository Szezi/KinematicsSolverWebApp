from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView, ListView

from .models import Project, Robot


class DashboardView(ListView):
    template_name = "robot/dashboard.html"
    model = Robot
    context_object_name = 'robots'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_member'] = Project.objects.filter(members=self.request.user).count()
        context['project_admin'] = Project.objects.filter(admin=self.request.user).count()
        context['robot_last'] = Robot.objects.all().filter(owner=self.request.user).order_by('-created')[0:1]


        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(DashboardView, self).dispatch(request, *args, **kwargs)


class ProjectDetail(LoginRequiredMixin, DetailView):
    template_name = 'robot/project_detail.html'
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['robots'] = Robot.objects.filter(project=pk)
        context['robots_number'] = Robot.objects.filter(project=pk).count()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(ProjectDetail, self).dispatch(request, *args, **kwargs)


class ProjectCreate(LoginRequiredMixin, CreateView):
    template_name = 'robot/project_form.html'
    model = Project
    fields = ['name', 'description', 'admin', 'members']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProjectCreate, self).form_valid(form)

    def get_initial(self):
        return {'admin': self.request.user, 'members': self.request.user}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(ProjectCreate, self).dispatch(request, *args, **kwargs)


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'robot/project_update.html'
    model = Project
    fields = ['name', 'description', 'admin', 'members']
    context_object_name = 'project'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(ProjectUpdate, self).dispatch(request, *args, **kwargs)


class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(ProjectDelete, self).dispatch(request, *args, **kwargs)


class RobotDetail(LoginRequiredMixin, DetailView):
    template_name = 'robot/robot_detail.html'
    model = Robot
    context_object_name = 'robot'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(RobotDetail, self).dispatch(request, *args, **kwargs)


class RobotCreate(LoginRequiredMixin, CreateView):
    template_name = 'robot/robot_form.html'
    model = Robot
    fields = '__all__'
    success_url = reverse_lazy('dashboard')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)  # Get the form as usual
        user = self.request.user
        form.fields['project'].queryset = Project.objects.filter(members=user)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(RobotCreate, self).form_valid(form)

    def get_initial(self):
        return {'owner': self.request.user}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(RobotCreate, self).dispatch(request, *args, **kwargs)


class RobotUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'robot/robot_update.html'
    model = Robot
    fields = '__all__'
    context_object_name = 'robot'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(RobotUpdate, self).dispatch(request, *args, **kwargs)


class RobotDelete(LoginRequiredMixin, DeleteView):
    model = Robot
    context_object_name = 'robot'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(RobotDelete, self).dispatch(request, *args, **kwargs)