import os
import json
import random
from datetime import datetime, date
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_ARABIC_RESHAPER = True
except ImportError:
    HAS_ARABIC_RESHAPER = False


# ==========================================
# 1. DATA STRUCTURES & DATA DICTIONARIES
# ==========================================

governorates = {
    "Cairo": {
        "directorate": "مديرية أمن القاهرة (Cybercrime Directorate - Cairo)",
        "address": "باب الخلق / المقر الرئيسي بأكاديمية الشرطة بالعباسية",
        "hotline": "108", "phone": "0224065052", "whatsapp": "01080800080"
    },
    "Giza": {
        "directorate": "مديرية أمن الجيزة (Cybercrime Unit - Giza)",
        "address": "شارع مراد - الجيزة",
        "hotline": "108", "phone": "0235728888", "whatsapp": "01080800080"
    },
    "Qalyubia": {
        "directorate": "مديرية أمن القليوبية (Cybercrime Unit - Qalyubia)",
        "address": "بنها - بجوار محطة القطار",
        "hotline": "108", "phone": "0133222300", "whatsapp": "01080800080"
    },
    "Alexandria": {
        "directorate": "مديرية أمن الإسكندرية (Cybercrime Unit - Alexandria)",
        "address": "سموحة - الإسكندرية",
        "hotline": "108", "phone": "034255555", "whatsapp": "01080800080"
    },
    "Port Said": {
        "directorate": "مديرية أمن بورسعيد (Cybercrime Unit - Port Said)",
        "address": "حي المناخ - بورسعيد",
        "hotline": "108", "phone": "0663222400", "whatsapp": "01080800080"
    },
    "Suez": {
        "directorate": "مديرية أمن السويس (Cybercrime Unit - Suez)",
        "address": "حي السويس",
        "hotline": "108", "phone": "0623333300", "whatsapp": "01080800080"
    },
    "Ismailia": {
        "directorate": "مديرية أمن الإسماعيلية (Cybercrime Unit - Ismailia)",
        "address": "شارع شبين الكوم - الإسماعيلية",
        "hotline": "108", "phone": "0643322100", "whatsapp": "01080800080"
    },
    "Sharqia": {
        "directorate": "مديرية أمن الشرقية (Cybercrime Unit - Sharqia)",
        "address": "الزقازيق - شارع الجلاء",
        "hotline": "108", "phone": "0552302300", "whatsapp": "01080800080"
    },
    "Dakahlia": {
        "directorate": "مديرية أمن الدقهلية (Cybercrime Unit - Dakahlia)",
        "address": "المنصورة - المشاية السفلية",
        "hotline": "108", "phone": "0502255300", "whatsapp": "01080800080"
    },
    "Gharbia": {
        "directorate": "مديرية أمن الغربية (Cybercrime Unit - Gharbia)",
        "address": "طنطا - أول طريق شوبر",
        "hotline": "108", "phone": "0403334500", "whatsapp": "01080800080"
    },
    "Menofia": {
        "directorate": "مديرية أمن المنوفية (Cybercrime Unit - Menofia)",
        "address": "شبين الكوم - مجمع المصالح",
        "hotline": "108", "phone": "0482223400", "whatsapp": "01080800080"
    },
    "Beheira": {
        "directorate": "مديرية أمن البحيرة (Cybercrime Unit - Beheira)",
        "address": "دمنهور - ميدان المحطة",
        "hotline": "108", "phone": "0453316200", "whatsapp": "01080800080"
    },
    "Kafr El-Sheikh": {
        "directorate": "مديرية أمن كفر الشيخ (Cybercrime Unit - Kafr El-Sheikh)",
        "address": "كفر الشيخ - شارع الخليفة المأمون",
        "hotline": "108", "phone": "0473233200", "whatsapp": "01080800080"
    },
    "Damietta": {
        "directorate": "مديرية أمن دمياط (Cybercrime Unit - Damietta)",
        "address": "دمياط - شارع التحرير",
        "hotline": "108", "phone": "0572224000", "whatsapp": "01080800080"
    },
    "Beni Suef": {
        "directorate": "مديرية أمن بني سويف (Cybercrime Unit - Beni Suef)",
        "address": "شارع كورنيش النيل - بني سويف",
        "hotline": "108", "phone": "0822322300", "whatsapp": "01080800080"
    },
    "Faiyum": {
        "directorate": "مديرية أمن الفيوم (Cybercrime Unit - Faiyum)",
        "address": "الفيوم - شارع المحطة",
        "hotline": "108", "phone": "0846342200", "whatsapp": "01080800080"
    },
    "Minya": {
        "directorate": "مديرية أمن المنيا (Cybercrime Unit - Minya)",
        "address": "المنيا - كورنيش النيل",
        "hotline": "108", "phone": "0862362500", "whatsapp": "01080800080"
    },
    "Asyut": {
        "directorate": "مديرية أمن أسيوط (Cybercrime Unit - Asyut)",
        "address": "أسيوط - ميدان المجذوب",
        "hotline": "108", "phone": "0882334000", "whatsapp": "01080800080"
    },
    "Sohag": {
        "directorate": "مديرية أمن سوهاج (Cybercrime Unit - Sohag)",
        "address": "سوهاج - شارع الجمهورية",
        "hotline": "108", "phone": "0932322200", "whatsapp": "01080800080"
    },
    "Qena": {
        "directorate": "مديرية أمن قنا (Cybercrime Unit - Qena)",
        "address": "قنا - ميدان الساعة",
        "hotline": "108", "phone": "0963332400", "whatsapp": "01080800080"
    },
    "Luxor": {
        "directorate": "مديرية أمن الأقصر (Cybercrime Unit - Luxor)",
        "address": "الأقصر - شارع خالد بن الوليد",
        "hotline": "108", "phone": "0952372000", "whatsapp": "01080800080"
    },
    "Aswan": {
        "directorate": "مديرية أمن أسوان (Cybercrime Unit - Aswan)",
        "address": "أسوان - طريق الكورنيش",
        "hotline": "108", "phone": "0972303000", "whatsapp": "01080800080"
    },
    "Red Sea": {
        "directorate": "مديرية أمن البحر الأحمر (Cybercrime Unit - Red Sea)",
        "address": "الغردقة - شارع النصر",
        "hotline": "108", "phone": "0653546000", "whatsapp": "01080800080"
    },
    "Matrouh": {
        "directorate": "مديرية أمن مطروح (Cybercrime Unit - Matrouh)",
        "address": "مرسى مطروح - شارع الجلاء",
        "hotline": "108", "phone": "0464932000", "whatsapp": "01080800080"
    },
    "North Sinai": {
        "directorate": "مديرية أمن شمال سيناء (Cybercrime Unit - North Sinai)",
        "address": "العريش - شارع الفاتح",
        "hotline": "108", "phone": "0683350000", "whatsapp": "01080800080"
    },
    "South Sinai": {
        "directorate": "مديرية أمن جنوب سيناء (Cybercrime Unit - South Sinai)",
        "address": "طور سيناء - المجمع الأمني",
        "hotline": "108", "phone": "0693770000", "whatsapp": "01080800080"
    },
    "New Valley": {
        "directorate": "مديرية أمن الوادي الجديد (Cybercrime Unit - New Valley)",
        "address": "الخارجة - شارع جمال عبد الناصر",
        "hotline": "108", "phone": "0922920000", "whatsapp": "01080800080"
    }
}

