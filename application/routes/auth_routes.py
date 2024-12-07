from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from application.models import Staff, db
from application.utils import ResponseHelper
from datetime import timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

def create_default_admin():
    """
    Ensure the default administrator account exists.
    Staff ID: admin
    Password: password
    """
    admin = Staff.query.filter_by(staffID="admin").first()
    if not admin:
        hashed_password = generate_password_hash("password", method="pbkdf2:sha256")
        new_admin = Staff(
            staffID="admin",
            firstname="System",
            lastname="Administrator",
            email="admin@example.com",
            password=hashed_password,
            role="admin"
        )
        db.session.add(new_admin)
        db.session.commit()


@auth_bp.before_app_request
def initialize():
    """
    Hook to create the default admin on app startup.
    """
    create_default_admin()


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new staff member.
    ---
    tags:
      - auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - firstname
              - lastname
              - email
              - password
            properties:
              firstname:
                type: string
                example: John
              lastname:
                type: string
                example: Doe
              email:
                type: string
                example: john.doe@example.com
              password:
                type: string
                example: securepassword123
    responses:
      201:
        description: User registered successfully.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: User registered successfully
                data:
                  type: object
                  properties:
                    email:
                      type: string
                      example: john.doe@example.com
                    staffID:
                      type: string
                      example: 123456
      400:
        description: Email already exists.
    """
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if Staff.query.filter_by(email=email).first():
            return ResponseHelper.default_response("Email already exists", 400)

          # Use pbkdf2:sha256 as the hashing method
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_staff = Staff(
            firstname=data.get("firstname"),
            lastname=data.get("lastname"),
            email=email,
            password=hashed_password,
        )
        db.session.add(new_staff)
        db.session.commit()

        return ResponseHelper.default_response(
            "User registered successfully", 201, {"email": email,"staffID": new_staff.staffID}
        )
    except Exception as e:
        return ResponseHelper.default_response(f"Registration failed: {str(e)}", 500)


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user by staff ID and password.
    ---
    tags:
      - auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - staffID
              - password
            properties:
              staffID:
                type: string
                example: admin
              password:
                type: string
                example: password
    responses:
      200:
        description: Login successful.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Login successful
                data:
                  type: object
                  properties:
                    token:
                      type: string
                      example: jwt_token_here
                    role:
                      type: string
                      example: admin
      401:
        description: Invalid credentials.
      500:
        description: Internal server error.
    """
    try:
        data = request.get_json()
        staff_id = data.get("staffID")
        password = data.get("password")

        staff = Staff.query.filter_by(staffID=staff_id).first()

        if not staff or not check_password_hash(staff.password, password):
            return ResponseHelper.default_response("Invalid credentials", 401)

        token = create_access_token(identity={"id": staff.id, "role": staff.role}, expires_delta=timedelta(days=1))

        return ResponseHelper.default_response(
            "Login successful",
            200,
            {"token": token, "role": staff.role}
        )
    except Exception as e:
        return ResponseHelper.default_response(f"Login failed: {str(e)}", 500)