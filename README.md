PC-Build eStore
Overview
PC-Build eStore is a Django-based web application designed to streamline the process of selecting and purchasing components for custom PC builds. This project aims to provide users with an intuitive interface to browse, filter, and compare various PC parts, ensuring a seamless and informed shopping experience.

Features
User Authentication: Secure user registration, login, and profile management.
Product Catalog: Comprehensive listing of PC components, including processors, motherboards, RAM, GPUs, and more.
Advanced Filtering: Search and filter products based on categories, brands, specifications, and price.
Product Comparison: Compare different products side-by-side to make informed decisions.
Responsive Design: Mobile-friendly layout ensuring accessibility on various devices.
Shopping Cart: Add, remove, and manage items in the shopping cart with real-time updates.
Order Management: Track order history and order status.
Admin Panel: Manage products, categories, and user accounts with ease.
Technologies Used
Backend: Django, Django REST Framework
Frontend: HTML, CSS, JavaScript, Bootstrap
Database: MySql
Setup Instructions
Clone the Repository:

git clone https://github.com/itsHaarsh/pc-build-estore.git

cd pc-build-estore

*Install Dependencies:
pip install -r requirements.txt

Set Up the Database:
python manage.py makemigrations
python manage.py migrate

*Create a Superuser:
python manage.py createsuperuser

*Run the Development Server:
python manage.py runserver

*Access the Application:
Open your browser and navigate to "http://127.0.0.1:8000/"