threat_type = [
    ("direct_threat", "Is there a direct threat of physical harm?"),
    ("private_content", "Are private photos or videos being used to threaten you?"),
    ("repeated_threat", "Has the threat been repeated multiple times?"),
    ("personal_info", "Does the extortionist know personal information like your address or workplace?"),
    ("financial_demand", "Is the extortionist demanding money or illegal favors?")
]

Risk_Scores = {
    "direct_threat": 3,
    "private_content": 3,
    "repeated_threat": 2,
    "personal_info": 2,
    "financial_demand": 2
}

evidence_types = [
    "Screenshot", "Message", "File", "Video", "Audio", "Link", "Other"
]

class Case:
    def __init__(self, victim_name, victim_phone, case_type):
        self.case_id = random.randint(1000, 9999)
        self.victim_name = victim_name
        self.victim_phone = victim_phone
        self.case_type = case_type
        self.case_status = "New"
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "case_id": self.case_id,
            "victim_name": self.victim_name,
            "victim_phone": self.victim_phone,
            "case_type": self.case_type,
            "case_status": self.case_status,
            "created_at": str(self.created_at)
        }

def fix_arabic(text):
    if HAS_ARABIC_RESHAPER:
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)
    return text


# ==========================================
# 2. AUTHORIZED PERSONAL LOGIN WINDOW
# ==========================================

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Aman Police System - Authorized Login")
        self.geometry("400x320")
        self.configure(bg="#0F172A")
        self.resizable(False, False)
        self.user_info = None

        tk.Label(self, text="AUTHORIZED PERSONAL LOGIN", font=("Segoe UI", 11, "bold"), bg="#0F172A", fg="#00B2FE").pack(pady=15)

        form_frame = tk.Frame(self, bg="#0F172A")
        form_frame.pack(padx=20, pady=5, fill="both")

        tk.Label(form_frame, text="Username:", bg="#0F172A", fg="#FFFFFF").grid(row=0, column=0, sticky="w", pady=8)
        self.ent_user = tk.Entry(form_frame, bg="#1E293B", fg="#FFFFFF", insertbackground="white", width=22)
        self.ent_user.grid(row=0, column=1, pady=8)

        tk.Label(form_frame, text="Password (Min 8 chars):", bg="#0F172A", fg="#FFFFFF").grid(row=1, column=0, sticky="w", pady=8)
        self.ent_pass = tk.Entry(form_frame, show="*", bg="#1E293B", fg="#FFFFFF", insertbackground="white", width=22)
        self.ent_pass.grid(row=1, column=1, pady=8)

        tk.Label(form_frame, text="National ID:", bg="#0F172A", fg="#FFFFFF").grid(row=2, column=0, sticky="w", pady=8)
        self.ent_nid = tk.Entry(form_frame, bg="#1E293B", fg="#FFFFFF", insertbackground="white", width=22)
        self.ent_nid.grid(row=2, column=1, pady=8)

        btn_login = tk.Button(self, text="Login to Secure System", command=self.attempt_login, bg="#00FF66", fg="#0F172A", font=("Segoe UI", 10, "bold"), pady=5)
        btn_login.pack(pady=18)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def attempt_login(self):
        username = self.ent_user.get().strip()
        password = self.ent_pass.get().strip()
        national_id = self.ent_nid.get().strip()

        if not username or not national_id:
            messagebox.showerror("Error", "Please enter username and National ID.")
            return

        if len(password) < 8:
            messagebox.showerror("Password Error", "Password must be at least 8 characters long. Please try again.")
            return

        self.user_info = {
            "username": username,
            "password": password,
            "national_id": national_id
        }
        messagebox.showinfo("Login Successful", f"Login Successful! Welcome User {username}")
        self.destroy()

    def on_close(self):
        if not self.user_info:
            self.master.destroy()


