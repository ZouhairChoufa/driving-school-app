# -*- coding: utf-8 -*-
import customtkinter
from tkinter import messagebox
from tkcalendar import Calendar
from database import get_admin_profile, update_admin_profile, get_employees, add_employee, delete_employee, get_employee_by_id, update_employee
from utils import handle_image_upload, get_image_for_card, validate_email, export_to_excel, validate_and_format_date

class AdminFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.arabic_font = app.font_arabic_bold
        self.font_card_details = customtkinter.CTkFont(family="Arial", size=15, weight="normal")

        self.selected_admin_image_path = None
        self.selected_employee_image_path = None
        self.selected_employee_image_path_edit = None
        
        self.grid_columnconfigure(0, weight=1)

        president_frame = customtkinter.CTkFrame(self, corner_radius=10)
        president_frame.grid(row=0, column=0, padx=40, pady=10, sticky="ew")
        president_frame.grid_columnconfigure(0, weight=1)
        self.create_president_section(president_frame)

        employee_frame = customtkinter.CTkFrame(self, corner_radius=10)
        employee_frame.grid(row=1, column=0, padx=40, pady=20, sticky="nsew")
        employee_frame.grid_columnconfigure(0, weight=1)
        self.create_employee_section(employee_frame)
        self.refresh_employee_list()
        
    def _open_calendar_popup(self, entry_widget):
        top = customtkinter.CTkToplevel(self)
        top.title("Select Date"); top.geometry("300x250"); top.transient(self.app); top.grab_set()
        cal = Calendar(top, selectmode='day', date_pattern='dd/mm/y')
        cal.pack(pady=10, padx=10, fill="both", expand=True)
        def select_date():
            entry_widget.delete(0, 'end'); entry_widget.insert(0, cal.get_date()); top.destroy()
        customtkinter.CTkButton(top, text="Select", command=select_date).pack(pady=10)

    def create_president_section(self, parent):
        customtkinter.CTkLabel(parent, text="President & Company Profile", font=customtkinter.CTkFont(size=18, weight="bold")).grid(row=0, column=0, pady=10, padx=10, sticky="w")
        
        self.president_card_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        self.president_card_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        
        self.edit_president_button = customtkinter.CTkButton(parent, text="Edit Profile", command=self.open_edit_president_window , font=customtkinter.CTkFont(size=16, weight="bold"))
        self.refresh_admin_profile()

    def refresh_admin_profile(self):
        for widget in self.president_card_frame.winfo_children(): widget.destroy()
        admin_data = get_admin_profile()
        if admin_data:
            self.create_employee_card(self.president_card_frame, admin_data, is_admin=True).pack(fill="x", expand=True)
            self.edit_president_button.grid(row=2, column=0, pady=10, padx=10)
        else:
            customtkinter.CTkLabel(self.president_card_frame, text="No profile found. Please add details.").pack()
            self.edit_president_button.grid_forget()
            self.open_edit_president_window(first_setup=True)

    def open_edit_president_window(self, first_setup=False):
        admin_data = get_admin_profile()
        if not admin_data and not first_setup:
            return

        edit_window = customtkinter.CTkToplevel(self)
        edit_window.title("Edit President & Company Profile")
        edit_window.geometry("450x700")
        edit_window.transient(self.app); edit_window.grab_set(); edit_window.focus()

        scroll_frame = customtkinter.CTkScrollableFrame(edit_window)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        def get_admin_data(index, default=""):
            return admin_data[index] if admin_data and len(admin_data) > index and admin_data[index] is not None else default

        fields_data = {
            ("First Name", "الإسم الشخصي"): ("first_name", get_admin_data(1)),
            ("Last Name", "الإسم العائلي"): ("last_name", get_admin_data(2)),
            ("Company Name", "إسم الشركة"): ("company_name", get_admin_data(6)),
            ("Company ID", "معرف الشركة"): ("company_id", get_admin_data(7)),
            ("Address", "العنوان"): ("address", get_admin_data(4)),
            ("Phone", "رقم الهاتف"): ("phone", get_admin_data(3)),
            ("Fax Phone Number", "رقم الفاكس"): ("fax", get_admin_data(9)),
            ("Email", "البريد الإلكتروني"): ("email", get_admin_data(10))
        }

        edit_entries = {}
        for (english_label, arabic_label), (key, val) in fields_data.items():
            label_frame = customtkinter.CTkFrame(scroll_frame, fg_color="transparent")
            label_frame.pack(fill="x", padx=10, pady=(10, 0))
            customtkinter.CTkLabel(label_frame, text=english_label).pack(side="left")
            customtkinter.CTkLabel(label_frame, text=arabic_label, font=self.arabic_font).pack(side="right")
            
            justify_side = 'right' if key in ['first_name', 'last_name', 'company_name', 'address'] else 'left'
            entry = customtkinter.CTkEntry(scroll_frame, justify=justify_side)
            entry.pack(fill="x", padx=10)
            entry.insert(0, val)
            edit_entries[key] = entry

        self.selected_admin_image_path = None
        image_button = customtkinter.CTkButton(scroll_frame, text="Upload New Image", command=lambda: self.handle_edit_president_image(image_preview))
        image_button.pack(pady=(20, 5))
        image_preview = customtkinter.CTkLabel(scroll_frame, text="No New Image Selected")
        image_preview.pack()

        save_button = customtkinter.CTkButton(scroll_frame, text="Save Changes", command=lambda: self.save_president_changes(edit_entries, edit_window))
        save_button.pack(pady=20)

    def handle_edit_president_image(self, preview_label):
        self.selected_admin_image_path = handle_image_upload(preview_label, fixed_filename="admin_profile.png")

    def save_president_changes(self, entries, window):
        data = {key: entry.get() for key, entry in entries.items()}
        
        if data["email"] and not validate_email(data["email"]):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.", parent=window)
            return

        data["image_path"] = self.selected_admin_image_path
        update_admin_profile(data)
        self.selected_admin_image_path = None
        messagebox.showinfo("Success", "Profile updated.", parent=window)
        window.destroy()
        self.refresh_admin_profile()
        self.app.reload_company_details()

    def create_employee_section(self, parent):
        title_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        title_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
        
        customtkinter.CTkLabel(title_frame, text="Employee Management", font=customtkinter.CTkFont(size=18, weight="bold")).pack(side="left", padx=10)
        customtkinter.CTkButton(title_frame, text="Export to Excel", command=self.export_employees_to_excel).pack(side="right", padx=10)

        add_form = customtkinter.CTkFrame(parent, fg_color="transparent")
        add_form.grid(row=1, column=0, sticky="ew", padx=40)

        fields = [
            ("first_name", "First Name", "الإسم الشخصي"), ("last_name", "Last Name", "الإسم العائلي"),
            ("birthday", "Birthday", "تاريخ الإزدياد"), ("cin", "CIN", "رقم البطاقة الوطنية"),
            ("phone", "Phone", "رقم الهاتف"), ("address", "Address", "العنوان")
        ]

        for key, english_label, arabic_label in fields:
            label_frame = customtkinter.CTkFrame(add_form, fg_color="transparent")
            label_frame.pack(fill="x", padx=5, pady=(5,0))
            customtkinter.CTkLabel(label_frame, text=english_label).pack(side="left")
            customtkinter.CTkLabel(label_frame, text=arabic_label, font=self.arabic_font).pack(side="right")
            
            justify_side = 'right' if key in ['first_name', 'last_name', 'address'] else 'left'

            if key == "birthday":
                date_frame = customtkinter.CTkFrame(add_form, fg_color="transparent")
                date_frame.pack(fill="x", padx=5, pady=(0,5))
                entry = customtkinter.CTkEntry(date_frame, placeholder_text=english_label, justify=justify_side)
                entry.pack(fill="x", expand=True, side="left")
                customtkinter.CTkButton(date_frame, text="📅", width=30, command=lambda e=entry: self._open_calendar_popup(e)).pack(side="right", padx=(5,0))
            else:
                entry = customtkinter.CTkEntry(add_form, placeholder_text=english_label, justify=justify_side)
                entry.pack(fill="x", padx=5, pady=(0,5))
            
            setattr(self, f"emp_{key}", entry)

        upload_frame = customtkinter.CTkFrame(add_form, fg_color="transparent")
        upload_frame.pack(fill="x", padx=5, pady=5)
        
        customtkinter.CTkButton(upload_frame, text="Upload Image", command=self.upload_employee_image , font=customtkinter.CTkFont(size=13, weight="bold")).pack(side="left")
        self.emp_image_preview = customtkinter.CTkLabel(upload_frame, text="No Image Selected")
        self.emp_image_preview.pack(side="left", padx=10)

        customtkinter.CTkButton(add_form, text="إضافة عامل", command=self.add_employee, font=self.arabic_font).pack(pady=10)

        self.employee_list_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        self.employee_list_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.employee_list_frame.grid_columnconfigure(0, weight=1)

    def export_employees_to_excel(self):
        employees_data = get_employees()
        if not employees_data:
            messagebox.showinfo("No Data", "There are no employees to export.")
            return
        
        headers = ["ID", "First Name", "Last Name", "Birthday", "CIN", "Phone", "Address"]
        data_to_export = [[emp[0], emp[1], emp[2], emp[3], emp[4], emp[5], emp[6]] for emp in employees_data]
        export_to_excel(headers, data_to_export, default_filename="employees_export.xlsx")

    def add_employee(self):
        bday = validate_and_format_date(self.emp_birthday.get())
        if self.emp_birthday.get() and bday is None:
            messagebox.showerror("Invalid Date", "Please use a valid date format for birthday.")
            return

        data = {
            "first_name": self.emp_first_name.get(), "last_name": self.emp_last_name.get(),
            "birthday": bday, "cin": self.emp_cin.get(),
            "phone": self.emp_phone.get(), "address": self.emp_address.get(),
            "image_path": self.selected_employee_image_path
        }
        
        if not all(data.get(k) for k in ["first_name", "last_name", "phone", "cin"]):
            messagebox.showerror("Error", "First name, last name, CIN, and phone are required.")
            return

        add_employee(data)
        self.clear_employee_form()
        self.refresh_employee_list()

    def delete_employee(self, emp_id):
        if messagebox.askyesno("Confirm Delete", "Remove this employee?"):
            delete_employee(emp_id)
            self.refresh_employee_list()

    def refresh_employee_list(self):
        for widget in self.employee_list_frame.winfo_children(): widget.destroy()
        for emp_data in get_employees():
            self.create_employee_card(self.employee_list_frame, emp_data).pack(fill="x", expand=True, pady=5, padx=5)

    def clear_employee_form(self):
        self.emp_first_name.delete(0, 'end'); self.emp_last_name.delete(0, 'end')
        self.emp_birthday.delete(0, 'end'); self.emp_cin.delete(0, 'end')
        self.emp_phone.delete(0, 'end'); self.emp_address.delete(0, 'end')
        self.selected_employee_image_path = None
        self.emp_image_preview.configure(text="No Image Selected")

    def upload_employee_image(self):
        self.selected_employee_image_path = handle_image_upload(self.emp_image_preview)

    def create_employee_card(self, parent, data, is_admin=False):
        frame = customtkinter.CTkFrame(parent)
        frame.grid_columnconfigure(1, weight=1)

        if is_admin:
            (emp_id, fname, lname, phone, address, image_path, company_name, company_id, _, fax, email) = data
            row_span = 6
        else:
            (emp_id, fname, lname, bday, cin, phone, address, image_path) = data
            row_span = 5

        img = get_image_for_card(image_path)
        customtkinter.CTkLabel(frame, image=img, text="").grid(row=0, column=0, rowspan=row_span, padx=10, pady=10)
        customtkinter.CTkLabel(frame, text=f"{fname} {lname}", font=customtkinter.CTkFont(size=18, weight="bold")).grid(row=0, column=1, sticky="w", padx=10)
        
        if is_admin:
            customtkinter.CTkLabel(frame, text=f"Company: {company_name or 'N/A'} (ID: {company_id or 'N/A'})", font=self.font_card_details).grid(row=1, column=1, sticky="w", padx=10)
            customtkinter.CTkLabel(frame, text=f"Address: {address or 'N/A'}", font=self.font_card_details).grid(row=2, column=1, sticky="w", padx=10)
            customtkinter.CTkLabel(frame, text=f"Phone: {phone or 'N/A'}", font=self.font_card_details).grid(row=3, column=1, sticky="w", padx=10)
            customtkinter.CTkLabel(frame, text=f"Fax: {fax or 'N/A'}", font=self.font_card_details).grid(row=4, column=1, sticky="w", padx=10)
            customtkinter.CTkLabel(frame, text=f"Email: {email or 'N/A'}", font=self.font_card_details).grid(row=5, column=1, sticky="w", padx=10, pady=(0,10))
        else:
            customtkinter.CTkLabel(frame, text=f"Birthday: {bday or 'N/A'}", font=self.font_card_details).grid(row=1, column=1, sticky="w", padx=10)
            customtkinter.CTkLabel(frame, text=f"CIN: {cin or 'N/A'}", font=self.font_card_details).grid(row=2, column=1, sticky="w", padx=10)
            customtkinter.CTkLabel(frame, text=f"Phone: {phone or 'N/A'}", font=self.font_card_details).grid(row=3, column=1, sticky="w", padx=10)
            customtkinter.CTkLabel(frame, text=f"Address: {address or 'N/A'}", font=self.font_card_details).grid(row=4, column=1, sticky="w", padx=10, pady=(0,10))

        if not is_admin:
            button_frame = customtkinter.CTkFrame(frame, fg_color="transparent")
            button_frame.grid(row=0, column=2, rowspan=row_span, padx=10)
            customtkinter.CTkButton(button_frame, text="Edit", command=lambda e_id=emp_id: self.open_edit_employee_window(e_id), width=80).pack(pady=5)
            customtkinter.CTkButton(button_frame, text="Remove", fg_color="red", hover_color="#C00000", command=lambda e_id=emp_id: self.delete_employee(e_id), width=80).pack(pady=5)
        
        return frame
    
    def open_edit_employee_window(self, emp_id):
        emp_data = get_employee_by_id(emp_id)
        if not emp_data: return

        edit_window = customtkinter.CTkToplevel(self)
        edit_window.title("Edit Employee")
        edit_window.geometry("400x600")
        edit_window.transient(self.app); edit_window.grab_set(); edit_window.focus()
        (_, fname, lname, bday, cin, phone, address, _) = emp_data
        
        fields = [
            ("first_name", fname, "First Name", "الإسم الشخصي"), ("last_name", lname, "Last Name", "الإسم العائلي"),
            ("birthday", bday, "Birthday", "تاريخ الإزدياد"), ("cin", cin, "CIN", "رقم البطاقة الوطنية"),
            ("phone", phone, "Phone", "رقم الهاتف"), ("address", address, "Address", "العنوان")
        ]

        edit_entries = {}
        for key, val, english_label, arabic_label in fields:
            label_frame = customtkinter.CTkFrame(edit_window, fg_color="transparent")
            label_frame.pack(fill="x", padx=20, pady=(10,0))
            customtkinter.CTkLabel(label_frame, text=english_label).pack(side="left")
            customtkinter.CTkLabel(label_frame, text=arabic_label, font=self.arabic_font).pack(side="right")
            
            justify_side = 'right' if key in ['first_name', 'last_name', 'address'] else 'left'
            if key == "birthday":
                date_frame = customtkinter.CTkFrame(edit_window, fg_color="transparent")
                date_frame.pack(fill="x", padx=20, pady=(0,5))
                entry = customtkinter.CTkEntry(date_frame, justify=justify_side)
                entry.pack(fill="x", expand=True, side="left")
                customtkinter.CTkButton(date_frame, text="📅", width=30, command=lambda e=entry: self._open_calendar_popup(e)).pack(side="right", padx=(5,0))
            else:
                entry = customtkinter.CTkEntry(edit_window, justify=justify_side)
                entry.pack(fill="x", padx=20, pady=(0,5))
            
            entry.insert(0, val or "")
            edit_entries[key] = entry

        self.selected_employee_image_path_edit = None
        image_button = customtkinter.CTkButton(edit_window, text="Upload New Image", command=lambda: self.handle_edit_employee_image(image_preview))
        image_button.pack(pady=(20, 5))
        image_preview = customtkinter.CTkLabel(edit_window, text="No New Image Selected")
        image_preview.pack()
        
        save_button = customtkinter.CTkButton(edit_window, text="Save Changes", command=lambda: self.save_employee_changes(emp_id, edit_entries, edit_window))
        save_button.pack(pady=20)

    def handle_edit_employee_image(self, preview_label):
        self.selected_employee_image_path_edit = handle_image_upload(preview_label)

    def save_employee_changes(self, emp_id, entries, window):
        bday = validate_and_format_date(entries["birthday"].get())
        if entries["birthday"].get() and bday is None:
            messagebox.showerror("Invalid Date", "Please use a valid date format for birthday.", parent=window)
            return
            
        data = {key: entry.get() for key, entry in entries.items()}
        data["birthday"] = bday
        data["image_path"] = self.selected_employee_image_path_edit

        if not all(data.get(k) for k in ["first_name", "last_name", "phone", "cin"]):
            messagebox.showerror("Error", "Required fields are empty.", parent=window)
            return
            
        update_employee(emp_id, data)
        messagebox.showinfo("Success", "Employee details updated.", parent=window)
        window.destroy()
        self.refresh_employee_list()
