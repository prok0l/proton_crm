from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    AuthenticationForm
from django import forms

from .models import CustomUser, Tasks


class LoginUser(AuthenticationForm):
    username = forms.CharField(label="Логин", max_length=120, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser

        fields = ('name',
                  'username',
                  'is_admin',
        )

        add_fieldsets = (
            (
                None,
                {
                    'classes': ('wide',),
                    'fields': ('name', 'username', 'password1',
                               'password2'),
                },
            ),
            (
                'Additional info',
                {
                    'fields': ('is_admin', ),
                }
            )
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser

        fields = ('name',
                  'username',
                  'is_admin',
                  )

        add_fieldsets = (
            (
                None,
                {
                    'classes': ('wide',),
                    'fields': ('name', 'username', 'password1',
                               'password2'),
                },
            ),
            (
                'Additional info',
                {
                    'fields': ('is_admin',),
                }
            )
        )
