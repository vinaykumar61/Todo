# To-Do List Application (Django + APIs + Templates)

## 📌 Project Overview
This is a **To-Do List web application** developed using **Python and Django**.  
The project provides **RESTful APIs for CRUD operations** and uses **HTML templates** for the user interface.

👉 **Important Note:**  
- Django **ORM is NOT used** (as per assignment instruction)  
- Database operations are handled using **MySQLdb (raw SQL queries)**  
- The project runs **only after activating the virtual environment**

---

## 🛠️ Tech Stack
- Python 3.8.10
- Django 4.0.2
- MySQL
- MySQLdb
- HTML, CSS
- JavaScript, jQuery
- DataTables (Server-side pagination)
- SweetAlert2

---

## 📂 Features
- Create Task
- View Task List (with pagination & search)
- Update Task (Modal popup)
- Delete Task
- REST APIs for all operations
- Server-side pagination using DataTables
- Proper exception handling
- CSRF protection

---

## ⚙️ Environment Setup (MANDATORY)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/vinaykumar61/Todo
cd todo_assignment



## Create Virtual Environment
python -m venv myenv

## Activate Virtual Environment in Windows command prompt 
myenv\Scripts\activate

## Install Dependencies
pip install -r requirements.txt


## Database Configuration

## Update database credentials in settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

CREATE DATABASE IF NOT EXISTS todo_db;

show databases;

use todo_db;

CREATE TABLE IF NOT EXISTS todo_db.tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

desc todo_db.tasks;

select * from todo_db.tasks;




## Run Server


python manage.py runserver


# Web Pages

# Task List Page
http://127.0.0.1:8000/


# Add Task Page
http://127.0.0.1:8000/add/