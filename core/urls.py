from django.urls import path
from core import views

urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employees_list'),
    path('view/<int:pk>', views.EmployeeView.as_view(), name='employee_view'),
    path('new', views.EmployeeCreate.as_view(), name='employee_new'),
    path('edit/<int:pk>', views.EmployeeUpdate.as_view(), name='employee_edit'),
    path('delete/<int:pk>', views.EmployeeDelete.as_view(), name='employee_delete'),
]