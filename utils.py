# -*- coding: utf-8 -*-
"""
الأدوات المساعدة والدوال العامة
Utility Functions and Helpers
"""

import re
from datetime import datetime
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class FormatUtils:
    """أدوات التنسيق / Formatting utilities"""
    
    @staticmethod
    def format_currency(amount: float, currency: str = "$") -> str:
        """تنسيق العملة / Format currency"""
        try:
            return f"{currency}{amount:,.2f}"
        except (ValueError, TypeError):
            return f"{currency}0.00"
    
    @staticmethod
    def format_date(date_obj: Optional[datetime], fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        """تنسيق التاريخ / Format date"""
        if isinstance(date_obj, str):
            return date_obj
        if date_obj:
            return date_obj.strftime(fmt)
        return "-"
    
    @staticmethod
    def format_phone(phone: str) -> str:
        """تنسيق رقم الهاتف / Format phone number"""
        # إزالة الأحرف غير الرقمية / Remove non-numeric characters
        digits = re.sub(r'\D', '', phone)
        if len(digits) == 10:
            return f"+1 ({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        return phone
    
    @staticmethod
    def truncate_text(text: str, length: int = 50) -> str:
        """اختصار النص / Truncate text"""
        if len(text) > length:
            return text[:length] + "..."
        return text


class SearchUtils:
    """أدوات البحث / Search utilities"""
    
    @staticmethod
    def filter_list(items: list, search_term: str, keys: list) -> list:
        """تصفية قائمة البيانات / Filter list of items"""
        if not search_term:
            return items
        
        search_lower = search_term.lower()
        filtered = []
        
        for item in items:
            for key in keys:
                if isinstance(item, dict):
                    value = str(item.get(key, "")).lower()
                else:
                    value = str(getattr(item, key, "")).lower()
                
                if search_lower in value:
                    filtered.append(item)
                    break
        
        return filtered


class ValidationUtils:
    """أدوات التحقق / Validation utilities"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """التحقق من صحة البريد الإلكتروني / Validate email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """التحقق من صحة رقم الهاتف / Validate phone"""
        pattern = r'^\+?[0-9]{10,15}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def is_valid_waybill(waybill: str) -> bool:
        """التحقق من صحة رقم البوليصة / Validate waybill"""
        pattern = r'^[A-Z0-9\-]{6,20}$'
        return re.match(pattern, waybill) is not None


class CalculationUtils:
    """أدوات الحسابات / Calculation utilities"""
    
    @staticmethod
    def calculate_total(shipping_cost: float, customs_fees: float) -> float:
        """حساب الإجمالي / Calculate total amount"""
        try:
            return float(shipping_cost) + float(customs_fees)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def calculate_profit_margin(cost: float, selling_price: float) -> float:
        """حساب هامش الربح / Calculate profit margin"""
        if cost == 0:
            return 0.0
        return ((selling_price - cost) / cost) * 100
    
    @staticmethod
    def round_currency(amount: float, decimals: int = 2) -> float:
        """تقريب العملة / Round currency to decimals"""
        return round(float(amount), decimals)


class ExportUtils:
    """أدوات التصدير / Export utilities"""
    
    @staticmethod
    def generate_csv_from_data(data: list, headers: list) -> str:
        """توليد ملف CSV / Generate CSV content"""
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()
    
    @staticmethod
    def generate_filename(prefix: str, extension: str = "csv") -> str:
        """توليد اسم ملف / Generate filename with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"
