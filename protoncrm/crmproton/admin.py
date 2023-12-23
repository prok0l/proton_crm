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
                    "tg_id",
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
                'fields': ('is_admin', 'tg_id'),
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
                'fields': ('is_admin', 'tg_id'),
            }
        )
    )


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "customer", "location",
                    "creation_date", "building", "telephone", "time",
                    "photo_required")
    list_filter = ("id", "name")


@admin.register(TasksTime)
class TaskTimeAdmin(admin.ModelAdmin):
    list_display = ("task", "time", "creation_date", "from_user", "is_overdue",
                    "is_reminded", )
    list_filter = ("from_user", "is_overdue", "time", )


@admin.register(Levels)
class LevelsAdmin(admin.ModelAdmin):
    list_display = ("name", "picture")
    list_filter = ("name", )


@admin.register(TasksLevels)
class TasksLevelsAdmin(admin.ModelAdmin):
    list_display = ("task", "level", "creation_date", "from_user")
    list_filter = ("task", )


@admin.register(States)
class StatesAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_start", "is_end", )
    list_filter = ("name", "code", "is_start", "is_end", )


@admin.register(TasksStates)
class TasksStatesAdmin(admin.ModelAdmin):
    list_display = ("task", "state", "creation_date", "from_user", "photo")
    list_filter = ("task", )


@admin.register(TasksUsers)
class TasksUsersAdmin(admin.ModelAdmin):
    list_display = ("task", "user", "is_active", "creation_date", "from_user")
    list_filter = ("task", "user", "is_active")


@admin.register(Buildings)
class BuildingsAdmin(admin.ModelAdmin):
    list_display = ('address', 'short_name', )
    list_filter = ('address', 'short_name',)


@admin.register(BuildingsUsers)
class BuildingsUsersAdmin(admin.ModelAdmin):
    list_display = ('building', 'user', )
    list_filter = ('building', 'user', )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
