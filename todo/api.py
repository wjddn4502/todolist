from ninja import NinjaAPI
from ninja import Router
from .models import Todo
from .schemas import TodoSchema
from .forms import TodoForm
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
# Ninja API 객체 생성

api = NinjaAPI()



# /api/todos - GET 요청 처리 (API)
@api.get("/todos", response=list[TodoSchema])
def todo_list(request):
    page = request.GET.get('page', '1')  # 페이지
    todos = Todo.objects.filter(completed=False)
    kw = request.GET.get('kw', '')  # 검색어

    if kw:
        todos = todos.filter(
            Q(title__icontains=kw) |  # 제목 검색
            Q(description__icontains=kw) |  # 설명 검색
            Q(important__icontains=kw)  # 중요도 검색
        ).distinct()

    paginator = Paginator(todos, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    # API는 JSON 반환 (웹 페이지용 렌더링도 처리)
    return render(request, 'todo/todo_list.html', {'todos': page_obj})

# /api/todos/{pk} - GET 요청 처리 (상세보기 API)
@api.get("/todos/{pk}", response=TodoSchema)
def todo_detail(request, pk: int):
    todo = get_object_or_404(Todo, id=pk)
    return render(request, 'todo/todo_detail.html', {'todo': todo})

# /api/todos - POST 요청 처리 (추가 API)
@api.post("/todos", response=TodoSchema)
def todo_post(request):
    form = TodoForm(request.POST)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.save()
        return redirect('todo_list')
    return render(request, 'todo/todo_post.html', {'form': form})

# /api/todos/{pk} - DELETE 요청 처리 (삭제 API)
@api.delete("/todos/{pk}")
def todo_delete(request, pk: int):
    todo = get_object_or_404(Todo, id=pk)
    todo.delete()
    return redirect('todo_list')

# /api/todos/{pk} - PUT 요청 처리 (수정 API)
@api.put("/todos/{pk}", response=TodoSchema)
def todo_edit(request, pk: int):
    todo = get_object_or_404(Todo, id=pk)
    form = TodoForm(request.POST, instance=todo)
    if form.is_valid():
        form.save()
        return redirect('todo_list')
    return render(request, 'todo/todo_post.html', {'form': form})

# /api/todos/{pk}/done - PUT 요청 처리 (완료 표시 API)
@api.put("/todos/{pk}/done", response=TodoSchema)
def todo_done(request, pk: int):
    todo = get_object_or_404(Todo, id=pk)
    todo.completed = True
    todo.save()
    return redirect('todo_list')

# 완료된 항목 리스트 (웹 페이지용)
@api.get("/todos/done", response=list[TodoSchema])
def todo_done_list(request):
    completed_todos = Todo.objects.filter(completed=True)  # completed 필드가 True인 항목만 가져옴
    return completed_todos