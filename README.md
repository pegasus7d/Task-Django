# Django Vendor Management System

This is a Django Vendor Management System designed to handle vendor profiles, track purchase orders, and calculate vendor performance metrics using Django and Django REST Framework.

## Getting Started

These instructions will guide you through setting up the project on your local machine for development and testing purposes.

### Prerequisites

Ensure you have Python and pip installed on your system. You will also need the following packages:
- Django
- Django REST Framework
- djangorestframework-simplejwt for JWT-based authentication
- NumPy

### Installation

Follow these steps to get your development environment running:

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/django-vendor-management.git
   cd django-vendor-management

   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install django djangorestframework djangorestframework-simplejwt numpy
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver

