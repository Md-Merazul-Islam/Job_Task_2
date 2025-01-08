from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission


class Category(models.Model):
    name = models.CharField(max_length=50, choices=[('food', 'Food'), ('travel', 'Travel'),
                                                    ('academics', 'Academics'), ('entertainment', 'Entertainment')])

    def __str__(self):
        return self.name


class Student(AbstractUser):
    college = models.CharField(max_length=100)
    semester = models.IntegerField()
    default_payment_methods = models.CharField(
        max_length=50, null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name="student_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="student_permissions",
        blank=True,
    )



class Expense(models.Model):
    # Default to a specific student's ID
    student = models.ForeignKey(
        Student, related_name='expenses', on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.FloatField()
    split_type = models.CharField(max_length=50)  
    date = models.DateField()
    receipt_image = models.ImageField(
        upload_to='receipts/', null=True, blank=True)

    def __str__(self):
        return f"Expense: {self.student.username}, {self.amount} {self.category.name}"


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Student)
    type = models.CharField(max_length=50, choices=[(
        'hostel', 'Hostel Roommates'), ('project', 'Project Teams'), ('trip', 'Trip Groups')])

# Settlement Model


class Settlement(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20, choices=[(
        'pending', 'Pending'), ('completed', 'Completed')])
    settlement_method = models.CharField(max_length=50)
    due_date = models.DateField()
