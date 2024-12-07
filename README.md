# Leave Management API

The Leave Management API is a backend service that provides functionality for managing staff leave requests and records. The system includes authentication, role-based access control, staff record management, and leave request workflows. This API is designed to be consumed by a frontend application.

---

## **Features**

- User registration with hashed passwords.
- Login with JWT token generation.
- Protected routes using JWT.
- Role-based user management (e.g., customer, administrator).
- Swagger UI for API documentation.

### **Authentication**

- JWT-based authentication.
- Admins and staff login using staffID and password.

### **Role-Based Access Control**

- Admins can manage staff records (add, edit, delete).
- Staff can view their leave requests.

### **Leave Request Workflow**

- Staff can request leave.
- Line managers can approve or reject leave requests.

### **API Documentation**

- Fully documented using OpenAPI 3.0 and served via Swagger UI.



## **Installation**

- git clone https://github.com/your-repository/leave-management-api.git
- cd leave-management-api
- python -m venv venv
- source venv/bin/activate  # On Windows: venv\Scripts\activate
- pip install -r requirements.txt
- 
---

## **Getting Started**

### **Prerequisites**

Make sure you have the following installed:
- Python 3.9 or later
- pip (Python package manager)

---

### **Setup Instructions**

#### **Step 1: Clone the Repository**
```bash
git clone https://github.com/Nwoko-Repo/swe242025-team3.git
cd swe242025-team3

#### **Step 2: Set up a virtual Environment**
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
flask db upgrade
flask run


The app will start on http://localhost:5000.
Swagger UI is available at http://localhost:5000/swagger.

