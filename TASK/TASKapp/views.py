from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.db.models import Q

# Create your views here.

def add_log(task, user, action):
    # log
    try:
        id = ActivityLog.objects.latest('id').id + 1
    except:
        id = 0
    ActivityLog.objects.create(id=id, task=task, user=user, action=action)

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # 保存新註冊的用戶
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # 註冊成功後重定向到登入頁面
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required 
def task(request):
    user = request.user
    tasks = Task.objects.filter(user_id=user)
    # 取得共享的任務
    sharedTasks = SharedTask.objects.filter(Q(user=user) | Q(task__user_id=user))
    # 排除共享任務後的我的任務
    my_tasks = tasks.exclude(id__in=sharedTasks.values_list('id', flat=True))

    # 為每個任務獲取留言
    for task in my_tasks:
        task.comments = Comment.objects.filter(task=task)

    return render(request, 'task.html',locals())

@login_required
def show_share(request):
    user = request.user
    tasks = Task.objects.filter(user_id=user)
    # 取得共享的任務
    sharedTasks = SharedTask.objects.filter(Q(user=user) | Q(task__user_id=user))
    # 排除共享任務後的我的任務
    my_tasks = tasks.exclude(id__in=sharedTasks.values_list('id', flat=True))

    show_share = {}
    for shared_task in sharedTasks:
        # 找到所有共享紀錄
        related_shared_tasks = SharedTask.objects.filter(task=shared_task.task)
        
        # 確保任務不會重複
        if shared_task.task.id not in show_share:
            # 初始化共享任務表
            show_share[shared_task.task.id] = {
                'task': shared_task.task,  # 任務對象
                'shared_users': []  # 共享使用者
            }
        
        # 將使用者加入到對應的陣列中
        for related_task in related_shared_tasks:
            show_share[shared_task.task.id]['shared_users'].append(related_task.user)
        show_share[shared_task.task.id]['shared_users'].append(shared_task.task.user_id)

    # 查詢每個共享任務的留言
        show_share[shared_task.task.id]['comments'] = Comment.objects.filter(task=shared_task.task)

    return render(request, 'show_share.html',locals())

@login_required
def add_task(request):
    user = request.user
    tasks = Task.objects.filter(user_id=user)
    # 取得共享的任務
    sharedTasks = SharedTask.objects.filter(Q(user=user) | Q(task__user_id=user))
    # 排除共享任務後的我的任務
    my_tasks = tasks.exclude(id__in=sharedTasks.values_list('id', flat=True))

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                id = Task.objects.latest('id').id + 1
            except:
                id = 0
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            due_date = form.cleaned_data['due_date']
            priority = form.cleaned_data['priority']
            status = form.cleaned_data['status']
            user_id = request.user  
            task = Task(
                id = id,
                title = title,
                description = description,
                due_date = due_date,
                priority = priority,
                status = status,
                user_id = user_id
            )
            task.save()  # 保存
            messages.success(request, '任務已新增！')
            add_log(task, user, "新增")
            return redirect('task')  # 重定向到任務列表頁面
    else:
        form = TaskForm()
    return render(request, 'add_task.html', locals())


@login_required
def edit_task(request, id):
    user = request.user
    tasks = Task.objects.filter(user_id=user)
    # 取得共享的任務
    sharedTasks = SharedTask.objects.filter(Q(user=user) | Q(task__user_id=user))
    # 排除共享任務後的我的任務
    my_tasks = tasks.exclude(id__in=sharedTasks.values_list('id', flat=True))

    previous_url = request.META.get('HTTP_REFERER')

    task = Task.objects.get(id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)  # 使用 instance 參數
        if form.is_valid():
            form.save()  # 保存表單
            messages.success(request, '任務已更新！')
            add_log(task, user, "更新")
            return redirect('task')  # 重定向到任務列表頁面
    else:
        form = TaskForm(instance=task)  # 預填充表單內容
    action = "編輯"

    return render(request, 'edit_task.html', locals())


@login_required
def share_task(request,id):
    user = request.user
    tasks = Task.objects.filter(user_id=user)
    # 取得共享的任務
    sharedTasks = SharedTask.objects.filter(Q(user=user) | Q(task__user_id=user))
    print(share_task)
    # 排除共享任務後的我的任務
    my_tasks = tasks.exclude(id__in=sharedTasks.values_list('id', flat=True))

    task = Task.objects.get(id=id)
    if request.method == 'POST':
        form = ShareForm(request.POST)  
        if form.is_valid():
            try:
                user_name = form.cleaned_data['user'].strip()
                username = User.objects.get(username=user_name)

                # 检查是否已存在相同的共享任务
                existing_shared_task = SharedTask.objects.filter(task=task, user=username).first()
                if existing_shared_task or user==username:
                    error_message = "該使用者已經共享此任務"
                    return render(request, 'edit_task.html', locals())

                try:
                    share_id = SharedTask.objects.latest('id').id + 1
                except:
                    share_id = 0
                SharedTask.objects.create(id=share_id, task=task, user=username)
                add_log(task, user, f"{user.username}分享給{username.username}")
                return redirect('task')  # 重定向到任務列表頁面
            except Exception as e:
                error_message = "沒有該名使用者"
                return render(request, 'edit_task.html', locals())
    else:
        form = ShareForm()  
    action = "分享"

    return render(request, 'edit_task.html', locals())


@login_required
def comment_task(request, id):
    user = request.user
    tasks = Task.objects.filter(user_id=user)
    # 取得共享的任務
    sharedTasks = SharedTask.objects.filter(Q(user=user) | Q(task__user_id=user))
    print(share_task)
    # 排除共享任務後的我的任務
    my_tasks = tasks.exclude(id__in=sharedTasks.values_list('id', flat=True))
    task = Task.objects.get(id=id)

    previous_url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = CommentForm(request.POST)  
        if form.is_valid():
            comment = form.cleaned_data['comment']
            try:
                comment_id = Comment.objects.latest('id').id + 1
            except:
                comment_id = 0
            Comment.objects.create(id=comment_id, task=task, user=user, content=comment)
            return redirect('task')  # 重定向到任務列表頁面
    else:
        form = CommentForm()  
    action = "留言"

    return render(request, 'edit_task.html', locals())

@login_required
def delete_task(request, id):
    user = request.user
    tasks = Task.objects.filter(user_id=user)
    # 取得共享的任務
    sharedTasks = SharedTask.objects.filter(Q(user=user) | Q(task__user_id=user))
    # 排除共享任務後的我的任務
    my_tasks = tasks.exclude(id__in=sharedTasks.values_list('id', flat=True))

    previous_url = request.META.get('HTTP_REFERER')

    task = Task.objects.get(id=id)
    add_log(task, user, "刪除")
    task.delete()
    return redirect('task')

@login_required
def show_log(request, id):
    user = request.user
    tasks = Task.objects.filter(user_id=user)
    # 取得共享的任務
    sharedTasks = SharedTask.objects.filter(Q(user=user) | Q(task__user_id=user))
    # 排除共享任務後的我的任務
    my_tasks = tasks.exclude(id__in=sharedTasks.values_list('id', flat=True))

    task = Task.objects.get(id=id)
    history = ActivityLog.objects.filter(task=task)
    previous_url = request.META.get('HTTP_REFERER')
    return render(request, 'show_log.html', locals())