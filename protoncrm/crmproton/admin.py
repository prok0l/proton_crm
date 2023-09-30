from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
                    "id",
                    "name",
                    "username",
                    "is_admin",
                    )
    list_filter = (
        "is_admin",
    )
    search_fields = (
        "id",
        "name",
        "username",
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('name', 'username', 'password1', 'password2'),
            },
        ),
        (
            'Additional info',
            {
                'fields': ('is_admin',),
            }
        )
    )

    fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('name', 'username', 'password'),
            },
        ),
        (
            'Additional info',
            {
                'fields': ('is_admin', ),
            }
        )
    )


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "files", "customer", "location",
                    "creation_date")
    list_filter = ("id", "name")


@admin.register(TasksTime)
class TaskTimeAdmin(admin.ModelAdmin):
    list_display = ("task", "time", "creation_date")
    list_filter = ("task", )


@admin.register(Levels)
class LevelsAdmin(admin.ModelAdmin):
    list_display = ("name", "picture")
    list_filter = ("name", )


@admin.register(TasksLevels)
class TasksLevelsAdmin(admin.ModelAdmin):
    list_display = ("task", "level", "creation_date")
    list_filter = ("task", )


@admin.register(States)
class StatesAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_start", "is_end", )
    list_filter = ("name", "code", "is_start", "is_end", )


@admin.register(TasksStates)
class TasksStatesAdmin(admin.ModelAdmin):
    list_display = ("task", "state", "creation_date")
    list_filter = ("task", )


@admin.register(TasksUsers)
class TasksUsersAdmin(admin.ModelAdmin):
    list_display = ("task", "user", "is_active", "creation_date")
    list_filter = ("task", "user", "is_active")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
