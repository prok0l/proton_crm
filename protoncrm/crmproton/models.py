from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=120, unique=True)
    name = models.CharField(max_length=240)

    is_admin = models.BooleanField(default=False)
    tg_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
            return self.username

    class Meta:
        verbose_name_plural = "Пользователи"


class Buildings(models.Model):
    address = models.CharField(max_length=2400)
    short_name = models.CharField(max_length=240)

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name_plural = "Здания"


class Tasks(models.Model):
    name = models.CharField(max_length=2400)
    files = models.ImageField(blank=True)
    customer = models.CharField(max_length=240)
    telephone = models.CharField(max_length=240, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    building = models.ForeignKey(Buildings, on_delete=models.CASCADE)
    location = models.CharField(max_length=240)
    creation_date = models.DateTimeField(auto_now=True)
    photo_required = models.BooleanField(default=False)

    @property
    def get_time(self):
        if self.time:
            return self.time.strftime('%Y-%m-%d %H:%M')
        else:
            return "Не указано"

    class Meta:
        verbose_name_plural = "Задачи"

    def __str__(self):
        return f"{self.name} " \
               f"{self.creation_date.strftime('%Y-%m-%d %H:%M:%S')}"


class TasksTime(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, null=False)
    creation_date = models.DateTimeField(auto_now=True)
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                  null=True)
    is_overdue = models.BooleanField(default=False)
    is_reminded = models.BooleanField(default=False)
    time = models.DateTimeField()

    @property
    def get_time(self):
        return self.time.strftime('%Y-%m-%d %H:%M')

    class Meta:
        verbose_name_plural = "Планируемое время"


class Levels(models.Model):
    name = models.CharField(max_length=240)
    picture = models.ImageField(blank=True, upload_to="levels",
                                verbose_name="Изображение")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Срочность"


class TasksLevels(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, null=False)
    level = models.ForeignKey(Levels, on_delete=models.CASCADE, null=False)
    creation_date = models.DateTimeField(auto_now=True)
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                  null=True)

    class Meta:
        verbose_name_plural = "Срочность задач"


class States(models.Model):
    name = models.CharField(max_length=240)
    code = models.CharField(max_length=240, default="")
    is_start = models.BooleanField(default=False)
    is_end = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Состояние"


class TasksStates(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, null=False)
    state = models.ForeignKey(States, on_delete=models.CASCADE, null=False)
    creation_date = models.DateTimeField(auto_now=True)
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                  null=True)
    photo = models.ImageField(blank=True)

    class Meta:
        verbose_name_plural = "Состояния задач"


class TasksUsers(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False,
                             related_name='user')
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now=True)
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                  null=True,
                                  related_name='from_user')

    class Meta:
        verbose_name_plural = "Исполнители задач"


class BuildingsUsers(models.Model):
    building = models.ForeignKey(Buildings, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.building} - {self.user}"

    class Meta:
        verbose_name_plural = "Здания исполнителей"


class TelegramIds(models.Model):
    tg_id = models.IntegerField(unique=True)
