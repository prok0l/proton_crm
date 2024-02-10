from datetime import datetime, timedelta

from crmproton.models import (TelegramIds, TasksTime, TasksUsers,
                              BuildingsUsers, CustomUser)

from asgiref.sync import sync_to_async


@sync_to_async
def check_user(tg_id: int):
    return bool(TelegramIds.objects.filter(tg_id=tg_id))


@sync_to_async
def tasktime_overduelist():
    links = list(TasksTime.objects.filter(time__lt=datetime.now(),
                                          is_overdue=False))
    return links


@sync_to_async
def tasktime_reminded(remind_time: int):
    links = list(TasksTime.objects.filter(time__gt=datetime.now(),
                                          time__lte=
                                          datetime.now() +
                                          timedelta(minutes=remind_time),
                                          is_overdue=False,
                                          is_reminded=False))
    return links


@sync_to_async
def get_info_about_overdue(link: TasksTime, is_overdue: bool = True):
    if is_overdue:
        link.is_overdue = True
    else:
        link.is_reminded = True
    link.save()
    building = link.task.building
    users = list(x.user.tg_id for x in TasksUsers.objects.filter(
        task=link.task, is_active=True, user__tg_id__isnull=False))
    if is_overdue:
        users += list(x.user.tg_id for x in BuildingsUsers.objects.filter(
            user__is_admin=True, user__tg_id__isnull=False, building=building
        ))
    return list(set(users))


@sync_to_async
def create_user(tg_id: int):
    TelegramIds(tg_id=tg_id).save()
    return None


@sync_to_async
def deeplink(username: str, tg_id: int):
    user = CustomUser.objects.filter(username=username)
    if not user:
        return False
    user[0].tg_id = tg_id
    user[0].save()
    return True
