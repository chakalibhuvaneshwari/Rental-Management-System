<<<<<<< HEAD
# 🏡 Rental Property Management System (Mini NoBroker)

A complete full-stack web application using Django, featuring a clean UI with role-based functionality for Tenants, Owners, and Admins.

## Features Included
- **Role-Based Users**: Color-themed dashboards. Tenant (Blue), Owner (Green).
- **Smart Search Engine**: Natural language parsing built into Django ORM.
- **AI Chatbot**: Floating widget with rule-based NLP using Ajax.
- **Maps**: Interactive Leaflet maps on property listings.
- **Complete Booking Workflow**: Tenants request -> Owners manage.
- **Wishlist & Messaging**: Save properties and contact owners directly.
- **Animations**: AOS scroll animations and Bootstrap 5 responsiveness.

## Setup Instructions

### Prerequisites
- Python 3.8+ installed
- Virtual Environment (recommended)

### Installation Steps

1. **Navigate to project directory**
   ```bash
   cd "EY Capstone Project(Rental)"
   ```

2. **(Optional) Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   The project depends on `django` and `pillow` for images.
   ```bash
   pip install django pillow
   ```

4. **Run migrations**
   (These might already be applied, but this creates the SQLite DB)
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   # Follow prompts. Give the user an 'ADMIN' role later in the backend or register normally.
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the App**
   Open your browser and visit `http://127.0.0.1:8000/`.

## Usage Demo
- Register one account as **Owner**. Add a property.
- Logout and register a second account as **Tenant**.
- Search for properties using the smart search bar e.g. "2BHK under 15000".
- Book a property, save to wishlist, and send a message to the owner.
- Test the chatbot on the bottom right of the screen.
=======
# Rental-Management-System
>>>>>>> 7a7869e1d15169d9b1ea43b90a1a6630688b90ae
