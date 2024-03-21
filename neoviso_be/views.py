import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View

from neoviso_be.auth.permissions import has_permission, user_has_permission
from neoviso_be.models import Customer, Department, Employee, Appointment
from neoviso_be.response import Response, PageResponse
from neoviso_be.serializers import CustomerSerializer, DepartmentSerializer, \
    EmployeeGetSerializer, AppointmentGetSerializer, AppointmentSerializer, EmployeeSerializer


class CustomerView(View):
    @staticmethod
    @has_permission('view_customer')
    def get(request, id):
        try:
            customer = Customer.objects.get(id=id)
            serializer = CustomerSerializer(customer)
            response = Response(model=serializer.data, message="Customer was retrieved successfully")
            return JsonResponse(response.__dict__, status=200)
        except Customer.DoesNotExist:
            response = Response(message="Customer was not found")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('add_customer')
    def post(request):
        try:
            data = json.loads(request.body)
            serializer = CustomerSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = Response(model=serializer.data, message="Customer was created successfully")
                return JsonResponse(response.__dict__, status=201)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('change_customer')
    def put(request, id):
        try:
            data = json.loads(request.body)

            customer = Customer.objects.get(id=id)
            serializer = CustomerSerializer(instance=customer, data=data)
            if serializer.is_valid():
                serializer.save()
                response = Response(model=serializer.data, message="Customer was updated successfully")
                return JsonResponse(response.__dict__, status=200)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except Customer.DoesNotExist:
            response = Response(message="Customer was not found")
            return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('delete_customer')
    def delete(request, id):
        try:
            customer = Customer.objects.get(id=id)
            customer.delete()
            response = Response(message="Customer was deleted successfully")
            return JsonResponse(response.__dict__, status=204)
        except Customer.DoesNotExist:
            response = Response(message="Customer was not found")
            return JsonResponse(response.__dict__, status=400)


class CustomerListView(View):
    @staticmethod
    @has_permission('view_customer')
    def get(request):
        queryset = Customer.objects.all().order_by('id')
        page_number = request.GET.get('pageNumber')
        per_page = request.GET.get('pageSize')
        if page_number is None and per_page is None:
            serializer = CustomerSerializer(queryset, many=True)
            response = Response(model=serializer.data,
                                message="List of employees was retrieved successfully")
            return JsonResponse(response.__dict__, status=200)

        else:
            paginator = Paginator(queryset, per_page)
            try:
                page_obj = paginator.page(page_number)
            except:
                page_obj = paginator.page(1)

            serializer = CustomerSerializer(page_obj.object_list, many=True)
            response = PageResponse(
                model=serializer.data,
                message="Page of customers was retrieved successfully",
                page_obj=page_obj,
                paginator=paginator
            )
            return JsonResponse(response.__dict__(), status=200)


class DepartmentView(View):
    @staticmethod
    @has_permission('view_department')
    def get(request, id):
        try:
            department = Department.objects.get(id=id)
            serializer = DepartmentSerializer(department)
            response = Response(model=serializer.data, message="Department was retrieved successfully")
            return JsonResponse(response.__dict__, status=200)
        except Department.DoesNotExist:
            response = Response(message="Department was not found")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('add_department')
    def post(request):
        try:
            data = json.loads(request.body)
            serializer = DepartmentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = Response(model=serializer.data, message="Department was created successfully")
                return JsonResponse(response.__dict__, status=201)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('change_department')
    def put(request, id):
        try:
            data = json.loads(request.body)

            department = Department.objects.get(id=id)
            serializer = DepartmentSerializer(instance=department, data=data)
            if serializer.is_valid():
                serializer.save()
                response = Response(model=serializer.data, message="Department was updated successfully")
                return JsonResponse(response.__dict__, status=200)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except Department.DoesNotExist:
            response = Response(message="Department was not found")
            return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('delete_department')
    def delete(request, id):
        try:
            department = Department.objects.get(id=id)
            department.delete()
            response = Response(message="Department was deleted successfully")
            return JsonResponse(response.__dict__, status=204)
        except Department.DoesNotExist:
            response = Response(message="Department was not found")
            return JsonResponse(response.__dict__, status=400)


class DepartmentListView(View):
    @staticmethod
    @has_permission('view_department')
    def get(request):
        queryset = Department.objects.all()
        serializer = DepartmentSerializer(queryset, many=True)
        response = Response(model=serializer.data,
                            message="List of departments was retrieved successfully")
        return JsonResponse(response.__dict__, status=200)


