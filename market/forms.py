from django import forms

from .models import *


class JobForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Назвавание Вакансии"
        self.fields['description'].label = "Описание Вакансии"
        self.fields['salary'].label = "Оплата"
        self.fields['location'].label = "Место роботы"
        self.fields['type'].label = "Тип занятости"
        self.fields['category'].label = "Тип работы"
        # self.fields['last_date'].label = "Дата закрытия вакансии"
        self.fields['website'].label = "Сайт компании"

        self.fields['description'].widget = forms.Textarea()
        # self.fields['last_date'].input_formats = ["%d.%m.%Y"]

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'Введите назвавание должности',
                'class': 'form-control'
            })
        self.fields['description'].widget.attrs.update(
            {
                'placeholder': 'Введите описание Вакансии',
                'class': 'form-control'
            })
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': 'Укажите оплату',
                'class': 'form-control'
            })
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'Укажите адрес',
                'class': 'form-control'
            })
        self.fields['type'].widget.attrs.update(
            {
                'placeholder': 'Укажите вид занятости',
                'class': 'form-control'
            })
        self.fields['category'].widget.attrs.update(
            {
                'placeholder': 'Укажите тип работы',
                'class': 'form-control'
            })
        # self.fields['last_date'].widget.attrs.update(
        #     {
        #         # 'placeholder': 'Выберите дату закрытия',
        #         'class': 'form-control'
        #     })
        self.fields['website'].widget.attrs.update(
            {
                'placeholder': 'Введите сайт компании',
                'class': 'form-control'
            })

    class Meta:
        model = Job
        exclude = ['user', 'created_at', 'views', 'slug', 'filled', 'last_date', 'price']

    def is_valid(self):
        valid = super(JobForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        job = super(JobForm, self).save(commit=False)
        job.price = job.salary * 0.05

        if commit:
            job.save()
        return job


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ('job',)
