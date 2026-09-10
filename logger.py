# -*- coding: utf-8 -*-
"""
نظام السجلات والتسجيل
Logging System Module
"""

import logging
import logging.handlers
from pathlib import Path
from config import LOGGING_CONFIG

def setup_logging():
    """تهيئة نظام السجلات / Setup logging system"""
    
    log_dir = Path(LOGGING_CONFIG["log_file"]).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # إنشاء المسجل الرئيسي / Create root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, LOGGING_CONFIG["level"]))
    
    # معالج الملف / File handler
    file_handler = logging.handlers.RotatingFileHandler(
        LOGGING_CONFIG["log_file"],
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, LOGGING_CONFIG["level"]))
    
    # معالج وحدة التحكم / Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # صيغة السجل / Log format
    formatter = logging.Formatter(LOGGING_CONFIG["format"])
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # إضافة المعالجات / Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info("=" * 60)
    logger.info("نظام السجلات تم تهيئته / Logging system initialized")
    logger.info("=" * 60)
    
    return logger


# تهيئة السجلات عند استيراد الوحدة / Initialize logging when module is imported
logger = setup_logging()
