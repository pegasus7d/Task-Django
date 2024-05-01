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


# Backend Logic and Data Models

## Data Models

### Vendor Model
Stores essential information about each vendor along with performance metrics.
- **name**: `CharField` - Vendor's name.
- **contact_details**: `TextField` - Contact information of the vendor.
- **address**: `TextField` - Physical address of the vendor.
- **vendor_code**: `CharField` - Unique identifier for the vendor.
- **on_time_delivery_rate**: `FloatField` - Tracks the percentage of on-time deliveries.
- **quality_rating_avg**: `FloatField` - Average rating of quality based on purchase orders.
- **average_response_time**: `FloatField` - Average time taken to acknowledge purchase orders.
- **fulfillment_rate**: `FloatField` - Percentage of purchase orders fulfilled successfully.

### Purchase Order (PO) Model
Captures details of each purchase order and used for calculating performance metrics.
- **po_number**: `CharField` - Unique number identifying the PO.
- **vendor**: `ForeignKey` - Link to the Vendor model.
- **order_date**: `DateTimeField` - Date when the order was placed.
- **delivery_date**: `DateTimeField` - Expected or actual delivery date of the order.
- **items**: `JSONField` - Details of items ordered.
- **quantity**: `IntegerField` - Total quantity of items in the PO.
- **status**: `CharField` - Current status of the PO (e.g., pending, completed, canceled).
- **quality_rating**: `FloatField` - Rating given to the vendor for this PO (nullable).
- **issue_date**: `DateTimeField` - Timestamp when the PO was issued to the vendor.
- **acknowledgment_date**: `DateTimeField`, nullable - Timestamp when the vendor acknowledged the PO.

### Historical Performance Model
Optionally stores historical data on vendor performance for trend analysis.
- **vendor**: `ForeignKey` - Link to the Vendor model.
- **date**: `DateTimeField` - Date of the performance record.
- **on_time_delivery_rate**: `FloatField` - Historical record of the on-time delivery rate.
- **quality_rating_avg**: `FloatField` - Historical record of the quality rating average.
- **average_response_time**: `FloatField` - Historical record of the average response time.
- **fulfillment_rate**: `FloatField` - Historical record of the fulfillment rate.

## Backend Logic for Performance Metrics

- **On-Time Delivery Rate**: Calculated each time a PO status changes to 'completed'. Logic: Count the number of completed POs delivered on or before the delivery_date and divide by the total number of completed POs for that vendor.
- **Quality Rating Average**: Updated upon the completion of each PO where a quality_rating is provided. Logic: Calculate the average of all quality_rating values for completed POs of the vendor.
- **Average Response Time**: Calculated each time a PO is acknowledged by the vendor. Logic: Compute the time difference between issue_date and acknowledgment_date for each PO, then find the average of these times for all POs of the vendor.
- **Fulfilment Rate**: Calculated upon any change in PO status. Logic: Divide the number of successfully fulfilled POs (status 'completed' without issues) by the total number of POs issued to the vendor.

## API Routes

### Vendor Profile Management
- **POST** `/api/vendors/`: Create a new vendor.
- **GET** `/api/vendors/`: List all vendors.
- **GET** `/api/vendors/{vendor_id}/`: Retrieve specific vendor details.
- **PUT** `/api/vendors/{vendor_id}/`: Update a vendor's details.
- **DELETE** `/api/vendors/{vendor_id}/`: Delete a vendor.

### Purchase Order Tracking
- **POST** `/api/purchase_orders/`: Create a purchase order.
- **GET** `/api/purchase_orders/`: List all purchase orders with an option to filter by vendor.
- **GET** `/api/purchase_orders/{po_id}/`: Retrieve details of a specific purchase order.
- **PUT** `/api/purchase_orders/{po_id}/`: Update a purchase order.
- **DELETE** `/api/purchase_orders/{po_id}/`: Delete a purchase order.

### Vendor Performance Evaluation
- **GET** `/api/vendors/{vendor_id}/performance`: Retrieve a vendor's performance metrics.