# ==========================================
# 3. MAIN GUI APPLICATION
# ==========================================

class AmanNetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aman Police System - Cybercrime Risk Assessment")
        self.root.geometry("880x880")
        self.root.configure(bg="#0F172A")

        self.evidence_list = []
        self.risk_vars = {}
        self.current_preview_photo = None
        self.officer_data = {"username": "Officer", "national_id": "N/A"}

        self.setup_styles()
        self.create_header()
        self.create_body()

        # Prompt Login Dialog
        self.root.withdraw()
        login_dlg = LoginWindow(self.root)
        self.root.wait_window(login_dlg)

        if login_dlg.user_info:
            self.officer_data = login_dlg.user_info
            self.lbl_officer_info.config(text=f"Logged User: {self.officer_data['username']} | National ID: {self.officer_data['national_id']}")
            self.root.deiconify()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#0F172A", borderwidth=0)
        style.configure("TNotebook.Tab", background="#1E293B", foreground="#94A3B8", padding=[12, 6], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#00B2FE")], foreground=[("selected", "#0F172A")])

        style.configure("TLabelframe", background="#1E293B", foreground="#00B2FE", borderwidth=1)
        style.configure("TLabelframe.Label", background="#1E293B", foreground="#00B2FE", font=("Segoe UI", 10, "bold"))

    def create_header(self):
        canvas = tk.Canvas(self.root, width=800, height=100, bg="#0F172A", highlightthickness=0)
        canvas.pack(pady=(10, 0))

        canvas.create_text(280, 40, text="Ama", font=("Segoe UI", 42, "bold"), fill="#00B2FE", anchor="e")

        shield_outer = [295, 10, 350, 10, 355, 45, 322, 78, 290, 45]
        shield_inner = [299, 14, 346, 14, 350, 43, 322, 73, 294, 43]
        canvas.create_polygon(shield_outer, fill="#00B2FE", outline="#00B2FE")
        canvas.create_polygon(shield_inner, fill="#0F172A", outline="#00B2FE", width=2)
        canvas.create_text(322, 41, text="N", font=("Segoe UI", 30, "bold"), fill="#00FF66")

        canvas.create_text(360, 40, text="et", font=("Segoe UI", 42, "bold"), fill="#FFFFFF", anchor="w")
        canvas.create_text(380, 88, text="AMAN POLICE SYSTEM - CYBER EXTORTER RISK ASSESSMENT", font=("Segoe UI", 8, "bold"), fill="#8B9AAE")

    def create_body(self):
        self.lbl_officer_info = tk.Label(self.root, text="", bg="#0F172A", fg="#00FF66", font=("Segoe UI", 9, "bold"))
        self.lbl_officer_info.pack(anchor="e", padx=25)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        self.tab_case = tk.Frame(self.notebook, bg="#1E293B")
        self.tab_risk = tk.Frame(self.notebook, bg="#1E293B")
        self.tab_evidence = tk.Frame(self.notebook, bg="#1E293B")
        self.tab_report = tk.Frame(self.notebook, bg="#1E293B")

        self.notebook.add(self.tab_case, text="1. Victim & Location")
        self.notebook.add(self.tab_risk, text="2. Risk Assessment")
        self.notebook.add(self.tab_evidence, text="3. Extorter & Evidence")
        self.notebook.add(self.tab_report, text="4. Report & Dispatch")

        self.build_case_tab()
        self.build_risk_tab()
        self.build_evidence_tab()
        self.build_report_tab()

    # --- STEP 1: VICTIM & LOCATION ---
    def build_case_tab(self):
        container = tk.Frame(self.tab_case, bg="#1E293B", padx=25, pady=20)
        container.pack(fill="both", expand=True)
        container.columnconfigure(1, weight=1)

        tk.Label(container, text="Victim Name:", bg="#1E293B", fg="#FFFFFF", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=10)
        self.entry_v_name = tk.Entry(container, font=("Segoe UI", 10), bg="#0F172A", fg="#FFFFFF", insertbackground="white")
        self.entry_v_name.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        tk.Label(container, text="Victim Phone Number:", bg="#1E293B", fg="#FFFFFF", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=10)
        self.entry_v_phone = tk.Entry(container, font=("Segoe UI", 10), bg="#0F172A", fg="#FFFFFF", insertbackground="white")
        self.entry_v_phone.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        tk.Label(container, text="Select Case Type:", bg="#1E293B", fg="#FFFFFF", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=10)
        self.case_type_cb = ttk.Combobox(container, font=("Segoe UI", 10), state="readonly", values=[
            "Financial Blackmail",
            "Emotional/Photo Blackmail",
            "Electronic Harassment",
            "Identity Theft",
            "Other"
        ])
        self.case_type_cb.current(0)
        self.case_type_cb.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

        tk.Label(container, text="Select Governorate Location:", bg="#1E293B", fg="#FFFFFF", font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", pady=10)
        self.gov_cb = ttk.Combobox(container, font=("Segoe UI", 10), state="readonly", values=list(governorates.keys()))
        self.gov_cb.current(0)
        self.gov_cb.grid(row=3, column=1, sticky="ew", padx=10, pady=10)
        self.gov_cb.bind("<<ComboboxSelected>>", self.update_gov_info)

        # --- Dynamic Governorate Details Display ---
        self.gov_info_frame = ttk.LabelFrame(container, text="Governorate Security Directorate Contact Details")
        self.gov_info_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=15)

        self.lbl_gov_directorate = tk.Label(self.gov_info_frame, text="", bg="#1E293B", fg="#00B2FE", font=("Segoe UI", 10, "bold"), anchor="w")
        self.lbl_gov_directorate.pack(fill="x", padx=10, pady=4)

        self.lbl_gov_address = tk.Label(self.gov_info_frame, text="", bg="#1E293B", fg="#FFFFFF", font=("Segoe UI", 9), anchor="w")
        self.lbl_gov_address.pack(fill="x", padx=10, pady=4)

        self.lbl_gov_phones = tk.Label(self.gov_info_frame, text="", bg="#1E293B", fg="#00FF66", font=("Segoe UI", 9, "bold"), anchor="w")
        self.lbl_gov_phones.pack(fill="x", padx=10, pady=6)

        # Initialize info
        self.update_gov_info()

    def update_gov_info(self, event=None):
        selected = self.gov_cb.get()
        data = governorates.get(selected, {})
        
        dir_text = fix_arabic(data.get("directorate", ""))
        addr_text = fix_arabic(data.get("address", ""))
        
        self.lbl_gov_directorate.config(text=f"Directorate: {dir_text}")
        self.lbl_gov_address.config(text=f"Address: {addr_text}")
        self.lbl_gov_phones.config(
            text=f"Hotline: {data.get('hotline', '')}   |   Landline: {data.get('phone', '')}   |   WhatsApp: {data.get('whatsapp', '')}"
        )

    # --- STEP 2: RISK ASSESSMENT ---
    def build_risk_tab(self):
        container = tk.Frame(self.tab_risk, bg="#1E293B", padx=25, pady=15)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Evaluate threat criteria (Yes/No):", bg="#1E293B", fg="#00B2FE", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 10))

        for key, question_text in threat_type:
            score = Risk_Scores[key]
            var = tk.BooleanVar(value=False)
            self.risk_vars[key] = (var, score)

            cb = tk.Checkbutton(container, text=f"{question_text} (+{score} pts)", variable=var,
                                command=self.update_risk_meter,
                                bg="#1E293B", fg="#FFFFFF", selectcolor="#0F172A",
                                activebackground="#1E293B", activeforeground="#00FF66",
                                font=("Segoe UI", 10))
            cb.pack(anchor="w", pady=5)

        meter_frame = ttk.LabelFrame(container, text="Risk Level Meter")
        meter_frame.pack(fill="x", pady=20, padx=5)

        self.meter_canvas = tk.Canvas(meter_frame, height=80, bg="#1E293B", highlightthickness=0)
        self.meter_canvas.pack(fill="x", padx=10, pady=5)

        self.lbl_risk_status = tk.Label(meter_frame, text="Total Score: 0 | Risk Level: Low", bg="#1E293B", fg="#22C55E", font=("Segoe UI", 10, "bold"))
        self.lbl_risk_status.pack(pady=(0, 5))

        self.update_risk_meter()

    def update_risk_meter(self):
        total_score = sum(score for var, score in self.risk_vars.values() if var.get())
        self.meter_canvas.delete("all")

        x_start = 40
        y_top = 15
        bar_height = 20
        total_width = 580

        colors = [("#22C55E", "Low (<3)"), ("#EAB308", "Medium (3-4)"), ("#F97316", "High (5-7)"), ("#EF4444", "Critical (>=8)")]
        segment_w = total_width / 4

        for i, (color, label) in enumerate(colors):
            x1 = x_start + i * segment_w
            x2 = x1 + segment_w
            self.meter_canvas.create_rectangle(x1, y_top, x2, y_top + bar_height, fill=color, outline="#0F172A", width=2)
            self.meter_canvas.create_text((x1 + x2) / 2, y_top + bar_height + 12, text=label, fill="#94A3B8", font=("Segoe UI", 8, "bold"))

        ratio = min(total_score / 12.0, 1.0)
        pointer_x = x_start + (ratio * total_width)

        needle_pts = [pointer_x - 6, y_top - 8, pointer_x + 6, y_top - 8, pointer_x, y_top + 4]
        self.meter_canvas.create_polygon(needle_pts, fill="#FFFFFF", outline="#00B2FE")
        self.meter_canvas.create_line(pointer_x, y_top, pointer_x, y_top + bar_height, fill="#FFFFFF", width=3)

        if total_score >= 8:
            risk_level, color_code = "Critical", "#EF4444"
        elif total_score >= 5:
            risk_level, color_code = "High", "#F97316"
        elif total_score >= 3:
            risk_level, color_code = "Medium", "#EAB308"
        else:
            risk_level, color_code = "Low", "#22C55E"

        self.lbl_risk_status.config(text=f"Total Score: {total_score} / 12 | Risk Level: {risk_level}", fg=color_code)
    # --- STEP 3: EXTORTER & EVIDENCE INFORMATION ---
    def build_evidence_tab(self):
        container = tk.Frame(self.tab_evidence, bg="#1E293B", padx=20, pady=15)
        container.pack(fill="both", expand=True)

        # Extorter Info
        ext_frame = ttk.LabelFrame(container, text="Extorter Information")
        ext_frame.pack(fill="x", pady=5, padx=5)

        tk.Label(ext_frame, text="Extorter Name:", bg="#1E293B", fg="#FFFFFF").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_ext_name = tk.Entry(ext_frame, bg="#0F172A", fg="#FFFFFF", insertbackground="white")
        self.entry_ext_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ext_frame, text="Phone Number:", bg="#1E293B", fg="#FFFFFF").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_ext_phone = tk.Entry(ext_frame, bg="#0F172A", fg="#FFFFFF", insertbackground="white")
        self.entry_ext_phone.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(ext_frame, text="Profile Link:", bg="#1E293B", fg="#FFFFFF").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_ext_link = tk.Entry(ext_frame, bg="#0F172A", fg="#FFFFFF", insertbackground="white", width=42)
        self.entry_ext_link.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        # Evidence Details
        ev_frame = ttk.LabelFrame(container, text="Collect Evidence")
        ev_frame.pack(fill="x", pady=10, padx=5)

        inner_ev_frame = tk.Frame(ev_frame, bg="#1E293B")
        inner_ev_frame.pack(fill="both", expand=True, padx=5, pady=5)

        controls_box = tk.Frame(inner_ev_frame, bg="#1E293B")
        controls_box.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(controls_box, text="Evidence Type:", bg="#1E293B", fg="#FFFFFF").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ev_type_cb = ttk.Combobox(controls_box, values=evidence_types, state="readonly", width=18)
        self.ev_type_cb.current(0)
        self.ev_type_cb.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(controls_box, text="Description:", bg="#1E293B", fg="#FFFFFF").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_ev_desc = tk.Entry(controls_box, bg="#0F172A", fg="#FFFFFF", insertbackground="white", width=40)
        self.entry_ev_desc.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        btn_browse = tk.Button(controls_box, text="Browse File Path", command=self.browse_file, bg="#00B2FE", fg="#0F172A", font=("Segoe UI", 8, "bold"))
        btn_browse.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.lbl_file_path = tk.Label(controls_box, text="", bg="#1E293B", fg="#94A3B8", wraplength=400, justify="left")
        self.lbl_file_path.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        btn_add_ev = tk.Button(controls_box, text="Add Evidence", command=self.add_evidence_item, bg="#00FF66", fg="#0F172A", font=("Segoe UI", 9, "bold"))
        btn_add_ev.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="w")

        # ====== إضافة مربع المعاينة (Image Preview) ======
        preview_box = tk.LabelFrame(inner_ev_frame, text="Image Preview", bg="#0F172A", fg="#00B2FE")
        preview_box.pack(side="right", padx=10, pady=5)

        self.lbl_img_preview = tk.Label(preview_box, text="[ Preview ]", bg="#0F172A", fg="#64748B", width=18, height=6)
        self.lbl_img_preview.pack(padx=5, pady=5)
        # ==========================================

        self.ev_listbox = tk.Listbox(container, bg="#0F172A", fg="#FFFFFF", height=6)
        self.ev_listbox.pack(fill="x", padx=5, pady=5)
    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.lbl_file_path.config(text=filename)
            
            try:
                img = Image.open(filename)
                img.thumbnail((120, 90))
                self.current_preview_photo = ImageTk.PhotoImage(img)
                self.lbl_img_preview.config(image=self.current_preview_photo, text="", width=120, height=90)
            except Exception as e:
                print(f"Error: {e}")
                self.lbl_img_preview.config(text="[ Preview ]", width=18, height=6)

    def add_evidence_item(self):
        ev_type = self.ev_type_cb.get()
        desc = self.entry_ev_desc.get().strip()
        path = self.lbl_file_path.cget("text")

        if not desc:
            messagebox.showwarning("Warning", "Please enter evidence description.")
            return

        evidence = {
            "type_evidence": ev_type,
            "description": desc,
            "file_path": path,
            "evidence_time": str(datetime.now())
        }
        self.evidence_list.append(evidence)
        self.ev_listbox.insert(tk.END, f"{len(self.evidence_list)} - Type: {ev_type} | Description: {desc} | File: {path}")

        self.entry_ev_desc.delete(0, tk.END)
        self.lbl_file_path.config(text="")
        
        self.lbl_img_preview.config(image="", text="[ Preview ]", width=18, height=6)
        
        messagebox.showinfo("Success", "Evidence added successfully.")

    # --- STEP 4: REPORT & DISPATCH ---
    def build_report_tab(self):
        container = tk.Frame(self.tab_report, bg="#1E293B", padx=20, pady=15)
        container.pack(fill="both", expand=True)

        btn_box = tk.Frame(container, bg="#1E293B")
        btn_box.pack(fill="x", pady=5)

        btn_gen = tk.Button(btn_box, text="Generate Official Report", command=self.generate_report_action, bg="#00FF66", fg="#0F172A", font=("Segoe UI", 9, "bold"), pady=5)
        btn_gen.pack(side="left", fill="x", expand=True, padx=2)

        btn_sub = tk.Button(btn_box, text="Submit Simulation", command=self.submit_report_simulation_action, bg="#00B2FE", fg="#0F172A", font=("Segoe UI", 9, "bold"), pady=5)
        btn_sub.pack(side="left", fill="x", expand=True, padx=2)

        btn_guide = tk.Button(btn_box, text="Emergency Guidelines", command=self.show_emergency_guidelines_action, bg="#EAB308", fg="#0F172A", font=("Segoe UI", 9, "bold"), pady=5)
        btn_guide.pack(side="left", fill="x", expand=True, padx=2)

        self.report_text = tk.Text(container, bg="#0F172A", fg="#00B2FE", font=("Consolas", 9), wrap="word")
        self.report_text.pack(fill="both", expand=True, pady=10)

    def generate_report_action(self):
        v_name = self.entry_v_name.get().strip()
        v_phone = self.entry_v_phone.get().strip()

        if not v_name or not v_phone:
            messagebox.showerror("Error", "Please enter Victim Name and Victim Phone.")
            return

        case_obj = Case(v_name, v_phone, self.case_type_cb.get())

        total_score = sum(score for var, score in self.risk_vars.values() if var.get())
        if total_score >= 8:
            risk_level = "Critical"
        elif total_score >= 5:
            risk_level = "High"
        elif total_score >= 3:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        gov_name = self.gov_cb.get()
        gov_details = governorates[gov_name]

        directorate_fixed = fix_arabic(gov_details['directorate'])
        address_fixed = fix_arabic(gov_details['address'])

        evidence_str = ""
        if len(self.evidence_list) > 0:
            for idx, ev in enumerate(self.evidence_list, 1):
                evidence_str += f"{idx} - Type: {ev['type_evidence']} | Description: {ev['description']} | File: {ev['file_path']}\n"
        else:
            evidence_str = "No evidence attached.\n"

        now = datetime.now()

        report_content = f"""
====================================================
            Aman - OFFICIAL INCIDENT REPORT
====================================================
Date of Report: {date.today()}
Time of Report: {now.time().strftime('%H:%M:%S')}

[ CASE DETAILS ]
Case ID       : {case_obj.case_id}
Victim Name   : {case_obj.victim_name}
Victim Phone  : {case_obj.victim_phone}
Case Type     : {case_obj.case_type}
Current Status: {case_obj.case_status}

[ EXTORTER INFORMATION ]
Phone Number  : {self.entry_ext_phone.get().strip() or 'Not Found'}
Profile Link  : {self.entry_ext_link.get().strip() or 'Not Found'}

[ RISK ASSESSMENT ]
Risk Level    : {risk_level}
Risk Score    : {total_score} / 12

[ EVIDENCE COLLECTED ]
{evidence_str}
[ OFFICIAL DISPATCH LOCATION ]
Governorate   : {gov_name}
Directorate   : {directorate_fixed}
Address       : {address_fixed}
Hotline       : {gov_details['hotline']}
Landline      : {gov_details['phone']}
WhatsApp      : {gov_details['whatsapp']}
====================================================
"""
        self.report_text.delete("1.0", tk.END)
        self.report_text.insert(tk.END, report_content)

        # Save txt file
        filename = f"Police_Report_{case_obj.case_id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_content)

        # Save cases.json
        cases_file = "cases.json"
        existing = []
        if os.path.exists(cases_file):
            try:
                with open(cases_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = []

        existing.append(case_obj.to_dict())
        with open(cases_file, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=4)

        messagebox.showinfo("Success", f"Report saved successfully as: {filename}")

    def submit_report_simulation_action(self):
        steps = [
            "Preparing Report Data... Done!",
            "Encrypting Evidence Files... Done!",
            "Connecting to Secure Police Server... Done!",
            "Dispatching Report... Done!"
        ]
        for step in steps:
            messagebox.showinfo("Submission Progress", step)
        messagebox.showinfo("Submission Complete", "Report Submitted Successfully!")

    def show_emergency_guidelines_action(self):
        guide = """
==================================================
         IMPORTANT SAFETY GUIDELINES        
==================================================
1. DO NOT pay any money to the extorter. (It will not stop them).
2. DO NOT delete any chats, photos, or voice notes (They are your evidence).
3. Block the extorter immediately from all your accounts.
4. Inform your trusted family members or friends for support.

If you are in immediate danger, please contact:
Website: https://moi.gov.eg/
Hotline: 108
"""
        messagebox.showinfo("Emergency Guidelines", guide)


if __name__ == "__main__":
    root = tk.Tk()
    app = AmanNetApp(root)
    root.mainloop()