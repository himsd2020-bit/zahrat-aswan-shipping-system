# -*- coding: utf-8 -*-
"""
نظام زهرة أسوان للشحن والتخليص الجمركي
Zahrat Aswan Shipping & Customs Clearance Management System

الإصدار: 2.0.0
مؤلف: Zahrat Aswan Development Team
الترخيص: MIT
"""

import sys
import logging
from ui.main_window import main

# إعداد السجلات / Setup logging
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        logger.info("="*60)
        logger.info("🚀 نظام زهرة أسوان يبدأ التشغيل")
        logger.info("🚀 Zahrat Aswan System Starting Up")
        logger.info("="*60)
        
        # تشغيل التطبيق الرئيسي / Run main application
        main()
    except Exception as e:
        logger.critical(f"❌ خطأ حرج: {e} / Critical error: {e}", exc_info=True)
        sys.exit(1)
