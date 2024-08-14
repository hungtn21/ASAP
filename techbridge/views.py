from django.contrib import messages  # メッセージフレームワークをインポート
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Group, GroupMember, GroupMessage, GroupThread


from django.shortcuts import render
from django.conf import settings
import requests


def prebase(request):
    return render(request, 'prebase.html')

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Điều hướng đến dashboard
        else:
            return render(request, 'signin.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print('Valid')
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Chuyển hướng tới trang chủ hoặc trang dashboard sau khi đăng ký thành công
        else:
            print(form.errors)
    else:  
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    user_groups = Group.objects.filter(groupmember__user=request.user)
    return render(request, 'dashboard.html', {'groups': user_groups})

@login_required
def logout(request):
    return render(request, 'prebase.html')

@login_required
def create_groupchat(request):
    if request.method == 'POST':
        group_name = request.POST['group_name']
        
        # Tạo nhóm mới
        group = Group.objects.create(group_name=group_name)
        # Thêm người dùng hiện tại vào nhóm
        GroupMember.objects.create(group=group, user=request.user)
        # Lấy danh sách user_id từ form (những người dùng khác)
        user_ids = request.POST.getlist('members')
        # Thêm các thành viên còn lại vào nhóm
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            GroupMember.objects.create(group=group, user=user)
        
        return redirect('dashboard')
    else:
        users = User.objects.exclude(id=request.user.id)
        return render(request, 'create_groupchat.html', {'users': users})
    
@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    return redirect('dashboard')

@login_required
def chat_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Kiểm tra xem người dùng có phải là thành viên của nhóm không
    if not GroupMember.objects.filter(group=group, user=request.user).exists():
        return redirect('dashboard')  # Nếu không phải là thành viên thì chuyển về dashboard

    threads = GroupThread.objects.filter(group=group).select_related('first_message')
    messages = GroupMessage.objects.filter(thread__group=group).select_related('sender')

    if request.method == "POST":
        message_content = request.POST.get('message_content')
        if message_content:
            # Tạo thread mới trước
            thread = GroupThread.objects.create(group=group)

            # Tạo tin nhắn mới và gán nó vào thread vừa tạo
            first_message = GroupMessage.objects.create(
                sender=request.user,
                message_content=message_content,
                thread=thread  # Gán thread cho tin nhắn
            )

            # Cập nhật tin nhắn đầu tiên cho thread
            thread.first_message = first_message
            thread.save()

            # Cập nhật tin nhắn mới nhất trong group
            group.latest_message_id = first_message
            group.save()

            return redirect('chat', group_id=group.id)  # Reload trang chat

    return render(request, 'chat.html', {
        'group': group,
        'messages': messages,
        'user': request.user,
    })

@login_required
def thread_view(request, thread_id):
    # 1. 指定されたメッセージを取得
    message = get_object_or_404(GroupMessage, id=thread_id)
    
    # 2. メッセージが属するスレッドを取得
    thread = message.thread
    
    # 3. スレッド内の全メッセージを取得し、タイムスタンプでソート
    messages = GroupMessage.objects.filter(thread=thread).order_by('timestamp')
    
    # 4. グループ情報を取得
    group = thread.group

    # 5. POST リクエストの処理
    if request.method == "POST":
        message_content = request.POST.get('message_content')
        if message_content:
            # 新しい返信メッセージを作成
            GroupMessage.objects.create(
                sender=request.user,
                thread=thread,
                message_content=message_content
            )
            return redirect('thread', message_id=thread_id)  # スレッドのページにリダイレクト
    
    # 6. テンプレートにデータを渡してレンダリング
    return render(request, 'thread.html', {
        'message': message,
        'messages': messages,
        'group': group
    })
