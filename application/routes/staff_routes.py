from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.models import Staff, db
from application.utils import ResponseHelper

staff_bp = Blueprint("staff", __name__, url_prefix="/staff")


def is_admin():
    """Helper function to check if the current user is an administrator."""
    current_user = get_jwt_identity()
    staff = Staff.query.filter_by(email=current_user).first()
    return staff and staff.role == "admin"


@staff_bp.route("/add", methods=["POST"])
@jwt_required()
def add_staff():
    """
    Add a new staff member.
    ---
    tags:
      - staff
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
              - lineManagerID
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
              lineManagerID:
                type: string
                example: 123456
    responses:
      201:
        description: Staff added successfully.
      403:
        description: Access denied.
    """
    if not is_admin():
        return ResponseHelper.default_response("Access denied", 403)

    try:
        data = request.get_json()
        email = data.get("email")

        if Staff.query.filter_by(email=email).first():
            return ResponseHelper.default_response("Email already exists", 400)

        new_staff = Staff(
            firstname=data.get("firstname"),
            lastname=data.get("lastname"),
            email=email,
            lineManagerID=data.get("lineManagerID"),
            leaveBalances=data.get("leaveBalances", {
                'sick_leave': 10,
                'exam_leave': 5,
                'annual_leave': 20,
                'compassionate_leave': 0,
            })
        )
        db.session.add(new_staff)
        db.session.commit()

        return ResponseHelper.default_response(
            "Staff added successfully", 201, {"staffID": new_staff.staffID}
        )
    except Exception as e:
        return ResponseHelper.default_response(f"Failed to add staff: {str(e)}", 500)


@staff_bp.route("/edit/<staff_id>", methods=["PATCH"])
@jwt_required()
def edit_staff(staff_id):
    """
    Edit an existing staff record.
    ---
    tags:
      - staff
    parameters:
      - name: staff_id
        in: path
        required: true
        description: The staff ID of the record to edit.
        schema:
          type: string
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              firstname:
                type: string
              lastname:
                type: string
              email:
                type: string
              lineManagerID:
                type: string
              leaveBalances:
                type: object
                example:
                  sick_leave: 8
                  exam_leave: 4
                  annual_leave: 18
                  compassionate_leave: 0
    responses:
      200:
        description: Staff record updated successfully.
      404:
        description: Staff not found.
      403:
        description: Access denied.
    """
    if not is_admin():
        return ResponseHelper.default_response("Access denied", 403)

    try:
        staff = Staff.query.filter_by(staffID=staff_id).first()

        if not staff:
            return ResponseHelper.default_response("Staff not found", 404)

        data = request.get_json()
        staff.firstname = data.get("firstname", staff.firstname)
        staff.lastname = data.get("lastname", staff.lastname)
        staff.email = data.get("email", staff.email)
        staff.lineManagerID = data.get("lineManagerID", staff.lineManagerID)
        staff.leaveBalances = data.get("leaveBalances", staff.leaveBalances)

        db.session.commit()
        return ResponseHelper.default_response("Staff record updated successfully", 200)
    except Exception as e:
        return ResponseHelper.default_response(f"Failed to update staff: {str(e)}", 500)


@staff_bp.route("/delete/<staff_id>", methods=["DELETE"])
@jwt_required()
def delete_staff(staff_id):
    """
    Delete a staff record.
    ---
    tags:
      - staff
    parameters:
      - name: staff_id
        in: path
        required: true
        description: The staff ID of the record to delete.
        schema:
          type: string
    responses:
      200:
        description: Staff record deleted successfully.
      404:
        description: Staff not found.
      403:
        description: Access denied.
    """
    if not is_admin():
        return ResponseHelper.default_response("Access denied", 403)

    try:
        staff = Staff.query.filter_by(staffID=staff_id).first()

        if not staff:
            return ResponseHelper.default_response("Staff not found", 404)

        db.session.delete(staff)
        db.session.commit()
        return ResponseHelper.default_response("Staff record deleted successfully", 200)
    except Exception as e:
        return ResponseHelper.default_response(f"Failed to delete staff: {str(e)}", 500)
