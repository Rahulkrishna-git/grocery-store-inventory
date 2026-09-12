# Grocery Store Inventory Management System

A web-based Grocery Store Inventory Management System developed using Flask and SQLite.

## Features

- Add new products
- Edit existing products
- Delete products
- Track stock quantities
- Low-stock detection
- Out-of-stock detection
- Search products by name, category, and barcode
- Barcode scanning using the device camera
- Product details page
- Inventory reports
- Category-wise inventory report
- Total inventory value calculation
- Responsive and professional user interface

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML5
- CSS3
- JavaScript
- HTML5 QR Code library

## Project Structure

```text
grocery_inventory/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── static/
│   └── style.css
│
└── templates/
    ├── index.html
    ├── add_product.html
    ├── edit_product.html
    ├── view_product.html
    └── reports.html
