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
   To start, clone the repository to your local machine and navigate into the project directory:

   ```bash
   git clone https://github.com/yourusername/django-vendor-management.git
   cd django-vendor-management
2. **Set up a virtual environment**
Next, set up a Python virtual environment by running:

- For Unix-based systems:
  ```
  python -m venv venv
  source venv/bin/activate
  ```
- For Windows:
  ```
  python -m venv venv
  venv\Scripts\activate
  ```

3. **Install the required packages**
Install Django, Django REST Framework, SimpleJWT, and NumPy using pip:
  ```
  pip install django djangorestframework djangorestframework-simplejwt numpy
  ```

4. **Apply migrations**
Initialize your database schema by applying migrations:

  ```
  python manage.py migrate
  ```
5. **Create an admin user**
Create a superuser for the Django admin interface:
  ```
  python manage.py createsuperuser
  ```

6. **Run the development server**
Start the development server to make the application accessible on your local machine:
  ```
  python manage.py runserver
  ```

Access the server at http://127.0.0.1:8000/
   

