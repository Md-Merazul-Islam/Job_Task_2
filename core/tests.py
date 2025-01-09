from rest_framework.test import APITestCase
from rest_framework import status
from .models import Expense, Student, Category

class ExpenseAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='food')
        self.student = Student.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.student)
        self.expense_data = {
            'student': self.student.id,
            'category': self.category.id,
            'amount': 100.0,
            'split_type': 'equal',
            'date': '2025-01-01',
        }

    def test_create_expense(self):
        response = self.client.post('/api/expenses/', self.expense_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_expenses(self):
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
