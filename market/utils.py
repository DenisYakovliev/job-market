from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy

from .models import *


def user_is_employer(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 'employer' or user.role == 'admin':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def user_is_employee(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 'employee' or user.role == 'admin':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


class DetailMixin:
    model = None
    template = None

    def get(self, request, job_id):
        obj = get_object_or_404(self.model, id=job_id)
        return render(request, self.template, context={self.model.__name__.lower(): obj})


class ObjectCreateMixin:
    model = None
    template = None

    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    @method_decorator(user_is_employer)
    def get(self, request):
        form = self.model()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.model(request.POST, request.FILES)

        if bound_form.is_valid():
            new_object = bound_form.save(commit=False)
            new_object.user = request.user
            new_object.save()
            return redirect(new_object)
        return render(request, self.template, context={'form': bound_form})


class ObjectUpdateMixin:
    model = None
    template = None
    model_form = None

    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    @method_decorator(user_is_employer)
    def get(self, request, id):
        obj = self.model.objects.get(id=id)
        bound_form = self.model_form(instance=obj)
        context = {'form': bound_form, self.model.__name__.lower(): obj}
        return render(request, self.template, context=context)

    def post(self, request, id):
        obj = self.model.objects.get(id=id)
        bound_form = self.model_form(request.POST, instance=obj)

        if bound_form.is_valid():
            new_object = bound_form.save()
            return redirect(new_object)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    @method_decorator(login_required(login_url=reverse_lazy('login_url')))
    @method_decorator(user_is_employer)
    def get(self, request, id):
        obj = self.model.objects.get(id=id)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, id):
        obj = self.model.objects.get(id=id)
        obj.delete()
        return redirect(reverse(self.redirect_url))
