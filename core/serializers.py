from rest_framework import serializers
from .models import Student, Expense, Group, Settlement, Category,MonthlyCost

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'username', 'email', 'college', 'semester', 'default_payment_methods']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = '__all__'


class MonthlyCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyCost
        fields = '__all__'