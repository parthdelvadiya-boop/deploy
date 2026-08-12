from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("",views.task_list,name="task_list"),
    path("register/",views.register_view,name="register"),
    path("login/",views.login_view,name="login"),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("task/create/",views.task_create,name="task_create"),
    path("task/<int:pk>/update/",views.task_update,name="task_update"),
    path("task/<int:pk>/delete/",views.task_delete,name="task_delete"),
    path("task/<int:pk>/complete/",views.task_complete,name="task_complete"),
]