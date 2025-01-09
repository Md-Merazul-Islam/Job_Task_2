from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Student, Expense, Group, Settlement, Category, MonthlyCost,UPIPayment
from .serializers import StudentSerializer, ExpenseSerializer, GroupSerializer, SettlementSerializer, CategorySerializer,MonthlyCostSerializer,UPIPaymentSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # permission_classes = [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        student = self.get_object()
        if student.user != request.user:
            return Response({"detail": "You can only update your own profile."}, status=400)

        # Proceed with the update
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def link_upi(self, request):
        student = Student.objects.get(user=request.user)
        upi_id = request.data.get('upi_id')
        
        if upi_id:
            student.upi_id = upi_id
            student.save()
            return Response({"detail": "UPI ID linked successfully."})

        return Response({"detail": "UPI ID is required."}, status=400)


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
    
    @action(detail=True, methods=['post'])
    def process_upi_payment(self, request, pk=None):
        settlement = self.get_object()
        if settlement.payment_status == 'paid':
            return Response({"detail": "Settlement already paid."}, status=400)
        upi_id = request.data.get('upi_id')
        transaction_id = request.data.get('transaction_id')

        if not upi_id or not transaction_id:
            return Response({"detail": "UPI ID and Transaction ID are required."}, status=400)
        upi_payment = UPIPayment.objects.create(
            settlement=settlement,
            upi_id=upi_id,
            transaction_id=transaction_id,
            payment_status='pending'  
        )

        payment_method = PaymentMethod.objects.get(name='UPI')  
        settlement.payment_method = payment_method
        settlement.payment_status = 'pending'
        settlement.save()

        # Return UPI payment details
        serializer = UPIPaymentSerializer(upi_payment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm_upi_payment(self, request, pk=None):
        settlement = self.get_object()
        upi_payment = UPIPayment.objects.get(settlement=settlement)

        # Check if the UPI payment is pending
        if upi_payment.payment_status != 'pending':
            return Response({"detail": "No pending UPI payment found."}, status=400)
        # Assuming payment is successful for demonstration
        upi_payment.payment_status = 'success'
        upi_payment.save()

        # Update settlement status
        settlement.payment_status = 'paid'
        settlement.save()

        return Response({"detail": "UPI payment confirmed."})


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