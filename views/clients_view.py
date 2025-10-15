import customtkinter
from tkinter import messagebox
from tkcalendar import Calendar
from database import add_client, get_clients, delete_client, get_client_by_id, update_client
from utils import handle_image_upload, get_image_for_card, generate_client_contract, validate_and_format_date, export_to_excel

class ClientsFrame(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.company_details = self.app.company_details
        self.selected_image_path = None
        self.selected_image_path_edit = None
        self.entry_widgets = {}
        self.arabic_font = customtkinter.CTkFont(size=14, weight="bold")
        
        self.arabic_license_options = ["(سيارة) B رخصة", "(نارية دراجة) A رخصة", "(شاحنة) C رخصة"]
        self.license_map_to_arabic = {
            "Permis B (Car)": "(سيارة) B رخصة", "Permis A (Moto)": "(نارية دراجة) A رخصة", "Permis C (Truck)": "(شاحنة) C رخصة"
        }
        self.license_map_to_english = {v: k for k, v in self.license_map_to_arabic.items()}

        self.grid_columnconfigure(0, weight=1); self.grid_columnconfigure(1, weight=2); self.grid_rowconfigure(0, weight=1)
        self.create_client_input_frame(self).grid(row=0, column=0, padx=(0, 10), pady=5, sticky="nsew")
        self.create_search_and_list_frame(self).grid(row=0, column=1, padx=(10, 0), pady=5, sticky="nsew")
        self.refresh_client_list()

    def _open_calendar_popup(self, entry_widget):
        top = customtkinter.CTkToplevel(self)
        top.title("Select Date"); top.geometry("300x250"); top.transient(self.app); top.grab_set()
        cal = Calendar(top, selectmode='day', date_pattern='dd/mm/y')
        cal.pack(pady=10, padx=10, fill="both", expand=True)
        def select_date():
            entry_widget.delete(0, 'end'); entry_widget.insert(0, cal.get_date()); top.destroy()
        customtkinter.CTkButton(top, text="Select", command=select_date).pack(pady=10)

    def create_client_input_frame(self, parent):
        frame = customtkinter.CTkScrollableFrame(parent, label_text="جديد زبون إضافة", label_font=customtkinter.CTkFont(size=20, weight="bold"))
        frame.grid_columnconfigure(0, weight=1)
        
        fields = [
            ("first_name", "First Name", "الشخصي الإسم"), ("last_name", "Last Name", "العائلي الإسم"),
            ("address", "Address", "العنوان"), ("birthday", "Birthday (DD/MM/YYYY)", "الإزدياد تاريخ"),
            ("cin", "CIN", "الوطنية البطاقة رقم"), ("phone", "Phone Number", "الهاتف رقم"),
            ("hours_practice", "Practice Hours", "التدريب ساعات"), ("hours_theory", "Theory Hours", "النظرية ساعات"),
            ("vehicle_matricule", "Vehicle Matricule", "المركبة تسجيل رقم"),
            ("monitor_name", "Monitor Name", "المدرب إسم"),
            ("exam_success_date", "Exam Success Date (DD/MM/YYYY)", "الإمتحان في النجاح تاريخ")
        ]
        
        for key, placeholder, arabic_label in fields:
            label_frame = customtkinter.CTkFrame(frame, fg_color="transparent"); label_frame.pack(fill="x", padx=10, pady=(5, 0))
            customtkinter.CTkLabel(label_frame, text=placeholder.split(" (")[0], font=customtkinter.CTkFont(weight="bold")).pack(side="left")
            customtkinter.CTkLabel(label_frame, text=arabic_label, font=self.arabic_font).pack(side="right")
            
            if key in ["birthday", "exam_success_date"]:
                date_frame = customtkinter.CTkFrame(frame, fg_color="transparent"); date_frame.pack(fill="x", padx=10, pady=(0, 5))
                entry = customtkinter.CTkEntry(date_frame, placeholder_text=placeholder); entry.pack(side="left", fill="x", expand=True)
                customtkinter.CTkButton(date_frame, text="📅", width=30, command=lambda e=entry: self._open_calendar_popup(e)).pack(side="right", padx=(5,0))
                self.entry_widgets[key] = entry
            else:
                entry = customtkinter.CTkEntry(frame, placeholder_text=placeholder); entry.pack(fill="x", padx=10, pady=(0, 5))
                self.entry_widgets[key] = entry
        
        self.entry_widgets["hours_practice"].insert(0, "20"); self.entry_widgets["hours_practice"].configure(state="disabled")
        self.entry_widgets["hours_theory"].insert(0, "20"); self.entry_widgets["hours_theory"].configure(state="disabled")
        self.entry_widgets["vehicle_matricule"].insert(0, "82-A-6958"); self.entry_widgets["vehicle_matricule"].configure(state="disabled")

        license_label_frame = customtkinter.CTkFrame(frame, fg_color="transparent"); license_label_frame.pack(fill="x", padx=10, pady=(5, 0))
        customtkinter.CTkLabel(license_label_frame, text="License Type", font=customtkinter.CTkFont(weight="bold")).pack(side="left")
        customtkinter.CTkLabel(license_label_frame, text="الرخصة نوع", font=self.arabic_font).pack(side="right")
        
        self.license_type_menu = customtkinter.CTkComboBox(frame, values=self.arabic_license_options); self.license_type_menu.pack(fill="x", padx=10, pady=(0, 5))
        
        self.upload_image_button = customtkinter.CTkButton(frame, text="Upload Image", command=self.upload_image); self.upload_image_button.pack(pady=10)
        self.image_preview_label = customtkinter.CTkLabel(frame, text="No Image Selected"); self.image_preview_label.pack()
        
        self.add_client_button = customtkinter.CTkButton(frame, text="Add Client", command=self.add_client); self.add_client_button.pack(pady=20)
        
        self.status_label = customtkinter.CTkLabel(frame, text=""); self.status_label.pack()
        
        return frame

    def create_search_and_list_frame(self, parent):
        container = customtkinter.CTkFrame(parent, fg_color="transparent"); container.grid_columnconfigure(0, weight=1); container.grid_rowconfigure(1, weight=1)
        search_frame = customtkinter.CTkFrame(container); search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10)); search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = customtkinter.CTkEntry(search_frame, placeholder_text="Search by name, phone, or CIN..."); 
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh_client_list())

        export_button = customtkinter.CTkButton(search_frame, text="Export to Excel", command=self.export_clients_to_excel)
        export_button.grid(row=0, column=1, padx=(0, 10), pady=10)

        self.client_list_frame = customtkinter.CTkScrollableFrame(container); self.client_list_frame.grid(row=1, column=0, pady=0, sticky="nsew"); self.client_list_frame.grid_columnconfigure(0, weight=1)
        return container

    def export_clients_to_excel(self):
        clients_data = get_clients(self.search_entry.get())
        if not clients_data:
            messagebox.showinfo("No Data", "There is no client data to export.")
            return
        
        headers = ["ID", "First Name", "Last Name", "Address", "Phone", "License Type", "Company Name", "Company ID", "Birthday", "CIN", "Practice Hours", "Theory Hours", "Vehicle Matricule", "Monitor Name", "Exam Success Date"]
        
        data_to_export = []
        for client in clients_data:
            client_list = list(client)
            del client_list[6] 
            data_to_export.append(client_list)

        export_to_excel(headers, data_to_export, default_filename="clients_export.xlsx")

    def refresh_client_list(self):
        for widget in self.client_list_frame.winfo_children(): widget.destroy()
        for row in get_clients(self.search_entry.get()):
            self.create_client_card(self.client_list_frame, row).pack(fill="x", padx=10, pady=5, expand=True)

    def create_client_card(self, parent, data):
        (client_id, fname, lname, address, phone, license, image_path, _, _, bday, cin, _, _, _, _, _) = data
        frame = customtkinter.CTkFrame(parent); frame.grid_columnconfigure(1, weight=1)
        customtkinter.CTkLabel(frame, image=get_image_for_card(image_path), text="").grid(row=0, column=0, rowspan=6, padx=10, pady=10)
        info_frame = customtkinter.CTkFrame(frame, fg_color="transparent"); info_frame.grid(row=0, column=1, rowspan=6, sticky="w", padx=10)
        customtkinter.CTkLabel(info_frame, text=f"{fname} {lname}", font=customtkinter.CTkFont(size=18, weight="bold")).pack(anchor="w")
        for text in [f"CIN: {cin or 'N/A'}", f"Phone Number: {phone or 'N/A'}", f"Birthday: {bday or 'N/A'}", f"Address: {address or 'N/A'}", f"Permis Licence: {license or 'N/A'}"]:
            customtkinter.CTkLabel(info_frame, text=text).pack(anchor="w")
        button_frame = customtkinter.CTkFrame(frame, fg_color="transparent"); button_frame.grid(row=0, column=2, rowspan=6, padx=10)
        customtkinter.CTkButton(button_frame, text="Edit", command=lambda c_id=client_id: self.open_edit_client_window(c_id), width=100).pack(pady=2)
        customtkinter.CTkButton(button_frame, text="Delete", fg_color="red", hover_color="#C00000", command=lambda c_id=client_id: self.delete_client(c_id), width=100).pack(pady=2)
        customtkinter.CTkButton(button_frame, text="Print Contract", fg_color="#00529B", hover_color="#003366", command=lambda c_id=client_id: self.print_contract(c_id), width=100).pack(pady=2)
        return frame

    def print_contract(self, client_id):
        client_data = get_client_by_id(client_id)
        if client_data:
            generate_client_contract(client_data, self.company_details)
        else:
            messagebox.showerror("Error", "Could not find client data.")

    def delete_client(self, client_id):
        if messagebox.askyesno("Confirm Delete", "Delete this client?"):
            delete_client(client_id)
            self.refresh_client_list()

    def add_client(self):
        client_data = {key: self.entry_widgets[key].get() for key in self.entry_widgets}
        if not all(client_data.get(key) for key in ["first_name", "last_name", "phone", "cin"]):
            return messagebox.showerror("Error", "Required fields cannot be empty.")
            
        bday = validate_and_format_date(client_data["birthday"])
        exam_date = validate_and_format_date(client_data["exam_success_date"])
        
        if (client_data["birthday"] and bday is None) or (client_data["exam_success_date"] and exam_date is None):
            return messagebox.showerror("Invalid Date", "Please use a valid date format (DD/MM/YYYY).")

        client_data.update({
            "birthday": bday, 
            "exam_success_date": exam_date, 
            "license_type": self.license_map_to_english.get(self.license_type_menu.get()), 
            "image_path": self.selected_image_path, 
            "company_name": self.company_details.get('name'), 
            "company_id": self.company_details.get('id')
        })
        add_client(client_data)
        self.status_label.configure(text="Client added!", text_color="green")
        self.refresh_client_list()
        self.clear_client_form()

    def clear_client_form(self):
        for key, entry in self.entry_widgets.items():
            if key not in ["hours_practice", "hours_theory", "vehicle_matricule"]: 
                entry.delete(0, 'end')
        
        for key, default in [("hours_practice", "20"), ("hours_theory", "20"), ("vehicle_matricule", "82-A-6958")]:
            entry = self.entry_widgets[key]
            entry.configure(state="normal")
            entry.delete(0, 'end')
            entry.insert(0, default)
            entry.configure(state="disabled")

        self.image_preview_label.configure(text="No Image Selected")
        self.selected_image_path = None
        self.status_label.after(3000, lambda: self.status_label.configure(text=""))

    def upload_image(self):
        self.selected_image_path = handle_image_upload(self.image_preview_label)

    def open_edit_client_window(self, client_id):
        client_data = get_client_by_id(client_id)
        if not client_data: 
            return

        edit_window = customtkinter.CTkToplevel(self)
        edit_window.title("Edit Client")
        edit_window.geometry("450x750")
        edit_window.transient(self.app)
        edit_window.grab_set()
        edit_window.focus()

        scroll_frame = customtkinter.CTkScrollableFrame(edit_window)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        (_, fname, lname, address, phone, license, _, _, _, bday, cin, h_prac, h_theo, v_mat, exam_date, monitor) = client_data
        
        fields_data = {
            ("First Name", "الشخصي الإسم"): ("first_name", fname), ("Last Name", "العائلي الإسم"): ("last_name", lname), 
            ("Address", "العنوان"): ("address", address), ("Birthday", "الإزدياد تاريخ"): ("birthday", bday), 
            ("CIN", "الوطنية البطاقة رقم"): ("cin", cin), ("Phone Number", "الهاتف رقم"): ("phone", phone), 
            ("Practice Hours", "التدريب ساعات"): ("hours_practice", h_prac), ("Theory Hours", "النظرية ساعات"): ("hours_theory", h_theo),
            ("Vehicle Matricule", "المركبة تسجيل رقم"): ("vehicle_matricule", v_mat),
            ("Monitor Name", "المدرب إسم"): ("monitor_name", monitor),
            ("Exam Success Date", "الإمتحان في النجاح تاريخ"): ("exam_success_date", exam_date)
        }
        
        edit_entries = {}
        for (english_label, arabic_label), (key, val) in fields_data.items():
            label_frame = customtkinter.CTkFrame(scroll_frame, fg_color="transparent"); label_frame.pack(fill="x", padx=10, pady=(10, 0))
            customtkinter.CTkLabel(label_frame, text=english_label, font=customtkinter.CTkFont(weight="bold")).pack(side="left")
            customtkinter.CTkLabel(label_frame, text=arabic_label, font=self.arabic_font).pack(side="right")
            
            if key in ["birthday", "exam_success_date"]:
                date_frame = customtkinter.CTkFrame(scroll_frame, fg_color="transparent"); date_frame.pack(fill="x", padx=10, pady=(0, 5))
                entry = customtkinter.CTkEntry(date_frame); entry.pack(side="left", fill="x", expand=True)
                customtkinter.CTkButton(date_frame, text="📅", width=30, command=lambda e=entry: self._open_calendar_popup(e)).pack(side="right", padx=(5,0))
            else:
                entry = customtkinter.CTkEntry(scroll_frame); entry.pack(fill="x", padx=10, pady=(0, 5))
            entry.insert(0, val or ""); edit_entries[key] = entry
        
        for key in ["hours_practice", "hours_theory", "vehicle_matricule"]: 
            edit_entries[key].configure(state="disabled")
        
        license_label_frame = customtkinter.CTkFrame(scroll_frame, fg_color="transparent"); license_label_frame.pack(fill="x", padx=10, pady=(10, 0))
        customtkinter.CTkLabel(license_label_frame, text="License Type", font=customtkinter.CTkFont(weight="bold")).pack(side="left")
        customtkinter.CTkLabel(license_label_frame, text="الرخصة نوع", font=self.arabic_font).pack(side="right")
        license_menu = customtkinter.CTkComboBox(scroll_frame, values=self.arabic_license_options); license_menu.pack(fill="x", padx=10, pady=(0, 5)); license_menu.set(self.license_map_to_arabic.get(license, license))
        
        self.selected_image_path_edit = None
        image_button = customtkinter.CTkButton(scroll_frame, text="Upload New Image", command=lambda: self.handle_edit_client_image(image_preview)); image_button.pack(pady=(20, 5))
        image_preview = customtkinter.CTkLabel(scroll_frame, text="No New Image Selected"); image_preview.pack()
        customtkinter.CTkButton(scroll_frame, text="Save Changes", command=lambda: self.save_client_changes(client_id, edit_entries, license_menu, edit_window)).pack(pady=20)

    def handle_edit_client_image(self, preview_label):
        self.selected_image_path_edit = handle_image_upload(preview_label)

    def save_client_changes(self, client_id, entries, license_menu, window):
        data = {key: entry.get() for key, entry in entries.items()}
        bday = validate_and_format_date(data["birthday"])
        exam_date = validate_and_format_date(data["exam_success_date"])
        
        if (data["birthday"] and bday is None) or (data["exam_success_date"] and exam_date is None):
            return messagebox.showerror("Invalid Date", "Please use a valid date format (DD/MM/YYYY).", parent=window)

        data.update({
            "birthday": bday, 
            "exam_success_date": exam_date, 
            "license_type": self.license_map_to_english.get(license_menu.get()), 
            "image_path": self.selected_image_path_edit
        })
        update_client(client_id, data)
        messagebox.showinfo("Success", "Client details updated.", parent=window)
        window.destroy()
        self.refresh_client_list()
