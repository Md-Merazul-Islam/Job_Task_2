from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission


class Category(models.Model):
    name = models.CharField(max_length=50, choices=[('food', 'Food'), ('travel', 'Travel'),
                                                    ('academics', 'Academics'), ('entertainment', 'Entertainment')])

    def __str__(self):
        return self.name




class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    upi_id = models.CharField(max_length=255, null=True, blank=True)  # Store UPI ID here
    college = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    default_payment_method = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"  {self.college}"


class Expense(models.Model):
    student = models.ForeignKey(
        Student, related_name='expenses', on_delete=models.CASCADE, default=1 ,null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True)
    split_type = models.CharField(max_length=50)  
    date = models.DateField()
    receipt_image = models.ImageField(
        upload_to='receipts/', null=True, blank=True)

    def __str__(self):
        # Check if student exists before accessing username
        if self.student:
            return f"Expense: {self.student.username}, {self.amount} {self.category.name}"
        return f"Expense: No student assigned, {self.amount} {self.category.name}"



class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Student)
    type = models.CharField(max_length=50, choices=[(
        'hostel', 'Hostel Roommates'), ('project', 'Project Teams'), ('trip', 'Trip Groups')])


class PaymentMethod(models.Model):
    UPI = 'UPI'
    CREDIT_CARD = 'CC'
    DEBIT_CARD = 'DC'
    NET_BANKING = 'NB'
    COD = 'COD'
    MOBILE_WALLET = 'MW'
    BANK_TRANSFER = 'BT'
    STRIPE = 'STR'
    PAYPAL = 'PP'
    BITCOIN = 'BTC'

    PAYMENT_METHOD_CHOICES = [
        (UPI, 'UPI'),
        (CREDIT_CARD, 'Credit Card'),
        (DEBIT_CARD, 'Debit Card'),
        (NET_BANKING, 'Net Banking'),
        (COD, 'Cash on Delivery'),
        (MOBILE_WALLET, 'Mobile Wallet'),
        (BANK_TRANSFER, 'Bank Transfer'),
        (STRIPE, 'Stripe'),
        (PAYPAL, 'PayPal'),
        (BITCOIN, 'Bitcoin'),
    ]
    
    name = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)
    description = models.TextField()

    def __str__(self):
        return self.get_name_display()



class Settlement(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)

    payment_status = models.CharField(max_length=20, choices=[(
        'pending', 'Pending'), ('completed', 'Completed')])
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    settlement_date = models.DateTimeField(auto_now_add=True , null=True, blank=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return f"Settlement for {self.student} - {self.amount}"


class MonthlyCost(models.Model):
    student = models.ForeignKey(Student, related_name='monthly_costs', on_delete=models.CASCADE,null=True, blank=True)
    month = models.CharField(max_length=10)  # e.g., January
    year = models.IntegerField()
    total_expense = models.FloatField(default=0.0)

    def __str__(self):
        if self.student:
            return f" {self.month} {self.year}: {self.total_expense}"
        return f"Unknown Student - {self.month} {self.year}: {self.total_expense}"

    

class UPIPayment(models.Model):
    settlement = models.OneToOneField(Settlement, on_delete=models.CASCADE)
    upi_id = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')])

    def __str__(self):
        return f"UPI Payment for {self.settlement} - {self.payment_status}"
