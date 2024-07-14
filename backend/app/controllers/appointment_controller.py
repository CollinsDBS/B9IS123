import logging
import traceback
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.models import Appointment
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

import datetime
appointment_bp = Blueprint('appointment', __name__)
# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@appointment_bp.route('/appointments', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required()
def create_appointment():
    try:
        data = request.get_json()
        service_type = data.get('serviceType')
        appointment_date = data.get('appointmentDate')
        
        if not service_type or not appointment_date:
            return jsonify({'message': 'Missing required fields'}), 400

        current_user = get_jwt_identity()

        new_appointment = Appointment(
            service_type=service_type,
            appointment_date=datetime.datetime.strptime(appointment_date,'%Y-%m-%dT%H:%M'),
            user_id=current_user['id']
        )
        db.session.add(new_appointment)
        db.session.commit()

        return jsonify({'message': 'Appointment created successfully'}), 201
    except Exception as e:
        logger.error("Error occurred during appointment creation: %s", e)
        logger.error(traceback.format_exc())  # Log the full traceback
        return jsonify({'message': 'Internal Server Error'}), 500

@appointment_bp.route('/appointments', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required()
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([appointment.to_dict() for appointment in appointments]), 200

@appointment_bp.route('/appointments/<int:id>', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required()
def get_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    return jsonify(appointment.to_dict()), 200

@appointment_bp.route('/appointments', methods=['POST'])
@jwt_required()
@cross_origin(supports_credentials=True)
def book_appointment():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_appointment = Appointment(
        user_id=current_user['id'],
        service_type=data.get('service_type'),
        appointment_date=data.get('appointment_date'),
        status='Pending'
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify(new_appointment.to_dict()), 201

@appointment_bp.route('/appointments/<int:id>', methods=['PUT'])
@jwt_required()
@cross_origin(supports_credentials=True)
def update_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    data = request.get_json()

    appointment.service_type = data.get('service_type', appointment.service_type)
    appointment.appointment_date = data.get('appointment_date', appointment.appointment_date)
    appointment.status = data.get('status', appointment.status)

    db.session.commit()
    return jsonify(appointment.to_dict()), 200

@appointment_bp.route('/appointments/<int:id>', methods=['DELETE'])
@jwt_required()
@cross_origin(supports_credentials=True)
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment deleted'}), 204