class AppointmentView(View):
    @staticmethod
    @has_permission('view_appointment')
    def get(request, id):
        try:
            appointment = Appointment.objects.get(id=id)
            serializer = AppointmentGetSerializer(appointment)
            response = Response(model=serializer.data, message="Appointment was retrieved successfully")
            return JsonResponse(response.__dict__, status=200)
        except Appointment.DoesNotExist:
            response = Response(message="Appointment was not found")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('add_appointment')
    def post(request):
        try:
            data = json.loads(request.body)
            serializer = AppointmentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = Response(model=serializer.data, message="Appointment was created successfully")
                return JsonResponse(response.__dict__, status=201)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('change_own_appointment')
    def put(request, id):
        try:
            data = json.loads(request.body)

            if user_has_permission(request.user, 'change_other_appointment'):
                appointment = Appointment.objects.get(id=id)
            else:
                appointment = Appointment.objects.get(id=id, employee=request.user.employee)
            serializer = AppointmentSerializer(instance=appointment, data=data)
            if serializer.is_valid():
                serializer.save()
                response = Response(model=serializer.data, message="Appointment was updated successfully")
                return JsonResponse(response.__dict__, status=200)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except Appointment.DoesNotExist:
            response = Response(message="Appointment was not found")
            return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('delete_own_appointment')
    def delete(request, id):
        try:
            if user_has_permission(request.user, 'delete_other_appointment'):
                appointment = Appointment.objects.get(id=id)
            else:
                appointment = Appointment.objects.get(id=id, employee=request.user.employee)
            appointment.delete()
            response = Response(message="Appointment was deleted successfully")
            return JsonResponse(response.__dict__, status=204)
        except Appointment.DoesNotExist:
            response = Response(message="Appointment was not found")
            return JsonResponse(response.__dict__, status=400)


class AppointmentListView(View):
    @staticmethod
    @has_permission('view_appointment')
    def get(request):
        queryset = Appointment.objects.all().order_by('id')
        page_number = request.GET.get('pageNumber')
        per_page = request.GET.get('pageSize')
        paginator = Paginator(queryset, per_page)

        try:
            page_obj = paginator.page(page_number)
        except:
            page_obj = paginator.page(1)

        serializer = AppointmentGetSerializer(page_obj.object_list, many=True)
        response = PageResponse(
            model=serializer.data,
            message="Page of appointments was retrieved successfully",
            page_obj=page_obj,
            paginator=paginator
        )
        return JsonResponse(response.__dict__(), status=200)


class EmployeeView(View):
    @staticmethod
    @has_permission('view_employee')
    def get(request, id):
        try:
            employee = Employee.objects.get(id=id)
            serializer = EmployeeGetSerializer(employee)
            response = Response(model=serializer.data, message="Employee was retrieved successfully")
            return JsonResponse(response.__dict__, status=200)
        except Employee.DoesNotExist:
            response = Response(message="Employee was not found")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('add_employee')
    def post(request):
        try:
            data = json.loads(request.body)
            serializer = EmployeeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = Response(model=serializer.data, message="Employee was created successfully")
                return JsonResponse(response.__dict__, status=201)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('change_employee')
    def put(request, id):
        try:
            data = json.loads(request.body)

            employee = Employee.objects.get(id=id)
            serializer = EmployeeSerializer(instance=employee, data=data)
            if serializer.is_valid():
                serializer.save()
                response = Response(model=serializer.data, message="Employee was updated successfully")
                return JsonResponse(response.__dict__, status=200)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except Employee.DoesNotExist:
            response = Response(message="Employee was not found")
            return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('delete_employee')
    def delete(request, id):
        try:
            employee = Employee.objects.get(id=id)
            employee.delete()
            employee.user.delete()
            response = Response(message="Employee was deleted successfully")
            return JsonResponse(response.__dict__, status=204)
        except Employee.DoesNotExist:
            response = Response(message="Employee was not found")
            return JsonResponse(response.__dict__, status=400)



class EmployeeListView(View):
    @staticmethod
    @has_permission('view_employee')
    def get(request):
        queryset = Employee.objects.all()
        serializer = EmployeeGetSerializer(queryset, many=True)
        response = Response(model=serializer.data,
                            message="List of employees was retrieved successfully")
        return JsonResponse(response.__dict__, status=200)
