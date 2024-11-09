from ninja import Router, NinjaAPI
from .forms import TodoForm
from .models import Todo
from .schemas import TodoSchema
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q

# Ninja API 객체 생성
api = NinjaAPI()

# API 엔드포인트
@api.get("/todos", response=list[TodoSchema])
def todo_list(request):
    page = request.GET.get('page', '1')  # 페이지
    todos = Todo.objects.filter(completed=False)
    kw = request.GET.get('kw', '')  # 검색어

    if kw:
        todos = todos.filter(
            Q(title__icontains=kw) |  # 제목 검색
            Q(description__icontains=kw) |  # 설명 검색
            Q(important__icontains=kw)  # 중요도 검색 (중요도가 텍스트라면 사용 가능)
        ).distinct()

    paginator = Paginator(todos, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    # 기존에 사용하던 컨텍스트를 반환
    return render(request, 'todo/todo_list.html', {'todos': page_obj})

# 웹 뷰
def todo_detail(request, pk):
    todo = Todo.objects.get(id=pk)
    return render(request, 'todo/todo_detail.html', {'todo': todo})

def todo_post(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todo/todo_post.html', {'form': form})

def todo_delete(request, pk):
    todo = get_object_or_404(Todo, id=pk)
    todo.delete()
    return redirect('todo_list')  # 삭제 후 목록 페이지로 리다이렉트

def todo_done_delete(request, pk):
    todo = get_object_or_404(Todo, id=pk)
    todo.delete()
    return redirect('todo_done_list')  # 삭제 후 삭제 목록 페이지로 리다이렉트

def todo_edit(request, pk):
    todo = get_object_or_404(Todo, id=pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/todo_post.html', {'form': form})

def home(request):
    return render(request, 'todo/home.html')  # 템플릿 경로가 정확한지 확인

def todo_done(request, pk):
    todo = get_object_or_404(Todo, id=pk)
    todo.completed = True
    todo.save()
    return redirect('todo_list')

def todo_done_list(request):
    completed_todos = Todo.objects.filter(completed=True)  # completed 필드가 True인 항목만 가져옴
    return render(request, 'todo/todo_done_list.html', {'todos': completed_todos})
