import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from .models import Project, Robot, ForwardKinematics, InverseKinematics

from robot.robotic_arm import RoboticArm


class DashboardView(ListView):
    """
        Dashboard View with basic information about users projects stats.\n
        Displayed users stats: \
        -number of projects user is member of \n
        -number of calculated fk \n
        -number of calculated ik \n
        -number of projects user is admin of \n
        -parameters of last created robot \n
        Unauthenticated user is redirected to home page.
    """
    template_name = "robot/dashboard.html"
    model = Robot
    context_object_name = 'robots'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_member'] = Project.objects.filter(members=self.request.user).count()
        context['fk_calc'] = ForwardKinematics.objects.filter(modified_by=self.request.user).count()
        context['ik_calc'] = InverseKinematics.objects.filter(modified_by=self.request.user).count()
        context['project_admin'] = Project.objects.filter(admin=self.request.user).count()
        context['robot_last'] = Robot.objects.all().filter(owner=self.request.user).order_by('-created')[0:1]

        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(DashboardView, self).dispatch(request, *args, **kwargs)


class ProjectDetail(LoginRequiredMixin, DetailView):
    """
        Projects details view. \n
        Unauthenticated user is redirected to home page.
    """
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
    """
        Create new project. \n
        Field to be filled: name, description, admin, members. \n
        Logged user is add to admin and members as initial value. \n
        Unauthenticated user is redirected to home page.
    """
    template_name = 'robot/project_form.html'
    model = Project
    fields = ['name', 'description', 'admin', 'members']

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
    """
        Update project. \n
        Only projects admin can edit project. \n
        Fields to modify: name, description, admin, members. \n
        Unauthenticated user is redirected to home page.
    """
    template_name = 'robot/project_update.html'
    model = Project
    fields = ['name', 'description', 'admin', 'members']
    context_object_name = 'project'

    def get_queryset(self):
        base_qs = super(ProjectUpdate, self).get_queryset()
        return base_qs.filter(admin=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                return redirect('home')
            return super(ProjectUpdate, self).dispatch(request, *args, **kwargs)
        except Http404:
            return redirect('dashboard')


class ProjectDelete(LoginRequiredMixin, DeleteView):
    """
        Delete project. \n
        Only projects admin can delete project. \n
        Unauthenticated user is redirected to home page.
    """
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        base_qs = super(ProjectDelete, self).get_queryset()
        return base_qs.filter(admin=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                return redirect('home')
            return super(ProjectDelete, self).dispatch(request, *args, **kwargs)
        except Http404:
            return redirect('dashboard')


class RobotDetail(LoginRequiredMixin, DetailView):
    """
        Robotic arm details view. \n
        Unauthenticated user is redirected to home page.
    """
    template_name = 'robot/robot_detail.html'
    model = Robot
    context_object_name = 'robot'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['fk_kinematics'] = ForwardKinematics.objects.filter(Robot=pk)
        context['ik_kinematics'] = InverseKinematics.objects.filter(Robot=pk)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(RobotDetail, self).dispatch(request, *args, **kwargs)


class RobotCreate(LoginRequiredMixin, CreateView):
    """
        Create new robotic arm. \n
        Field to be filled: \n
        'project', 'name', 'description', 'notes', \n
        'link1', 'link2', 'link3', 'link4', 'link5', \n
        'link1_min', 'link2_min', 'link3_min', 'link4_min', 'link5_min', \n
        'link1_max', 'link2_max', 'link3_max', 'link4_max', 'link5_max' \n
        Logged user is add to owner field as initial value. \n
        Unauthenticated user is redirected to home page.
    """
    template_name = 'robot/robot_form.html'
    model = Robot
    fields = ['project', 'name', 'description', 'notes', 'link1', 'link2', 'link3', 'link4', 'link5', 'link1_min', 'link2_min', 'link3_min', 'link4_min', 'link5_min', 'link1_max', 'link2_max', 'link3_max', 'link4_max', 'link5_max']

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)  # Get the form as usual
        user = self.request.user
        form.fields['project'].queryset = Project.objects.filter(members=user)
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(RobotCreate, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(RobotCreate, self).dispatch(request, *args, **kwargs)


class RobotUpdate(LoginRequiredMixin, UpdateView):
    """
        Update robotic arm. \n
        Only projects member can edit robotic arm. \n
        Unauthenticated user is redirected to home page.
    """
    template_name = 'robot/robot_update.html'
    model = Robot
    fields = ['name', 'description', 'notes', 'link1', 'link2', 'link3', 'link4', 'link5', 'link1_min', 'link2_min', 'link3_min', 'link4_min', 'link5_min', 'link1_max', 'link2_max', 'link3_max', 'link4_max', 'link5_max']
    context_object_name = 'robot'

    def get_queryset(self):
        base_qs = super(RobotUpdate, self).get_queryset()
        return base_qs.filter(project__members=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                return redirect('home')
            return super(RobotUpdate, self).dispatch(request, *args, **kwargs)
        except Http404:
            return redirect('dashboard')


class RobotDelete(LoginRequiredMixin, DeleteView):
    """
        Delete robotic arm. \n
        Only projects member can delete robotic arm. \n
        Unauthenticated user is redirected to home page.
    """
    model = Robot
    context_object_name = 'robot'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        base_qs = super(RobotDelete, self).get_queryset()
        return base_qs.filter(project__members=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                return redirect('home')
            return super(RobotDelete, self).dispatch(request, *args, **kwargs)
        except Http404:
            return redirect('dashboard')


class FkCreate(LoginRequiredMixin, CreateView):
    """
        Create forward kinematics calculation record. \n
        Fields to modify: 'Robot', 'name', 'notes', 'theta1', 'theta2', 'theta3', 'theta4' \n
        Unauthenticated user is redirected to home page.
    """
    template_name = 'robot/fk_form.html'
    model = ForwardKinematics
    fields = ['Robot', 'name', 'notes', 'theta1', 'theta2', 'theta3', 'theta4']

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)  # Get the form as usual
        user = self.request.user
        form.fields['Robot'].queryset = Robot.objects.filter(project__members=user)
        return form

    def form_valid(self, form):
        form.instance.modified_by = self.request.user

        if form.is_valid():
            form.instance.modified = datetime.datetime.now()
            form.save()
        return super(FkCreate, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(FkCreate, self).dispatch(request, *args, **kwargs)


class FkUpdate(LoginRequiredMixin, UpdateView):
    """
        Display and update forward kinematics calculation. \n
        Fields to modify: 'notes', 'theta1', 'theta2', 'theta3', 'theta4' \n
        Unauthenticated user is redirected to home page.
    """
    template_name = 'robot/fk_update.html'
    model = ForwardKinematics
    fields = ['notes', 'theta1', 'theta2', 'theta3', 'theta4']
    context_object_name = 'fk'

    def get_context_data(self, **kwargs):
        context = super(FkUpdate, self).get_context_data(**kwargs)
        context['link1'] = self.get_object().Robot.link1
        context['link2'] = self.get_object().Robot.link2
        context['link3'] = self.get_object().Robot.link3
        context['link4'] = self.get_object().Robot.link4
        context['link5'] = self.get_object().Robot.link5
        context['link1_min'] = self.get_object().Robot.link1_min
        context['link2_min'] = self.get_object().Robot.link2_min
        context['link3_min'] = self.get_object().Robot.link3_min
        context['link4_min'] = self.get_object().Robot.link4_min
        context['link5_min'] = self.get_object().Robot.link5_min
        context['link1_max'] = self.get_object().Robot.link1_max
        context['link2_max'] = self.get_object().Robot.link2_max
        context['link3_max'] = self.get_object().Robot.link3_max
        context['link4_max'] = self.get_object().Robot.link4_max
        context['link5_max'] = self.get_object().Robot.link5_max

        return context

    def calculate_fk(self, theta1, theta2, theta3, theta4):
        """
            Calculate forward kinematics of robotic arm.
            :param theta1: theta1 value
            :param theta2: theta2 value
            :param theta3: theta3 value
            :param theta4: theta4 value
            :return: result_xyz, dh_table
        """
        context = self.get_context_data()
        links = {"link1": [context['link1'], context['link1_min'], context['link1_max']],
                 "link2": [context['link2'], context['link2_min'], context['link2_max']],
                 "link3": [context['link3'], context['link3_min'], context['link3_max']],
                 "link4": [context['link4'], context['link4_min'], context['link4_max']],
                 "link5": [context['link5'], context['link5_min'], context['link5_max']]}
        Robot_FK = RoboticArm(links)
        result_xyz = Robot_FK.fk_solve_auto(theta1, theta2, theta3, theta4)
        dh_table = Robot_FK.fk_dh(theta1, theta2, theta3, theta4)
        return result_xyz, dh_table

    def form_valid(self, form):
        form.instance.modified_by = self.request.user

        theta1 = form.instance.theta1
        theta2 = form.instance.theta2
        theta3 = form.instance.theta3
        theta4 = form.instance.theta4

        try:
            calculation = self.calculate_fk(theta1, theta2, theta3, theta4)
            x = calculation[0][1][0][0]
            y = calculation[0][1][1][1]
            z = calculation[0][1][2][2]
            alpha = calculation[0][0]

        except:
            x = 0
            y = 0
            z = 0
            alpha = 0
            print("form invalid")

        if form.is_valid():
            form.instance.x = x
            form.instance.y = y
            form.instance.z = z
            form.instance.alpha = alpha

            form.instance.modified = datetime.datetime.now()
            form.save()

        return super(FkUpdate, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(FkUpdate, self).dispatch(request, *args, **kwargs)


class IkCreate(LoginRequiredMixin, CreateView):
    """
        Create inverse kinematics calculation record. \n
        Fields to modify: 'Robot', 'name', 'notes', 'x', 'y', 'z', 'alpha' \n
        Unauthenticated user is redirected to home page.
    """
    template_name = 'robot/ik_form.html'
    model = InverseKinematics
    fields = ['Robot', 'name', 'notes', 'x', 'y', 'z', 'alpha']

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)  # Get the form as usual
        user = self.request.user
        form.fields['Robot'].queryset = Robot.objects.filter(project__members=user)
        return form

    def form_valid(self, form):
        form.instance.modified_by = self.request.user

        if form.is_valid():
            form.instance.modified = datetime.datetime.now()
            form.save()
        return super(IkCreate, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(IkCreate, self).dispatch(request, *args, **kwargs)


class IkUpdate(LoginRequiredMixin, UpdateView):
    """
        Display and update inverse kinematics calculation. \n
        Fields to modify: 'notes', 'x', 'y', 'z', 'alpha' \n
        Unauthenticated user is redirected to home page.
    """
    template_name = 'robot/ik_update.html'
    model = InverseKinematics
    fields = ['notes', 'x', 'y', 'z', 'alpha']
    context_object_name = 'ik'

    def get_context_data(self, **kwargs):
        context = super(IkUpdate, self).get_context_data(**kwargs)
        context['link1'] = self.get_object().Robot.link1
        context['link2'] = self.get_object().Robot.link2
        context['link3'] = self.get_object().Robot.link3
        context['link4'] = self.get_object().Robot.link4
        context['link5'] = self.get_object().Robot.link5
        context['link1_min'] = self.get_object().Robot.link1_min
        context['link2_min'] = self.get_object().Robot.link2_min
        context['link3_min'] = self.get_object().Robot.link3_min
        context['link4_min'] = self.get_object().Robot.link4_min
        context['link5_min'] = self.get_object().Robot.link5_min
        context['link1_max'] = self.get_object().Robot.link1_max
        context['link2_max'] = self.get_object().Robot.link2_max
        context['link3_max'] = self.get_object().Robot.link3_max
        context['link4_max'] = self.get_object().Robot.link4_max
        context['link5_max'] = self.get_object().Robot.link5_max

        return context

    def calculate_ik(self, x, y, z, alpha):
        """
            Calculate inverse kinematics of robotic arm.
            :param x: x values
            :param y: y value
            :param z: z value
            :param alpha: alpha value
            :return: config1, config2
            """
        context = self.get_context_data()
        links = {"link1": [context['link1'], context['link1_min'], context['link1_max']],
                 "link2": [context['link2'], context['link2_min'], context['link2_max']],
                 "link3": [context['link3'], context['link3_min'], context['link3_max']],
                 "link4": [context['link4'], context['link4_min'], context['link4_max']],
                 "link5": [context['link5'], context['link5_min'], context['link5_max']]}
        Robot_IK = RoboticArm(links)
        Robot_IK.ik_solver(x, y, z, alpha)
        config_1 = Robot_IK.ik_get_config1()
        config_2 = Robot_IK.ik_get_config2()
        return config_1, config_2

    def form_valid(self, form):
        form.instance.modified_by = self.request.user

        x = form.instance.x
        y = form.instance.y
        z = form.instance.z
        alpha = form.instance.alpha

        try:
            calculation = self.calculate_ik(x, y, z , alpha)
            theta1 = calculation[0][0][0]
            theta2 = calculation[0][0][1]
            theta3 = calculation[0][0][2]
            theta4 = calculation[0][0][3]
            theta11 = calculation[1][0][0]
            theta22 = calculation[1][0][1]
            theta33 = calculation[1][0][2]
            theta44 = calculation[1][0][3]
        except:
            theta1 = 0
            theta2 = 0
            theta3 = 0
            theta4 = 0
            theta11 = 0
            theta22 = 0
            theta33 = 0
            theta44 = 0
            print("form invalid")

        if form.is_valid():
            form.instance.theta1 = theta1
            form.instance.theta2 = theta2
            form.instance.theta3 = theta3
            form.instance.theta4 = theta4
            form.instance.theta11 = theta11
            form.instance.theta22 = theta22
            form.instance.theta33 = theta33
            form.instance.theta44 = theta44
            form.instance.modified = datetime.datetime.now()
            form.save()

        return super(IkUpdate, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super(IkUpdate, self).dispatch(request, *args, **kwargs)
