from rest_framework import serializers
from .models import Student, Expense, Group, Settlement, Category,MonthlyCost,UPIPayment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['user', 'upi_id', 'college', 'semester', 'default_payment_method']

    def validate_upi_id(self, value):
        if value and not value.endswith('@upi'):  
            raise serializers.ValidationError("Invalid UPI ID format.")
        return value

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
        
        

class UPIPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UPIPayment
        fields = ['settlement', 'upi_id', 'transaction_id', 'payment_status']