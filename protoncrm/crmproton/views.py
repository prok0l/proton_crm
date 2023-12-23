from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from crmproton.forms import LoginUser

from crmproton.models import *
from django.conf import settings

from services.taskinfo import TaskInfoStart


def page404(request, _exception):
    return HttpResponseNotFound(render(request, 'err404.html'))


def login(request):
    form = LoginUser(request.POST)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            print(f'User \'{username}\' logged in now.')
            return redirect('/')
        else:
            # messages.error(request, 'Ошибка: не верный логин или пароль')
            messages.error(request, "Неверный логин или пароль!")
            return redirect('/login/')
    return render(request, 'login.html', {'form': form})


def index(request):
    if request.method == 'POST':
        name = request.POST.get('text')
        customer = request.POST.get('customer')
        location = request.POST.get('location')
        telephone = request.POST.get('telephone')
        level = request.POST.get('level')
        building = Buildings.objects.get(
            short_name=request.POST.get('building'))
        time = request.POST.get('time')
        task = Tasks(name=name, customer=customer,
                     location=location, building=building,
                     telephone=telephone, time=time)
        if len(request.FILES) == 0:
            pass
        else:
            _, file = request.FILES.popitem()
            file = file[0]
            task.files = file
        task.save()
        link = TasksLevels(task=task, level=Levels.objects.get(name=level))
        link.save()
        link = TasksStates(task=task, state=States.objects.get(is_start=True))
        link.save()
        return redirect(info, task.id)

    return render(request, 'index.html',
                  {'levels': Levels.objects.all(),
                   'buildings': Buildings.objects.all()})


def info(request, task_id):
    task = Tasks.objects.filter(id=task_id)
    if not task:
        return render(request, 'info_not_found.html')
    task = task[0]
    obj = TaskInfoStart(task=task).generate_obj()
    return render(request, 'info.html', {'MEDIA_URL': settings.MEDIA_URL,
                                         'task_info': obj})


@login_required
def task_list(request, state_n=None):
    user = auth.get_user(request)
    buildings = [x.building for x in BuildingsUsers.objects.filter(user=user)]

    if not state_n:
        state_n = States.objects.filter(is_start=True)
        if not state_n:
            return render(request, 'info_not_found.html')
        state_n = state_n[0].code
    state = States.objects.filter(code=state_n)

    if not state:
        return render(request, 'info_not_found.html')

    state = state[0]
    states = States.objects.all()

    if user.is_admin:
        tasks = [x.task for x in TasksStates.objects.filter(
            state=state, task__building__in=buildings)]
    else:
        tasks = [x.task for x in TasksUsers.objects.filter(user=request.user,
                                                           is_active=True)]
    tasks = set(x for x in tasks if (link := list(TasksStates.objects
                                                  .filter(task=x)))
                and link[-1].state == state)
    return render(request, 'task_list.html', {'tasks': tasks,
                                              'states': states,
                                              'state': state.name})


@login_required
def task_settings(request, task_id):
    user = auth.get_user(request)
    buildings = [x.building for x in BuildingsUsers.objects.filter(user=user)]
    task = Tasks.objects.filter(id=task_id)
    if not task:
        return render(request, 'info_not_found.html')
    task = task[0]
    if task.building not in buildings:
        return redirect(f'/info/{task_id}')

    if request.method == "GET":
        obj = TaskInfoStart(task=task).generate_obj()
        states = list(States.objects.all())
        levels = list(Levels.objects.all())
        workers = list(x.user for x in BuildingsUsers.objects.filter(
            building=task.building, user__is_admin=False))
        return render(request, 'task_settings.html',
                      {'MEDIA_URL': settings.MEDIA_URL,
                       'task_info': obj,
                       'states': states,
                       'levels': levels,
                       'workers': workers})

    else:
        data = dict(request.POST)

        if data.get('state'):
            state = States.objects.get(name=data.get('state')[-1])
            if len(request.FILES) == 0:
                file = None
            else:
                _, file = request.FILES.popitem()
                file = file[0]
            TasksStates(task=task, state=state, from_user=user,
                        photo=file).save()

        if user.is_admin:
            if data.get('photo_required'):
                if data.get('photo_required') == ['on']:
                    task.photo_required = True
                else:
                    task.photo_required = False
                task.save()

            if data.get('date'):
                link = list(TasksTime.objects.filter(task=task))
                new_date = data.get('date')[0]
                if new_date and (not link or link[-1].get_time
                                 != new_date):
                    if link:
                        link_obj = link[-1]
                        if link_obj:
                            link_obj.is_overdue = True
                            link_obj.save()
                    TasksTime(task=task,
                              time=datetime.strptime(new_date,
                                                     '%Y-%m-%dT%H:%M'),
                              from_user=user).save()

            if data.get('level'):
                level = Levels.objects.get(name=data.get('level')[-1])
                TasksLevels(task=task, level=level, from_user=user).save()
            workers = data.get('workers', [])
            workers_links = list(TasksUsers.objects.filter(task=task,
                                                           is_active=True))
            workers_now = [x.user for x in workers_links]
            workers_new = [CustomUser.objects.filter(id=int(x))
                           for x in workers]
            add_worker = [x for x in workers_new if x not in workers_now]
            del_worker = [x for x in workers_links
                          if x.user not in workers_new]
            for x in add_worker:
                if x:
                    TasksUsers(task=task, user=x[0],
                               from_user=user).save()
            for x in del_worker:
                x.is_active = False
                x.from_user = request.user
                x.save()
        return redirect('task', task_id)


@login_required
def account(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "account.html",
                          {"user": request.user})
        else:
            tg_id = request.POST.get('tg_input')
            if tg_id:
                if not TelegramIds.objects.filter(tg_id=tg_id):
                    messages.warning(request, "Извините, но такой"
                                              " tg_id не найден")
                else:
                    user = CustomUser.objects.get(id=request.user.id)
                    user.tg_id = tg_id
                    user.save()
                    messages.success(request, "Telegram успешно"
                                              " привязан")
                return redirect('/account/')
            else:
                return redirect('/account/')
    else:
        return redirect('/login/')


@login_required
def change_password(request):
    if request.method == 'GET':
        return render(request, 'change_password.html')
    else:
        old_password, new_password, repeat_password = dict(request.POST)[
            'password']
        if new_password != repeat_password:
            messages.warning(request, 'Введенные пароли не совпадают!')
        else:
            user = request.user
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                auth.login(request, user)
                messages.success(request, 'Поменял!')
            else:
                messages.error(request, 'Хм, похоже пароль неверный')
        return redirect('/account/change_password/')
