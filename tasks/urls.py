from django.urls import path, include
from . import views
urlpatterns=[
    path('',views.Read,name='task_list'),
    path('create/',views.Create,name='task_creating'),
    path('update/<int:pk>',views.Update,name='task_updating'),
    path('delete/<int:pk>',views.Delete,name='task_Deleting'),
    path('toggle/<int:pk>',views.ToggleComplete,name='task_toggle'),
        # url name, ,, FUNCTION NAME IN VIEW, alias to give
]