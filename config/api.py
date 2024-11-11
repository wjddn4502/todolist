from ninja import NinjaAPI, Router
from todo.models import Todo
from todo.schemas import TodoSchema
from todo.forms import TodoForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from typing import List

api = NinjaAPI()
router = Router()

@api.get("/todos/", response=List[TodoSchema])
def todo_list(request, page: int = 1, kw: str = ""):
    todos = Todo.objects.filter(completed=False)
    if kw:
        todos = todos.filter(
            Q(title__icontains=kw) |
            Q(description__icontains=kw) |
            Q(important__icontains=kw)
        ).distinct()

    from django.core.paginator import Paginator
    paginator = Paginator(todos, 10)
    page_obj = paginator.get_page(page)
    return list(page_obj)

@api.get("/todos/{pk}/", response=TodoSchema)
def todo_detail(request, pk: int):
    todo = get_object_or_404(Todo, id=pk)
    return todo

@api.post("/todos/post", response=TodoSchema)
def todo_post(request, data: TodoSchema):
    todo = Todo.objects.create(**data.dict())
    return todo

@api.delete("/todos/{pk}/", response={204: None})
def todo_delete(request, pk: int):
    todo = get_object_or_404(Todo, id=pk)
    todo.delete()
    return 204, None

@api.put("/todos/{pk}/", response=TodoSchema)
def todo_edit(request, pk: int, data: TodoSchema):
    todo = get_object_or_404(Todo, id=pk)
    for attr, value in data.dict().items():
        setattr(todo, attr, value)
    todo.save()
    return todo

@api.put("/todos/{pk}/done/", response=TodoSchema)
def todo_done(request, pk: int):
    todo = get_object_or_404(Todo, id=pk)
    todo.completed = True
    todo.save()
    return todo

@api.get("/todos/done/", response=List[TodoSchema])
def todo_done_list(request):
    completed_todos = Todo.objects.filter(completed=True)
    return list(completed_todos)

@api.get("/hello")
def hello(request, name: str):
    return {"message": f"Hello {name}"}

@api.get("/test")
def test(request):
    return {"test": "success"}
