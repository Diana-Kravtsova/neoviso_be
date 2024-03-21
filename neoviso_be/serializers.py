from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from rest_framework import serializers

from neoviso_be.models import Customer, Department, Employee, Appointment
from neoviso_be.settings import EMAIL_HOST_USER


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class AppointmentGetSerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'date', 'start', 'end', 'employee', 'customer']

    def get_employee(self, obj: Appointment):
        return {
            "id": obj.employee.id,
            "userId": obj.employee.user.id,
            "fullname": obj.employee.user.username
        }

    def get_customer(self, obj: Appointment):
        return {
            "id": obj.customer.id,
            "fullname": obj.customer.fullname
        }


class AppointmentSerializer(serializers.ModelSerializer):
    employeeId = serializers.PrimaryKeyRelatedField(source='employee', queryset=Employee.objects.all())
    employeeId.default_error_messages['does_not_exist'] = 'Employee was not found'

    customerId = serializers.PrimaryKeyRelatedField(source='customer', queryset=Customer.objects.all())
    employeeId.default_error_messages['does_not_exist'] = 'Customer was not found'

    class Meta:
        model = Appointment
        fields = ['id', 'date', 'start', 'end', 'employeeId', 'customerId']


class EmployeeGetSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')
    fullname = serializers.CharField(source='user.username')
    userId = serializers.IntegerField(source='user.id')

    class Meta:
        model = Employee
        fields = ['id', 'fullname', 'email', 'phone', 'address', 'department', 'userId', 'roles']

    def get_department(self, obj: Employee):
        return {
            "id": obj.department.id,
            "fullname": obj.department.fullname
        }

    def get_roles(self, obj: Employee):
        groups = obj.user.groups.all()
        return [group.name for group in groups]

class EmployeeSerializer(serializers.ModelSerializer):
    departmentId = serializers.PrimaryKeyRelatedField(source='department', queryset=Department.objects.all())
    departmentId.default_error_messages['does_not_exist'] = 'Department was not found'
    email = serializers.EmailField(source='user.email')
    fullname = serializers.CharField(source='user.username')
    roles = serializers.ManyRelatedField(source='user.groups', child_relation=serializers.CharField())

    class Meta:
        model = Employee
        fields = ['email', 'fullname', 'roles', 'phone', 'address', 'departmentId']

    def create(self, validated_data):
        password = User.objects.make_random_password()
        hashed_password = make_password(password)

        user = User.objects.create(
            email=validated_data['user']['email'],
            username=validated_data['user']['username'],
            password=hashed_password
        )

        # not working yet
        # subject = 'Your Generated Password'
        # message = f'Your generated password is: {password}'
        # sender = EMAIL_HOST_USER
        # recipient = user.email
        # send_mail(subject, message, sender, [recipient])

        try:
            for role in validated_data['user']['groups']:
                group = Group.objects.get(name=role)
                group.user_set.add(user)
        except Group.DoesNotExist:
            raise serializers.ValidationError('Group does not exist')

        employee = Employee.objects.create(
            user=user,
            phone=validated_data['phone'],
            address=validated_data['address'],
            department=validated_data['department']
        )

        return employee

    def update(self, instance: Employee, validated_data):
        instance.user.email = validated_data['user']['email']
        instance.user.username = validated_data['user']['username']
        instance.phone = validated_data['phone']
        instance.address = validated_data['address']
        instance.department = validated_data['department']

        instance.user.groups.clear()
        try:
            for role in validated_data['user']['groups']:
                group = Group.objects.get(name=role)
                group.user_set.add(instance.user)
        except Group.DoesNotExist:
            raise serializers.ValidationError('Group does not exist')

        instance.save()
        instance.user.save()
        return instance
