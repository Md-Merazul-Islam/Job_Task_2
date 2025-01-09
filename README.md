# Student Management and Payment System

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
   git clone <repository-url>
   cd <project-directory>
