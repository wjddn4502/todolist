from django.urls import path
from . import views
from ninja import NinjaAPI
api = NinjaAPI()
urlpatterns = [
    path('', views.todo_list, name='todo_list'),
	path('<int:pk>/', views.todo_detail, name='todo_detail'),
	path('post/', views.todo_post, name='todo_post'),
    path('todo_done/delete/<int:pk>/', views.todo_done_return, name='todo_done_return'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('done/delete/<int:pk>/', views.todo_done_delete, name='todo_done_delete'),
    path('edit/<int:pk>/', views.todo_edit, name='todo_edit'),
    path('done/<int:pk>/', views.todo_done, name='todo_done'),
    path('api/', api.urls),
    path('done/', views.todo_done_list, name='todo_done_list'),
]