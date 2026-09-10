# 🚚 نظام زهرة أسوان للشحن والتخليص الجمركي
## Zahrat Aswan Shipping & Customs Clearance Management System

### الميزات الرئيسية | Key Features

✅ **إدارة الشحنات** - Shipment Management
- إضافة وتحرير وحذف الشحنات
- تتبع حالة الشحنات
- إدارة بيانات المرسل والمستقبل

✅ **الأمان والتشفير** - Security & Encryption
- تشفير آمن للبيانات الحساسة (أرقام الهوية)
- استخدام تشفير Fernet (AES)
- حماية الخصوصية والامتثال للقوانين

✅ **الحسابات المالية** - Financial Management
- حساب التكاليف التلقائي
- رسوم التخليص الجمركي
- تتبع حالات الدفع
- التقارير المالية الشاملة

✅ **التقارير والإحصائيات** - Reports & Analytics
- ملخص مالي شامل
- إحصائيات الشحنات
- تصدير البيانات إلى CSV
- رسوم بيانية وتحليلات

✅ **التكامل مع الفروع** - Branch Management
- دعم عمل متعدد الفروع
- إدارة موحدة للبيانات
- تقارير شاملة لكل فرع

---

### متطلبات التشغيل | Requirements

```bash
Python 3.8+
Tkinter (عادة مدرج مع Python / Usually included with Python)
cryptography>=41.0.7
Pillow>=10.1.0
pytz>=2023.3
```

### التثبيت | Installation

1. **استنساخ المستودع** | Clone the repository
```bash
git clone https://github.com/himsd2020-bit/zahrat-aswan-shipping-system.git
cd zahrat-aswan-shipping-system
```

2. **إنشاء بيئة افتراضية** | Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # على Linux/Mac
# أو
venv\Scripts\activate  # على Windows
```

3. **تثبيت المتطلبات** | Install dependencies
```bash
pip install -r requirements.txt
```

### التشغيل | Running

```bash
python main.py
```

---

### هيكل المشروع | Project Structure

```
zahrat-aswan-shipping-system/
├── main.py              # نقطة البداية الرئيسية
├── config.py            # إعدادات النظام
├── database.py          # إدارة قاعدة البيانات
├── encryption.py        # نظام التشفير الآمن
├── models.py            # نماذج البيانات والتحقق
├── logger.py            # نظام السجلات
├── utils.py             # الدوال المساعدة
├── ui/
│   ├── main_window.py   # النافذة الرئيسية
│   └── widgets.py       # عناصر الواجهة
├── data/                # مجلد البيانات
│   └── logs/            # ملفات السجلات
├── requirements.txt     # المتطلبات
└── README.md            # هذا الملف
```

---

### الاستخدام الأساسي | Basic Usage

#### 1. إضافة شحنة جديدة | Add New Shipment
- انتقل إلى التبويب "📦 إضافة شحنة جديدة"
- أدخل البيانات المطلوبة (مع علامة *)
- اضغط "💾 حفظ الشحنة"

#### 2. عرض جميع الشحنات | View All Shipments
- انتقل إلى التبويب "📋 جميع الشحنات"
- استخدم شريط البحث للعثور على شحنات محددة

#### 3. عرض التقارير المالية | View Financial Reports
- انتقل إلى التبويب "📊 التقارير والحسابات"
- عرض الإحصائيات الشاملة

#### 4. تصدير البيانات | Export Data
- من القائمة "ملف" → "تصدير إلى CSV"
- سيتم حفظ الملف بصيغة CSV

---

### الميزات الأمنية | Security Features

🔒 **التشفير من الدرجة الأولى**
- استخدام Fernet (AES-128)
- مفاتيح تشفير آمنة
- حماية أرقام الهوية والجوازات

🔒 **حماية البيانات**
- قاعدة بيانات SQLite آمنة
- فحوصات التحقق من الصحة
- سجلات التدقيق الشاملة

🔒 **الامتثال القانوني**
- حماية بيانات العملاء
- توافق مع قوانين الخصوصية
- معايير الأمان الدولية

---

### الدعم والمساهمة | Support & Contribution

#### الإبلاغ عن مشاكل | Report Issues
- افتح issue جديد في [Issues](https://github.com/himsd2020-bit/zahrat-aswan-shipping-system/issues)
- وصف المشكلة بالتفصيل
- أرفق لقطات شاشة إذا أمكن

#### المساهمة | Contributing
1. Fork المشروع
2. أنشئ فرع جديد (`git checkout -b feature/AmazingFeature`)
3. قم بالتعديلات والتحسينات
4. اطلب دمج فرعك (Pull Request)

---

### الترخيص | License

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

---

### المؤلفون | Authors

- **فريق تطوير زهرة أسوان** - Zahrat Aswan Development Team
- **البريد الإلكتروني**: him.sd.2020@gmail.com

---

### شكر وتقدير | Acknowledgments

- شكر خاص لكل المساهمين والمستخدمين
- المكتبات المستخدمة: Tkinter, SQLite, Cryptography

---

### خارطة الطريق | Roadmap

- [ ] واجهة ويب (Web Interface)
- [ ] تطبيق الهاتف المحمول (Mobile App)
- [ ] نظام إدارة المستخدمين (User Management)
- [ ] تكامل الدفع الإلكتروني (Payment Integration)
- [ ] نظام الإشعارات (Notification System)
- [ ] تقارير متقدمة (Advanced Reports)

---

### الدعم والمساعدة | Help & Support

للحصول على المساعدة:
1. تحقق من [الأسئلة الشائعة](FAQ.md)
2. قراءة [التوثيق](DOCUMENTATION.md)
3. فتح issue في المستودع
4. تواصل عبر البريد الإلكتروني

---

**آخر تحديث**: 2026-09-10  
**الإصدار الحالي**: 2.0.0  
**الحالة**: 🟢 نشط ومدعوم / Active & Maintained
