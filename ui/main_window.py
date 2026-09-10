# -*- coding: utf-8 -*-
"""
نافذة التطبيق الرئيسية
Main Application Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from config import GUI_CONFIG
from database import db_manager
from models import ValidationRules, ShipmentModel
from ui.widgets import ShipmentFormFrame, ShipmentTableFrame, ReportFrame

logger = logging.getLogger(__name__)


class MainWindow:
    """النافذة الرئيسية للتطبيق / Main application window"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(GUI_CONFIG["title"])
        self.root.geometry(f"{GUI_CONFIG['window_width']}x{GUI_CONFIG['window_height']}")
        self.root.configure(bg="#f4f6f9")
        
        # تطبيق الستايل / Apply styling
        self._setup_styles()
        
        # إنشاء الواجهة / Create UI
        self._create_widgets()
        
        logger.info("✓ النافذة الرئيسية تم إنشاؤها / Main window created")
    
    def _setup_styles(self):
        """تهيئة الأنماط / Setup GUI styles"""
        style = ttk.Style()
        style.theme_use(GUI_CONFIG["theme"])
        
        # تخصيص الألوان والخطوط / Customize colors and fonts
        style.configure(
            "TLabel",
            font=(GUI_CONFIG["font_family"], GUI_CONFIG["font_size"]),
            background="#f4f6f9",
            anchor="right"
        )
        
        style.configure(
            "TButton",
            font=(GUI_CONFIG["font_family"], GUI_CONFIG["font_size"], "bold"),
            padding=8
        )
        
        style.map(
            "TButton",
            background=[("active", "#155cb4")],
            foreground=[("active", "white")]
        )
        
        style.configure(
            "Title.TLabel",
            font=(GUI_CONFIG["font_family"], 16, "bold"),
            background="#1a73e8",
            foreground="white"
        )
    
    def _create_widgets(self):
        """إنشاء عناصر الواجهة / Create UI widgets"""
        # شريط العنوان / Title bar
        title_frame = tk.Frame(self.root, bg="#1a73e8", height=60)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="🚚 " + GUI_CONFIG["title"],
            font=(GUI_CONFIG["font_family"], 16, "bold"),
            bg="#1a73e8",
            fg="white",
            pady=10
        )
        title_label.pack(side=tk.RIGHT, padx=20)
        
        # شريط القائمة / Menu bar
        self._create_menu_bar()
        
        # الإطار الرئيسي / Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إنشاء التبويبات / Create notebook tabs
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # التبويب الأول: إدخال الشحنات / Tab 1: New Shipment
        shipment_frame = ttk.Frame(notebook)
        notebook.add(shipment_frame, text="📦 إضافة شحنة جديدة")
        self.shipment_form = ShipmentFormFrame(shipment_frame, self.on_shipment_saved)
        
        # التبويب الثاني: جدول الشحنات / Tab 2: Shipments Table
        table_frame = ttk.Frame(notebook)
        notebook.add(table_frame, text="📋 جميع الشحنات")
        self.shipment_table = ShipmentTableFrame(table_frame)
        
        # التبويب الثالث: التقارير / Tab 3: Reports
        report_frame = ttk.Frame(notebook)
        notebook.add(report_frame, text="📊 التقارير والحسابات")
        self.report_section = ReportFrame(report_frame)
    
    def _create_menu_bar(self):
        """إنشاء شريط القائمة / Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # قائمة ملف / File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ملف", menu=file_menu)
        file_menu.add_command(label="تصدير إلى CSV", command=self.export_to_csv)
        file_menu.add_command(label="طباعة", command=self.print_shipments)
        file_menu.add_separator()
        file_menu.add_command(label="خروج", command=self.on_closing)
        
        # قائمة تحرير / Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="تحرير", menu=edit_menu)
        edit_menu.add_command(label="مسح البيانات", command=self.clear_all_data)
        edit_menu.add_command(label="إعدادات", command=self.show_settings)
        
        # قائمة مساعدة / Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="مساعدة", menu=help_menu)
        help_menu.add_command(label="حول البرنامج", command=self.show_about)
    
    def on_shipment_saved(self):
        """تحديث الجدول بعد حفظ شحنة / Refresh table after saving shipment"""
        self.shipment_table.refresh()
        self.report_section.refresh()
        messagebox.showinfo("نجاح", "تم حفظ الشحنة بنجاح!")
    
    def export_to_csv(self):
        """تصدير البيانات إلى CSV / Export data to CSV"""
        try:
            from utils import ExportUtils
            shipments = db_manager.get_all_shipments()
            if not shipments:
                messagebox.showwarning("تنبيه", "لا توجد بيانات للتصدير")
                return
            
            filename = ExportUtils.generate_filename("shipments")
            headers = list(shipments[0].keys())
            csv_content = ExportUtils.generate_csv_from_data(shipments, headers)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(csv_content)
            
            messagebox.showinfo("نجاح", f"تم التصدير إلى: {filename}")
            logger.info(f"✓ تم تصدير البيانات إلى {filename} / Data exported to {filename}")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل التصدير: {e}")
            logger.error(f"✗ خطأ في التصدير: {e} / Export error: {e}")
    
    def print_shipments(self):
        """طباعة الشحنات / Print shipments"""
        messagebox.showinfo("طباعة", "ميزة الطباعة قريباً...")
    
    def clear_all_data(self):
        """مسح جميع البيانات / Clear all data"""
        if messagebox.askyesno("تأكيد", "هل أنت متأكد من مسح جميع البيانات؟ هذا الإجراء لا يمكن التراجع عنه!"):
            messagebox.showinfo("قيد التطوير", "هذه الميزة قيد التطوير...")
    
    def show_settings(self):
        """عرض الإعدادات / Show settings"""
        messagebox.showinfo("الإعدادات", "صفحة الإعدادات قيد التطوير...")
    
    def show_about(self):
        """عرض معلومات البرنامج / Show about dialog"""
        about_text = f"""
{GUI_CONFIG['title']}
نسخة: 2.0.0

نظام إدارة شامل للشحن والتخليص الجمركي
يتضمن:
✓ إدارة الشحنات
✓ تشفير آمن للبيانات
✓ التقارير المالية
✓ إدارة الفروع

© 2024 جميع الحقوق محفوظة
        """
        messagebox.showinfo("حول البرنامج", about_text)
    
    def on_closing(self):
        """إغلاق التطبيق / Close application"""
        if messagebox.askokcancel("خروج", "هل تريد إغلاق البرنامج؟"):
            db_manager.close_connection()
            self.root.destroy()
            logger.info("✓ البرنامج تم إغلاقه / Application closed")


def main():
    """نقطة البداية الرئيسية / Main entry point"""
    root = tk.Tk()
    app = MainWindow(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
