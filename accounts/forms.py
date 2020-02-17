from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from .models import User


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Почта")
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Введите почту'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Введите пароль'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("Пользователь не существует либо введены неправильные данные!")
            if not self.user.check_password(password):
                raise forms.ValidationError("Пароли не совподают!")
            if not self.user.is_active:
                raise forms.ValidationError("Пользователь не активен!")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class EmployeeRegisterForm(forms.ModelForm):
    error_message = {
        'password_mismatch': "Пароли не совподают!",
    }

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(EmployeeRegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Имя"
        self.fields['last_name'].label = "Фамилия"
        self.fields['email'].label = "Почта"
        self.fields['about'].label = "Инофрмация о себе"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"

        self.fields['about'].widget = forms.Textarea()

        self.fields['first_name'].widget.attrs.update({
                'placeholder': 'Введите Имя',
                'class': 'form-control'
            })
        self.fields['last_name'].widget.attrs.update({
                'placeholder': 'Введите Фамилию',
                'class': 'form-control'
            })
        self.fields['email'].widget.attrs.update({
                'placeholder': 'Введите Почту',
                'class': 'form-control'
            })
        self.fields['about'].widget.attrs.update({
                'placeholder': 'Введите информацию о себе',
                'class': 'form-control'
            })
        self.fields['password1'].widget.attrs.update({
                'placeholder': 'Введите Пароль',
                'class': 'form-control'
            })
        self.fields['password2'].widget.attrs.update({
                'placeholder': 'Подтвердите Пароль',
                'class': 'form-control'
            })

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'about', 'password1', 'password2']

        error_messages = {
            'first_name': {
                'required': 'Указание имени обязательно!',
                'max_length': 'Слишко длинное имя!'
            },
            'last_name': {
                'required': 'Указание фамилии обязательно!',
                'max_length': 'Фимилия слишком длинная!'
            },
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_message['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(EmployeeRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.role = "employee"
        if commit:
            user.save()
        return user


class EmployerRegisterForm(forms.ModelForm):
    error_message = {
        'password_mismatch': "Пароли не совподают!",
    }

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(EmployerRegisterForm, self).__init__(*args, **kwargs)
        self.fields['company_name'].label = "Назвавание Компании"
        self.fields['company_address'].label = "Адрес Компании"
        self.fields['email'].label = "Почта"
        self.fields['about'].label = "Информация о компании"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"

        self.fields['about'].widget = forms.Textarea()

        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Введите Назвавание Компании',
                'class': 'form-control'
            })
        self.fields['company_address'].widget.attrs.update(
            {
                'placeholder': 'Введите Адрес Компании',
                'class': 'form-control'
            })
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Введите Почту',
                'class': 'form-control'
            })
        self.fields['about'].widget.attrs.update({
            'placeholder': 'Введите информацию о компании',
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Введите Пароль',
                'class': 'form-control'
            })
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Подтвердите Пароль',
                'class': 'form-control'
            })

    class Meta:
        model = User
        fields = ['email', 'company_name', 'company_address', 'about', 'password1', 'password2']
        error_messages = {
            'first_name': {
                'required': 'Название компании обязательно!',
                'max_length': 'Название компании слишком длинное'
            },
            'last_name': {
                'required': 'Адрес компании обязателен!',
                'max_length': 'Адрес компании слишком длинный'
            }
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_message['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(EmployerRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.role = "employer"
        if commit:
            user.save()
        return user


class EmployeeUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Имя"
        self.fields['last_name'].label = "Фамилия"
        self.fields['about'].label = "Инофрмация о себе"

        self.fields['about'].widget = forms.Textarea()

        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Введите Имя',
            'class': 'form-control'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Введите Фамилию',
            'class': 'form-control'
        })
        self.fields['about'].widget.attrs.update({
            'placeholder': 'Введите информацию о себе',
            'class': 'form-control'
        })

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'about']


class EmployerUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployerUpdateForm, self).__init__(*args, **kwargs)
        self.fields['company_name'].label = "Назвавание Компании"
        self.fields['company_address'].label = "Адрес Компании"
        self.fields['about'].label = "Информация о компании"

        self.fields['about'].widget = forms.Textarea()

        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Введите Назвавание Компании',
                'class': 'form-control'
            })
        self.fields['company_address'].widget.attrs.update(
            {
                'placeholder': 'Введите Адрес Компании',
                'class': 'form-control'
            })
        self.fields['about'].widget.attrs.update({
            'placeholder': 'Введите информацию о компании',
            'class': 'form-control'
        })

    class Meta:
        model = User
        fields = ['company_name', 'company_address', 'about']
