﻿# Student Management and Payment System

## Overview

This project is a Student Management and Payment System built using Django and Django REST Framework (DRF). It allows managing students, expenses, group settlements, categories, and UPI payment integration. The system also provides user registration and login functionality with email activation and JWT authentication for secure access.

The main components of this system include:

- **Student Management**: Create, update, and view student profiles.
- **Expenses**: Add and track expenses associated with students.
- **Settlements**: Handle financial settlements and UPI payments.
- **Categories**: Manage different categories for expenses.
- **UPI Payments**: Process UPI transactions for settlements.

## Features

- **Student Profile Management**: Allows users to update their profiles and link their UPI IDs.
- **Expense Management**: Record student expenses and track monthly costs.
- **Settlement Processing**: Handle group settlements and confirm UPI payments.
- **User Registration**: Register new users with email activation.
- **User Authentication**: Login with JWT tokens, support for username/email and password authentication.
- **UPI Payment Integration**: Handle UPI transactions for settlements.

## Setup

### Prerequisites

- Python 3.8+
- Django 3.2+
- Django REST Framework (DRF)
- PostgreSQL (or another database)
- Pip (for package installation)
- SMTP server for email handling (for account activation emails)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Md-Merazul-Islam/School-Management-System.git
   cd <project-directory>


2. **Install dependencies:
   ```bash
   pip install -r requirements.txt

3. **Set up the database:
If using PostgreSQL, create a database and update the DATABASES settings in settings.py.

4. **Run the migrations:
   ```base
   python manage.py migrate

5. **Run the development server:

   ```bash
   python manage.py runserver
   
Test the endpoints: The application will be available at http://127.0.0.1:8000/. You can interact with the API using tools like Postman or Insomnia.


# API Documentation & API Endpoints : 

This is the documentation for the API of the project. Below are the available endpoints organized by their respective resources.

---

## **Account Endpoints**

### **POST** `/account/login/`
- **Action**: Login to the system.
- **Function**: `account_login_create`

### **POST** `/account/logout/`
- **Action**: Logout from the system.
- **Function**: `account_logout_create`

### **GET** `/account/profile/`
- **Action**: Get the profile details of the logged-in user.
- **Function**: `account_profile_read`

### **PUT** `/account/profile/`
- **Action**: Update the profile details of the logged-in user.
- **Function**: `account_profile_update`

### **PATCH** `/account/profile/`
- **Action**: Partially update the profile details of the logged-in user.
- **Function**: `account_profile_partial_update`

### **POST** `/account/register/`
- **Action**: Register a new account.
- **Function**: `account_register_create`

---

## **API Endpoints for Categories**

### **GET** `/api/categories/`
- **Action**: Get the list of categories.
- **Function**: `api_categories_list`

### **POST** `/api/categories/`
- **Action**: Create a new category.
- **Function**: `api_categories_create`

### **GET** `/api/categories/{id}/`
- **Action**: Get details of a specific category by ID.
- **Function**: `api_categories_read`

### **PUT** `/api/categories/{id}/`
- **Action**: Update a category by ID.
- **Function**: `api_categories_update`

### **PATCH** `/api/categories/{id}/`
- **Action**: Partially update a category by ID.
- **Function**: `api_categories_partial_update`

### **DELETE** `/api/categories/{id}/`
- **Action**: Delete a category by ID.
- **Function**: `api_categories_delete`

---

## **API Endpoints for Expenses**

### **GET** `/api/expenses/`
- **Action**: Get the list of expenses.
- **Function**: `api_expenses_list`

### **POST** `/api/expenses/`
- **Action**: Create a new expense.
- **Function**: `api_expenses_create`

### **GET** `/api/expenses/{id}/`
- **Action**: Get details of a specific expense by ID.
- **Function**: `api_expenses_read`

### **PUT** `/api/expenses/{id}/`
- **Action**: Update an expense by ID.
- **Function**: `api_expenses_update`

### **PATCH** `/api/expenses/{id}/`
- **Action**: Partially update an expense by ID.
- **Function**: `api_expenses_partial_update`

### **DELETE** `/api/expenses/{id}/`
- **Action**: Delete an expense by ID.
- **Function**: `api_expenses_delete`

---

## **API Endpoints for Groups**

### **GET** `/api/groups/`
- **Action**: Get the list of groups.
- **Function**: `api_groups_list`

### **POST** `/api/groups/`
- **Action**: Create a new group.
- **Function**: `api_groups_create`

### **GET** `/api/groups/{id}/`
- **Action**: Get details of a specific group by ID.
- **Function**: `api_groups_read`

### **PUT** `/api/groups/{id}/`
- **Action**: Update a group by ID.
- **Function**: `api_groups_update`

### **PATCH** `/api/groups/{id}/`
- **Action**: Partially update a group by ID.
- **Function**: `api_groups_partial_update`

### **DELETE** `/api/groups/{id}/`
- **Action**: Delete a group by ID.
- **Function**: `api_groups_delete`

---

## **API Endpoints for Monthly Costs**

### **GET** `/api/monthly-costs/`
- **Action**: Get the list of monthly costs.
- **Function**: `api_monthly-costs_list`

---

## **API Endpoints for Settlements**

### **GET** `/api/settlements/`
- **Action**: Get the list of settlements.
- **Function**: `api_settlements_list`

### **POST** `/api/settlements/`
- **Action**: Create a new settlement.
- **Function**: `api_settlements_create`

### **GET** `/api/settlements/{id}/`
- **Action**: Get details of a specific settlement by ID.
- **Function**: `api_settlements_read`

### **PUT** `/api/settlements/{id}/`
- **Action**: Update a settlement by ID.
- **Function**: `api_settlements_update`

### **PATCH** `/api/settlements/{id}/`
- **Action**: Partially update a settlement by ID.
- **Function**: `api_settlements_partial_update`

### **DELETE** `/api/settlements/{id}/`
- **Action**: Delete a settlement by ID.
- **Function**: `api_settlements_delete`

### **POST** `/api/settlements/{id}/confirm_upi_payment/`
- **Action**: Confirm UPI payment for a settlement.
- **Function**: `api_settlements_confirm_upi_payment`

### **POST** `/api/settlements/{id}/process_upi_payment/`
- **Action**: Process UPI payment for a settlement.
- **Function**: `api_settlements_process_upi_payment`

---

## **API Endpoints for Students**

### **GET** `/api/students/`
- **Action**: Get the list of students.
- **Function**: `api_students_list`

### **POST** `/api/students/`
- **Action**: Create a new student.
- **Function**: `api_students_create`

### **PATCH** `/api/students/link_upi/`
- **Action**: Link a student's UPI ID.
- **Function**: `api_students_link_upi`

### **GET** `/api/students/{id}/`
- **Action**: Get details of a specific student by ID.
- **Function**: `api_students_read`

### **PUT** `/api/students/{id}/`
- **Action**: Update a student's details by ID.
- **Function**: `api_students_update`

### **PATCH** `/api/students/{id}/`
- **Action**: Partially update a student's details by ID.
- **Function**: `api_students_partial_update`

### **DELETE** `/api/students/{id}/`
- **Action**: Delete a student by ID.
- **Function**: `api_students_delete`


