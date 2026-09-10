# -*- coding: utf-8 -*-
"""
نموذج البيانات والتحقق من الصحة
Data Models and Validation Module
"""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from config import VALIDATION_RULES, PAYMENT_STATUSES, ID_TYPES

logger_validation = []


@dataclass
class ShipmentModel:
    """نموذج بيانات الشحنة / Shipment Data Model"""
    waybill_number: str
    sender_name: str
    receiver_name: str
    receiver_phone: str
    id_type: str
    id_number: str
    destination: str
    shipping_cost: float
    customs_fees: float
    payment_status: str
    sender_phone: Optional[str] = None
    receiver_email: Optional[str] = None
    cargo_description: Optional[str] = None
    cargo_weight: Optional[float] = None
    cargo_dimensions: Optional[str] = None
    notes: Optional[str] = None
    
    def to_dict(self) -> dict:
        """تحويل النموذج إلى قاموس / Convert model to dictionary"""
        return {
            'waybill_number': self.waybill_number,
            'sender_name': self.sender_name,
            'sender_phone': self.sender_phone,
            'receiver_name': self.receiver_name,
            'receiver_phone': self.receiver_phone,
            'receiver_email': self.receiver_email,
            'id_type': self.id_type,
            'id_number': self.id_number,
            'cargo_description': self.cargo_description,
            'cargo_weight': self.cargo_weight,
            'cargo_dimensions': self.cargo_dimensions,
            'destination': self.destination,
            'shipping_cost': self.shipping_cost,
            'customs_fees': self.customs_fees,
            'payment_status': self.payment_status,
            'notes': self.notes,
        }


class ValidationRules:
    """قواعد التحقق من صحة البيانات / Data Validation Rules"""
    
    @staticmethod
    def validate_waybill(waybill: str) -> tuple[bool, str]:
        """التحقق من رقم البوليصة / Validate waybill number"""
        if not waybill or len(waybill) == 0:
            return False, "رقم البوليصة مطلوب / Waybill number is required"
        
        if not re.match(VALIDATION_RULES["waybill_pattern"], waybill):
            return False, "صيغة رقم البوليصة غير صحيحة (6-20 حرف/رقم) / Invalid waybill format (6-20 alphanumeric)"
        
        return True, "صحيح / Valid"
    
    @staticmethod
    def validate_phone(phone: str) -> tuple[bool, str]:
        """التحقق من رقم الهاتف / Validate phone number"""
        if not phone:
            return False, "رقم الهاتف مطلوب / Phone number is required"
        
        if not re.match(VALIDATION_RULES["phone_pattern"], phone):
            return False, "صيغة رقم الهاتف غير صحيحة / Invalid phone format (10-15 digits)"
        
        return True, "صحيح / Valid"
    
    @staticmethod
    def validate_email(email: str) -> tuple[bool, str]:
        """التحقق من البريد الإلكتروني / Validate email address"""
        if not email:
            return True, "صحيح / Valid"  # اختياري / Optional
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "صيغة البريد الإلكتروني غير صحيحة / Invalid email format"
        
        return True, "صحيح / Valid"
    
    @staticmethod
    def validate_cost(cost: float) -> tuple[bool, str]:
        """التحقق من تكلفة الشحن / Validate shipping cost"""
        try:
            cost_float = float(cost)
            if cost_float < VALIDATION_RULES["min_cost"]:
                return False, f"الحد الأدنى للتكلفة: {VALIDATION_RULES['min_cost']} / Minimum cost: {VALIDATION_RULES['min_cost']}"
            
            if cost_float > VALIDATION_RULES["max_cost"]:
                return False, f"الحد الأقصى للتكلفة: {VALIDATION_RULES['max_cost']} / Maximum cost: {VALIDATION_RULES['max_cost']}"
            
            return True, "صحيح / Valid"
        except ValueError:
            return False, "التكلفة يجب أن تكون رقماً / Cost must be a number"
    
    @staticmethod
    def validate_fees(fees: float) -> tuple[bool, str]:
        """التحقق من الرسوم / Validate customs fees"""
        try:
            fees_float = float(fees)
            if fees_float < VALIDATION_RULES["min_fees"]:
                return False, f"الحد الأدنى للرسوم: {VALIDATION_RULES['min_fees']} / Minimum fees: {VALIDATION_RULES['min_fees']}"
            
            if fees_float > VALIDATION_RULES["max_fees"]:
                return False, f"الحد الأقصى للرسوم: {VALIDATION_RULES['max_fees']} / Maximum fees: {VALIDATION_RULES['max_fees']}"
            
            return True, "صحيح / Valid"
        except ValueError:
            return False, "الرسوم يجب أن تكون رقماً / Fees must be a number"
    
    @staticmethod
    def validate_id_number(id_number: str, id_type: str) -> tuple[bool, str]:
        """التحقق من رقم الهوية / Validate ID number"""
        if not id_number:
            return False, "رقم الهوية مطلوب / ID number is required"
        
        if len(id_number) < 5:
            return False, "رقم الهوية قصير جداً / ID number is too short"
        
        return True, "صحيح / Valid"
    
    @staticmethod
    def validate_required_field(field: str, field_name: str) -> tuple[bool, str]:
        """التحقق من الحقول المطلوبة / Validate required fields"""
        if not field or (isinstance(field, str) and field.strip() == ""):
            return False, f"{field_name} مطلوب / {field_name} is required"
        
        return True, "صحيح / Valid"
    
    @staticmethod
    def validate_shipment(data: dict) -> tuple[bool, list]:
        """التحقق الشامل من بيانات الشحنة / Comprehensive shipment validation"""
        errors = []
        
        # التحقق من الحقول المطلوبة / Validate required fields
        required_fields = {
            'waybill_number': 'رقم البوليصة / Waybill Number',
            'sender_name': 'اسم المرسل / Sender Name',
            'receiver_name': 'اسم المرسل إليه / Receiver Name',
            'receiver_phone': 'هاتف المرسل إليه / Receiver Phone',
            'id_type': 'نوع الهوية / ID Type',
            'id_number': 'رقم الهوية / ID Number',
            'destination': 'الوجهة / Destination',
            'payment_status': 'حالة الدفع / Payment Status',
        }
        
        for field, label in required_fields.items():
            valid, msg = ValidationRules.validate_required_field(data.get(field, ''), label)
            if not valid:
                errors.append(msg)
        
        # التحقق من صيغ البيانات / Validate data formats
        if data.get('waybill_number'):
            valid, msg = ValidationRules.validate_waybill(data['waybill_number'])
            if not valid:
                errors.append(msg)
        
        if data.get('receiver_phone'):
            valid, msg = ValidationRules.validate_phone(data['receiver_phone'])
            if not valid:
                errors.append(msg)
        
        if data.get('sender_phone'):
            valid, msg = ValidationRules.validate_phone(data['sender_phone'])
            if not valid:
                errors.append(msg)
        
        if data.get('receiver_email'):
            valid, msg = ValidationRules.validate_email(data['receiver_email'])
            if not valid:
                errors.append(msg)
        
        if data.get('shipping_cost'):
            valid, msg = ValidationRules.validate_cost(data['shipping_cost'])
            if not valid:
                errors.append(msg)
        
        if data.get('customs_fees') is not None:
            valid, msg = ValidationRules.validate_fees(data['customs_fees'])
            if not valid:
                errors.append(msg)
        
        if data.get('id_number'):
            valid, msg = ValidationRules.validate_id_number(data['id_number'], data.get('id_type', ''))
            if not valid:
                errors.append(msg)
        
        return len(errors) == 0, errors
