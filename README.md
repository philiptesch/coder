# 🗂️ Coder Backend

![Django](https://img.shields.io/badge/Django-6.0+-green.svg)
![REST API](https://img.shields.io/badge/REST-API-blue.svg)
![License](https://img.shields.io/github/license/philiptesch/coder)

> **A modern Freelancer platform backend**, built with Django & Django REST Framework.  
> Provides a REST API for managing users, profiles, offers, orders, and reviews — ideal for integration with a frontend.

---

## 🚀 Features

- 🔐 User registration & authentication (Token-based)
- 📋 Full CRUD operations for:
  - Users & Profiles
  - Offers & OfferDetails
  - Orders
  - Reviews
- 👥 User roles: `customer` and `business`
- ⚙️ Admin panel available at `/admin/`
- 🧩 RESTful API structure for frontend integration
- 📸 Admin previews for media files

---

## ⚙️ Tech Stack

- 🐍 Python 3.x  
- 🧬 Django 6.0  
- 🔌 Django REST Framework  
- 🗄️ SQLite (default, configurable to PostgreSQL)  
- 🔐 Token Authentication (`rest_framework.authtoken`)

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/philiptesch/coder
cd coder
````

### 2️⃣ Create and activate a virtual environment
### Windows (PowerShell)
```bash
python -m venv env
.\env\Scripts\Activate.ps1   
```
### Windows (CMD)
```bash
python -m venv env
env\Scripts\activate.bat 
```
### macOS / Linux
```bash
python3 -m venv env
source env/bin/activate
````

###3️⃣ Install dependencies

```bash
pip install -r requirements.txt
````

### 4️⃣ Apply database migrations

```bash
python manage.py migrate
````

### 5️⃣ Create a superuser

```bash
python manage.py createsuperuser
````

###6️⃣ Run the development server

```bash
python manage.py runserver
````
API available at: http://127.0.0.1:8000/
Admin panel under: http://127.0.0.1:8000/admin/

###📖 API Overview

The API supports managing:

- 👤 Users & Profiles

- 🗂️ Offers & OfferDetails

-📝 Orders

- 💬 Reviews

Use Postman or your frontend to test the API.

###🧪 Sample Endpoints

Users

| Method | Endpoint         | Description         |
| ------ | ---------------- | ------------------- |
| POST   | `/api/register/` | Register a new user |
| POST   | `/api/login/`    | Login a user        |

Profiles

| Method | Endpoint                      | Description                    |
| ------ | ----------------------------- | ------------------------------ |
| GET    | `/api/profiles/{profile_id}/` | Retrieve a specific profile    |
| PATCH  | `/api/profiles/{profile_id}/` | Update profile                 |
| GET    | `/api/profiles/business/`     | Retrieve all business profiles |
| GET    | `/api/profiles/customer/`     | Retrieve all customer profiles |

Offers

| Method | Endpoint                              | Description                 |
| ------ | ------------------------------------- | --------------------------- |
| GET    | `/api/offers/`                        | Get all offers              |
| POST   | `/api/offers/`                        | Create a new offer          |
| GET    | `/api/offers/{offer_id}/`             | Retrieve a specific offer   |
| PATCH  | `/api/offers/{offer_id}/`             | Update a specific offer     |
| DELETE | `/api/offers/{offer_id}/`             | Delete a specific offer     |
| GET    | `/api/offerdetails/{offerdetail_id}/` | Get a specific offer detail |


Orders

| Method | Endpoint                                         | Description                           |
| ------ | ------------------------------------------------ | ------------------------------------- |
| GET    | `/api/orders/`                                   | List all orders                       |
| POST   | `/api/orders/`                                   | Create a new order                    |
| PATCH  | `/api/orders/{order_id}/`                        | Update a specific order               |
| DELETE | `/api/orders/{order_id}/`                        | Delete a specific order               |
| GET    | `/api/order-count/{business_user_id}/`           | Count active orders for a business    |
| GET    | `/api/completed-order-count/{business_user_id}/` | Count completed orders for a business |


Reviews

| Method | Endpoint                    | Description      |
| ------ | --------------------------- | ---------------- |
| GET    | `/api/reviews/`             | List all reviews |
| POST   | `/api/reviews/`             | Create a review  |
| PATCH  | `/api/reviews/{review_id}/` | Update a review  |
| DELETE | `/api/reviews/{review_id}/` | Delete a review  |



###📂 Project Structure
```
coder/
├── auth_app/          # Custom User model and authentication
│   ├── models.py      # User model
│   └── admin.py       # User admin registration
├── coder_app/         # Offers, OfferDetails, Orders, Reviews
│   ├── models.py
│   └── admin.py
├── profile_app/       # Profiles
│   ├── models.py
│   └── admin.py
├── coder/             # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

---

## 🤝 Contributing
Contributions are welcome!  
If you'd like to improve this project, open an issue or submit a pull request.


## 🤝 Contributing
Contributions are welcome!  
If you'd like to improve this project, open an issue or submit a pull request.

---

## 📄 License
MIT License © philiptesch 





