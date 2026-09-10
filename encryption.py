# -*- coding: utf-8 -*-
"""
نظام التشفير الآمن
Secure Encryption Module - Uses Fernet (AES-based encryption)
"""

import os
import logging
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from config import ENCRYPTION_CONFIG

logger = logging.getLogger(__name__)


class EncryptionManager:
    """مدير التشفير الآمن / Secure Encryption Manager"""
    
    def __init__(self):
        self.key_file = Path(ENCRYPTION_CONFIG["key_file"])
        self.cipher = None
        self._initialize_encryption()
    
    def _initialize_encryption(self):
        """تهيئة نظام التشفير / Initialize encryption system"""
        try:
            if self.key_file.exists():
                # تحميل المفتاح الموجود / Load existing key
                with open(self.key_file, 'rb') as f:
                    key = f.read()
                logger.info("✓ مفتاح التشفير تم تحميله / Encryption key loaded")
            else:
                # إنشاء مفتاح جديد / Generate new key
                key = Fernet.generate_key()
                with open(self.key_file, 'wb') as f:
                    f.write(key)
                # تعيين أذونات آمنة / Set secure permissions
                os.chmod(self.key_file, 0o600)
                logger.info("✓ مفتاح تشفير جديد تم إنشاؤه / New encryption key generated")
            
            self.cipher = Fernet(key)
        except Exception as e:
            logger.error(f"✗ خطأ في التشفير: {e} / Encryption error: {e}")
            raise
    
    def encrypt_data(self, data: str) -> str:
        """
        تشفير البيانات
        Encrypt sensitive data (e.g., ID numbers)
        
        Args:
            data (str): البيانات غير المشفرة / Unencrypted data
            
        Returns:
            str: البيانات المشفرة / Encrypted data
        """
        try:
            if not data or not isinstance(data, str):
                raise ValueError("البيانات يجب أن تكون نصاً غير فارغ / Data must be non-empty string")
            
            encrypted_bytes = self.cipher.encrypt(data.encode())
            return encrypted_bytes.decode()
        except Exception as e:
            logger.error(f"✗ خطأ في تشفير البيانات: {e} / Data encryption error: {e}")
            raise
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """
        فك تشفير البيانات
        Decrypt sensitive data
        
        Args:
            encrypted_data (str): البيانات المشفرة / Encrypted data
            
        Returns:
            str: البيانات الأصلية / Original data
            
        Raises:
            ValueError: إذا كانت البيانات تالفة / If data is corrupted
        """
        try:
            if not encrypted_data or not isinstance(encrypted_data, str):
                raise ValueError("البيانات المشفرة غير صالحة / Invalid encrypted data")
            
            decrypted_bytes = self.cipher.decrypt(encrypted_data.encode())
            return decrypted_bytes.decode()
        except InvalidToken:
            logger.error("✗ فشل التحقق من البيانات المشفرة / Decryption token verification failed")
            raise ValueError("البيانات المشفرة تالفة أو غير صحيحة / Encrypted data is corrupted or invalid")
        except Exception as e:
            logger.error(f"✗ خطأ في فك التشفير: {e} / Data decryption error: {e}")
            raise


# إنشاء مثيل واحد من مدير التشفير / Create singleton instance
encryption_manager = EncryptionManager()
