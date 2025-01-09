from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Student, Expense, Group, Settlement, Category, MonthlyCost
from .serializers import StudentSerializer, ExpenseSerializer, GroupSerializer, SettlementSerializer, CategorySerializer,MonthlyCostSerializer
from rest_framework.response import Response

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    # permission_classes = [IsAuthenticated]
    
    
    def perform_create(self, serializer):
        expense = serializer.save()
        month = expense.date.strftime('%B')
        year = expense.date.year
        student = expense.student
        monthly_cost, created = MonthlyCost.objects.get_or_create(
            student=student, month=month, year=year
        )
        monthly_cost.total_expense += expense.amount
        monthly_cost.save()



class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [IsAuthenticated]


class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.all()
    serializer_class = SettlementSerializer
    # permission_classes = [IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticated]




class MonthlyCostViewSet(viewsets.ViewSet):
    def list(self, request):
        student_id = request.query_params.get('student_id')
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        filters = {}
        if student_id:
            filters['student__id'] = student_id
        if month:
            filters['month'] = month
        if year:
            filters['year'] = year

        monthly_costs = MonthlyCost.objects.filter(**filters)
        serializer = MonthlyCostSerializer(monthly_costs, many=True)
        return Response(serializer.data)