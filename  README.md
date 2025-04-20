# Modular Platform - Django Project

This project is a modular architecture platform built with Django 4.2.  
It allows dynamic installation, upgrading, and uninstallation of modules through a user-friendly interface.

---

## 🚀 Features

- **Modular Engine:**
  - List available modules
  - Install / Upgrade / Uninstall modules dynamically

- **Example Module - Product Management:**
  - Manage products (CRUD)
  - Soft delete support
  - Dynamic database schema upgrade

- **Role-Based Access Control:**
  - Manager: Full access (Create, Read, Update, Delete)
  - User: Limited access (Create, Read, Update)
  - Public: Read-only access

- **Schema Versioning:**
  - Upgrade modules with dynamic schema changes (add/remove fields)

- **Error Handling:**
  - Landing pages become inaccessible if modules are uninstalled

---

## 📦 Project Structure

```
apps/
├── modular_engine/          # Core modular engine
└── product_management/      # Example module: Product Management
ERD.png                      # Entity Relationship Diagram
Flowchart.png                # System Flowchart
requirements.txt             # Project dependencies
README.md                    # This file
```

---

## 🛠️ Installation Guide

1. Clone the repository:

```bash
git clone <your-repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply initial migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (admin):

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

---

## 🧩 Usage

- Access the Modular Management page at:  
  [http://localhost:8000/module/](http://localhost:8000/module/)

- Install or upgrade modules directly through the interface.

- Access installed modules landing page, e.g., Product Management:  
  [http://localhost:8000/product/](http://localhost:8000/product/)

---

## 📑 Additional Notes

- Every change in models must be upgraded via the **Upgrade** button after migration scripts are ready.
- Soft delete is enabled for products; deleted items will not appear in listings but are preserved in the database.
- Dynamic field handling ensures no crash when database schema evolves.

---

## 📋 License

This project is for technical evaluation and learning purposes only.  
No license applied.