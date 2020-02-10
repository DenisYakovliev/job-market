from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from django.contrib.auth.views import LogoutView, LoginView, FormView
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator

from .models import User
from .forms import *
from market.utils import *


class EmployeeRegisterView(View):
    def get(self, request):
        form = EmployeeRegisterForm()
        return render(request, 'accounts/employee/register.html', context={'form': form})

    def post(self, request):
        bound_form = EmployeeRegisterForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()

            email = bound_form.cleaned_data['email']
            password = bound_form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home_page_url')
        return render(request, 'accounts/employee/register.html', context={'form': bound_form})


class EmployerRegisterView(View):
    def get(self, request):
        form = EmployerRegisterForm()
        return render(request, 'accounts/employer/register.html', context={'form': form})

    def post(self, request):
        bound_form = EmployerRegisterForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()

            email = bound_form.cleaned_data['email']
            password = bound_form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home_page_url')
        return render(request, 'accounts/employer/register.html', context={'form': bound_form})


class UserLoginView(FormView):
    form_class = UserLoginForm
    success_url = 'home_page_url'
    template_name = 'accounts/login.html'

    extra_context = {
        'title': 'Вход'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home_page_url')


class ProfileDetailView(View):
    model = User
    template = 'accounts/user_detail.html'

    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    def get(self, request, id):
        obj = get_object_or_404(self.model, id=id)
        if obj.role == 'admin' and not request.user.role == 'admin':
            raise PermissionDenied
        return render(request, self.template, context={'user': obj})


class ProfileJobsPanelView(View):
    template = 'accounts/user_jobs_panel.html'

    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    @method_decorator(user_is_employer)
    def get(self, request):
        jobs = Job.objects.filter(user_id=self.request.user.id)

        paginator = Paginator(jobs, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''

        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''

        context = {
            'page_object': page,
            'is_paginated': is_paginated,
            'prev_url': prev_url,
            'next_url': next_url,
        }

        return render(request, self.template, context=context)

    def post(self, request):
        pass

