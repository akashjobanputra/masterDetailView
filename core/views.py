from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django_tables2 import tables, SingleTableView

from .models import Employee, EmployeeInfo


EmployeeFormSet = inlineformset_factory(
    Employee, EmployeeInfo, fields=(
        'dob', 'gender', 'phone', 'curr_address', 'soft_delete',),
    can_delete=False
)


class EmployeeTable(tables.Table):
    class Meta:
        model = Employee
        fields = ('name', 'email', 'soft_delete')

# Create your views here.
# class EmployeeListView(generic.ListView):


class EmployeeListView(SingleTableView):
    model = Employee
    table_class = EmployeeTable
    # fields=['name', 'email', 'soft_delete']
    template_name = 'core/employeeList.html'
    # paginate_by = 10
    queryset = Employee.objects.order_by('soft_delete', 'id')


class EmployeeView(generic.DetailView):
    model = Employee
    template_name = 'core/employeeDetail.html'

    def get_context_data(self, **kwargs):
        # xxx will be available in the template as the related objects
        context = super(EmployeeView, self).get_context_data(**kwargs)
        context['employeeInfo'] = EmployeeInfo.objects.filter(
            employee=self.get_object())[0]
        print(context)
        return context


class EmployeeCreate(generic.edit.CreateView):
    model = Employee
    fields = ['name', 'email']
    success_url = reverse_lazy('employees_list')
    template_name = 'core/employeeForm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['employeeInfo'] = EmployeeFormSet(self.request.POST)
        else:
            context['employeeInfo'] = EmployeeFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        employeeInfo = context['employeeInfo']
        self.object = form.save()
        if employeeInfo.is_valid():
            employeeInfo.instance = self.object
            employeeInfo.save()
        return super().form_valid(form)


class EmployeeUpdate(generic.edit.UpdateView):
    model = Employee
    fields = ['name', 'email', 'soft_delete']
    success_url = reverse_lazy('employees_list')
    template_name = 'core/employeeForm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            print(self.request.POST)
            context['employeeInfo'] = EmployeeFormSet(
                self.request.POST, instance=self.object)
        else:
            context['employeeInfo'] = EmployeeFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        employeeInfo = context['employeeInfo']
        self.object = form.save()
        if employeeInfo.is_valid():
            employeeInfo.instance = self.object
            employeeInfo.save()
        return super().form_valid(form)


class EmployeeDelete(generic.edit.DeleteView):
    model = Employee
    success_url = reverse_lazy('employees_list')

    def delete(self, request, *args, **kargs):
        self.employee = self.get_object()
        self.employeeInfo = EmployeeInfo.objects.filter(
            employee=self.get_object())[0]
        self.employee.soft_delete = True
        self.employeeInfo.soft_delete = True
        self.employee.save()
        self.employeeInfo.save()
        return HttpResponseRedirect(self.success_url)
