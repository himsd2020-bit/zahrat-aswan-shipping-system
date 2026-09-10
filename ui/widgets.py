# -*- coding: utf-8 -*-
"""
عناصر الواجهة الرسومية
GUI Widgets and Components
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from datetime import datetime
from database import db_manager
from models import ValidationRules, ShipmentModel
from config import PAYMENT_STATUSES, ID_TYPES
from utils import FormatUtils, CalculationUtils

logger = logging.getLogger(__name__)


class ShipmentFormFrame(ttk.Frame):
    """إطار نموذج إدخال الشحنة / Shipment input form frame"""
    
    def __init__(self, parent, on_save_callback=None):
        super().__init__(parent)
        self.on_save_callback = on_save_callback
        self.entries = {}
        self._create_widgets()
    
    def _create_widgets(self):
        """إنشاء عناصر النموذج / Create form widgets"""
        # إطار البيانات الأساسية / Basic info frame
        basic_frame = ttk.LabelFrame(self, text="البيانات الأساسية", padding=10)
        basic_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # صفوف الإدخال / Input rows
        fields_basic = [
            ("رقم البوليصة *", "waybill_number"),
            ("اسم المرسل *", "sender_name"),
            ("هاتف المرسل", "sender_phone"),
            ("اسم المرسل إليه *", "receiver_name"),
            ("هاتف المرسل إليه *", "receiver_phone"),
            ("البريد الإلكتروني", "receiver_email"),
            ("الوجهة النهائية *", "destination"),
        ]
        
        row = 0
        for label, field_name in fields_basic:
            ttk.Label(basic_frame, text=label).grid(row=row, column=1, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(basic_frame, width=40, justify="right")
            entry.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
            self.entries[field_name] = entry
            row += 1
        
        basic_frame.columnconfigure(0, weight=1)
        
        # إطار بيانات الهوية / Identity info frame
        identity_frame = ttk.LabelFrame(self, text="بيانات الهوية", padding=10)
        identity_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(identity_frame, text="نوع الهوية *").grid(row=0, column=1, sticky="e", padx=5, pady=5)
        self.entries["id_type"] = ttk.Combobox(
            identity_frame,
            values=[name for _, name in ID_TYPES],
            state="readonly",
            justify="right",
            width=38
        )
        self.entries["id_type"].grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        ttk.Label(identity_frame, text="رقم الهوية *").grid(row=1, column=1, sticky="e", padx=5, pady=5)
        self.entries["id_number"] = ttk.Entry(identity_frame, width=40, justify="right")
        self.entries["id_number"].grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        identity_frame.columnconfigure(0, weight=1)
        
        # إطار بيانات الشحن / Cargo info frame
        cargo_frame = ttk.LabelFrame(self, text="بيانات الشحن", padding=10)
        cargo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(cargo_frame, text="وصف الشحن").grid(row=0, column=1, sticky="ne", padx=5, pady=5)
        self.entries["cargo_description"] = tk.Text(cargo_frame, height=3, width=40, font=("Arial", 10))
        self.entries["cargo_description"].grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        ttk.Label(cargo_frame, text="الوزن (كج)").grid(row=1, column=1, sticky="e", padx=5, pady=5)
        self.entries["cargo_weight"] = ttk.Entry(cargo_frame, width=40, justify="right")
        self.entries["cargo_weight"].grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        ttk.Label(cargo_frame, text="الأبعاد").grid(row=2, column=1, sticky="e", padx=5, pady=5)
        self.entries["cargo_dimensions"] = ttk.Entry(cargo_frame, width=40, justify="right")
        self.entries["cargo_dimensions"].grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        cargo_frame.columnconfigure(0, weight=1)
        
        # إطار الحسابات / Financial info frame
        financial_frame = ttk.LabelFrame(self, text="الحسابات المالية", padding=10)
        financial_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(financial_frame, text="تكلفة الشحن ($) *").grid(row=0, column=1, sticky="e", padx=5, pady=5)
        self.entries["shipping_cost"] = ttk.Entry(financial_frame, width=40, justify="right")
        self.entries["shipping_cost"].grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.entries["shipping_cost"].bind("<KeyRelease>", self._update_total)
        
        ttk.Label(financial_frame, text="رسوم التخليص ($) *").grid(row=1, column=1, sticky="e", padx=5, pady=5)
        self.entries["customs_fees"] = ttk.Entry(financial_frame, width=40, justify="right")
        self.entries["customs_fees"].grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.entries["customs_fees"].bind("<KeyRelease>", self._update_total)
        
        ttk.Label(financial_frame, text="الإجمالي ($)").grid(row=2, column=1, sticky="e", padx=5, pady=5)
        self.total_label = ttk.Label(financial_frame, text="0.00", font=("Arial", 12, "bold"), foreground="#1a73e8")
        self.total_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        ttk.Label(financial_frame, text="حالة الدفع *").grid(row=3, column=1, sticky="e", padx=5, pady=5)
        self.entries["payment_status"] = ttk.Combobox(
            financial_frame,
            values=[name for _, name in PAYMENT_STATUSES],
            state="readonly",
            justify="right",
            width=38
        )
        self.entries["payment_status"].grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.entries["payment_status"].current(0)
        
        ttk.Label(financial_frame, text="ملاحظات").grid(row=4, column=1, sticky="ne", padx=5, pady=5)
        self.entries["notes"] = tk.Text(financial_frame, height=2, width=40, font=("Arial", 10))
        self.entries["notes"].grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        
        financial_frame.columnconfigure(0, weight=1)
        
        # أزرار الإجراء / Action buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="💾 حفظ الشحنة", command=self._save_shipment).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="🔄 مسح النموذج", command=self._clear_form).pack(side=tk.RIGHT, padx=5)
    
    def _update_total(self, event=None):
        """تحديث الإجمالي / Update total amount"""
        try:
            cost = float(self.entries["shipping_cost"].get() or 0)
            fees = float(self.entries["customs_fees"].get() or 0)
            total = CalculationUtils.calculate_total(cost, fees)
            self.total_label.config(text=FormatUtils.format_currency(total))
        except ValueError:
            self.total_label.config(text="0.00")
    
    def _save_shipment(self):
        """حفظ الشحنة / Save shipment"""
        try:
            # جمع البيانات / Collect data
            data = {}
            for field_name, entry in self.entries.items():
                if isinstance(entry, ttk.Entry) or isinstance(entry, ttk.Combobox):
                    data[field_name] = entry.get()
                elif isinstance(entry, tk.Text):
                    data[field_name] = entry.get("1.0", tk.END).strip()
            
            # التحقق من صحة البيانات / Validate data
            is_valid, errors = ValidationRules.validate_shipment(data)
            if not is_valid:
                messagebox.showerror("خطأ في التحقق", "\n".join(errors))
                return
            
            # تحويل التكاليف إلى أرقام / Convert costs to float
            data["shipping_cost"] = float(data["shipping_cost"])
            data["customs_fees"] = float(data["customs_fees"])
            
            # حفظ في قاعدة البيانات / Save to database
            shipment_id = db_manager.add_shipment(data)
            logger.info(f"✓ شحنة تم حفظها بنجاح: ID={shipment_id} / Shipment saved: ID={shipment_id}")
            
            # تنفيذ callback / Execute callback
            if self.on_save_callback:
                self.on_save_callback()
            
            # مسح النموذج / Clear form
            self._clear_form()
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل حفظ الشحنة: {e}")
            logger.error(f"✗ خطأ في حفظ الشحنة: {e} / Save shipment error: {e}")
    
    def _clear_form(self):
        """مسح النموذج / Clear form"""
        for entry in self.entries.values():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, tk.Text):
                entry.delete("1.0", tk.END)
            elif isinstance(entry, ttk.Combobox):
                entry.current(0)
        self.total_label.config(text="0.00")


class ShipmentTableFrame(ttk.Frame):
    """إطار جدول الشحنات / Shipment table frame"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()
        self.refresh()
    
    def _create_widgets(self):
        """إنشاء عناصر الجدول / Create table widgets"""
        # إطار البحث والتصفية / Search frame
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="بحث:").pack(side=tk.RIGHT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40, justify="right")
        search_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # جدول الشحنات / Shipments table
        columns = ("بوليصة", "المرسل", "المستلم", "الوجهة", "الإجمالي", "حالة الدفع", "التاريخ")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        
        # شريط التمرير / Scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
    
    def refresh(self):
        """تحديث الجدول / Refresh table"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            shipments = db_manager.get_all_shipments()
            for shipment in shipments:
                values = (
                    shipment["waybill_number"],
                    shipment["sender_name"][:20],
                    shipment["receiver_name"][:20],
                    shipment["destination"],
                    FormatUtils.format_currency(shipment["total_amount"]),
                    shipment["payment_status"],
                    FormatUtils.format_date(shipment["shipment_date"])
                )
                self.tree.insert("", tk.END, values=values)
        except Exception as e:
            logger.error(f"✗ خطأ في تحديث الجدول: {e} / Refresh table error: {e}")
    
    def _on_search(self, *args):
        """البحث في الجدول / Search in table"""
        search_term = self.search_var.get().lower()
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if any(search_term in str(val).lower() for val in values):
                self.tree.item(item, tags=())
            else:
                self.tree.item(item, tags=("hidden",))
        
        self.tree.tag_configure("hidden", foreground="gray")


class ReportFrame(ttk.Frame):
    """إطار التقارير / Reports frame"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()
        self.refresh()
    
    def _create_widgets(self):
        """إنشاء عناصر التقرير / Create report widgets"""
        # عنوان التقرير / Report title
        title_label = ttk.Label(
            self,
            text="📊 ملخص المالي الشامل",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=10)
        
        # إطار الإحصائيات / Statistics frame
        stats_frame = ttk.Frame(self)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # بطاقات الإحصائيات / Statistics cards
        self.stats_labels = {}
        stats_info = [
            ("total_shipments", "إجمالي الشحنات", "#4285f4"),
            ("total_revenue", "إجمالي الإيرادات", "#34a853"),
            ("paid_amount", "المبالغ المدفوعة", "#ea4335"),
            ("unpaid_amount", "المبالغ المعلقة", "#fbbc04"),
        ]
        
        for idx, (key, label, color) in enumerate(stats_info):
            card = self._create_stat_card(stats_frame, label, color)
            card.grid(row=0, column=idx, padx=10, pady=10, sticky="ew")
            self.stats_labels[key] = card
        
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(2, weight=1)
        stats_frame.columnconfigure(3, weight=1)
    
    def _create_stat_card(self, parent, label, color):
        """إنشاء بطاقة إحصائية / Create statistics card"""
        card = tk.Frame(parent, bg=color, height=100, relief=tk.RAISED, bd=1)
        
        label_widget = tk.Label(
            card,
            text=label,
            bg=color,
            fg="white",
            font=("Arial", 10, "bold")
        )
        label_widget.pack(pady=5)
        
        value_widget = tk.Label(
            card,
            text="0.00",
            bg=color,
            fg="white",
            font=("Arial", 16, "bold")
        )
        value_widget.pack(pady=10)
        
        card._value_label = value_widget
        return card
    
    def refresh(self):
        """تحديث التقرير / Refresh report"""
        try:
            summary = db_manager.get_financial_summary()
            
            # تحديث البطاقات / Update cards
            self.stats_labels["total_shipments"]._value_label.config(
                text=str(summary.get("total_shipments", 0))
            )
            self.stats_labels["total_revenue"]._value_label.config(
                text=FormatUtils.format_currency(summary.get("total_revenue", 0))
            )
            self.stats_labels["paid_amount"]._value_label.config(
                text=FormatUtils.format_currency(summary.get("paid_amount", 0))
            )
            self.stats_labels["unpaid_amount"]._value_label.config(
                text=FormatUtils.format_currency(summary.get("unpaid_amount", 0))
            )
        except Exception as e:
            logger.error(f"✗ خطأ في تحديث التقرير: {e} / Refresh report error: {e}")
