from django.urls import path
from app import views
app_name ='app'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.signout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('success/', views.success, name='success'),
    path('add-todo/', views.add_todo,name ='add-todo'),
    path('delete-todo/<int:id>', views.delete_todo,name ='delete-todo'),
    path('change-todo/<int:id>/<str:status>', views.change_todo,name ='change-todo'),
]