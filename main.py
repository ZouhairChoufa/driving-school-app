# -*- coding: utf-8 -*-
import sys
import os
import traceback
import customtkinter
from tkinter import messagebox
import sqlite3 
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import database
from views.dashboord_view import DashboardFrame
from views.clients_view import ClientsFrame
from views.admin_view import AdminFrame

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Driving School Management")
        self.center_window(600, 500)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.navigation_frame = None
        self.content_frame = None
        self.login_frame = None
        self.register_frame = None
        self.current_user_role = None
        self.font_arabic_bold = customtkinter.CTkFont(family="Arial", size=16, weight="bold")
        self.font_arabic_large_bold = customtkinter.CTkFont(family="Arial", size=24, weight="bold")
        self.font_arabic_nav_title = customtkinter.CTkFont(family="Arial", size=20, weight="bold")
        self.font_arabic_small_bold = customtkinter.CTkFont(family="Arial", size=12, weight="bold")

        self.text_button_color = "#000000"
        self._show_login_frame()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _clear_all_frames(self):
        for frame in [self.login_frame, self.register_frame, self.navigation_frame, self.content_frame]:
            if frame:
                frame.destroy()
        self.login_frame = self.register_frame = self.navigation_frame = self.content_frame = None

    def _show_login_frame(self):
        self._clear_all_frames()
        self.center_window(600, 500)
        self.login_frame = customtkinter.CTkFrame(self)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        
        center_frame = customtkinter.CTkFrame(self.login_frame)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        customtkinter.CTkLabel(center_frame, text="تسجيل الدخول", font=self.font_arabic_large_bold).pack(pady=(20, 30), padx=40)
        
        self.username_entry = customtkinter.CTkEntry(center_frame, placeholder_text="Username or Company ID", width=250)
        self.username_entry.pack(pady=10, padx=40)
        self.password_entry = customtkinter.CTkEntry(center_frame, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=10, padx=40)
        self.password_entry.bind("<Return>", self._login_event)
        
        customtkinter.CTkButton(center_frame, text="Login", command=self._login_event, width=250).pack(pady=20, padx=40)
        customtkinter.CTkButton(center_frame, text="إنشاء حساب جديد", fg_color="transparent", text_color=self.text_button_color, command=self._show_register_frame, font=self.font_arabic_small_bold).pack(pady=(0,20))

    def _show_register_frame(self):
        self._clear_all_frames()
        self.register_frame = customtkinter.CTkFrame(self)
        self.register_frame.grid(row=0, column=0, sticky="nsew")

        center_frame = customtkinter.CTkFrame(self.register_frame)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        customtkinter.CTkLabel(center_frame, text="إنشاء حساب", font=self.font_arabic_large_bold).pack(pady=(20, 30), padx=40)

        self.reg_fname_entry = customtkinter.CTkEntry(center_frame, placeholder_text="First Name - الإسم الأول", width=250, justify='right')
        self.reg_fname_entry.pack(pady=5, padx=40)
        self.reg_lname_entry = customtkinter.CTkEntry(center_frame, placeholder_text="Last Name - الإسم العائلي", width=250, justify='right')
        self.reg_lname_entry.pack(pady=5, padx=40)
        self.reg_username_entry = customtkinter.CTkEntry(center_frame, placeholder_text="Username - إسم المستخدم", width=250)
        self.reg_username_entry.pack(pady=5, padx=40)
        self.reg_company_id_entry = customtkinter.CTkEntry(center_frame, placeholder_text="Company ID - رقم المؤسسة", width=250)
        self.reg_company_id_entry.pack(pady=5, padx=40)
        self.reg_password_entry = customtkinter.CTkEntry(center_frame, placeholder_text="Password - كلمة السر", show="*", width=250)
        self.reg_password_entry.pack(pady=5, padx=40)

        customtkinter.CTkButton(center_frame, text="Register", command=self._register_event, width=250).pack(pady=20, padx=40)
        customtkinter.CTkButton(center_frame, text="عودة", fg_color="transparent", text_color=self.text_button_color, command=self._show_login_frame, font=self.font_arabic_bold).pack(pady=(0,20))

    def _register_event(self):
        fname = self.reg_fname_entry.get()
        lname = self.reg_lname_entry.get()
        username = self.reg_username_entry.get()
        company_id = self.reg_company_id_entry.get()
        password = self.reg_password_entry.get()

        if not all([fname, lname, username, company_id, password]):
            messagebox.showerror("Registration Failed", "All fields are required.")
            return
        
        if company_id != '5704':
            messagebox.showerror("Registration Failed", "Invalid Company ID. Please enter the correct ID to register.")
            return

        try:
            database.create_user(fname, lname, username, company_id, password)
            messagebox.showinfo("Success", "Account created successfully! You can now log in.")
            self._show_login_frame()
        except sqlite3.IntegrityError:
            messagebox.showerror("Registration Error", f"The username '{username}' is already taken. Please choose another one.")
        except Exception as e:
            messagebox.showerror("Registration Error", f"An unexpected error occurred: {e}")

    def _login_event(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Login Failed", "Please enter both Username and Password.")
            return

        role = database.check_login(username, password)
        if role:
            self.current_user_role = role
            self._clear_all_frames()
            self._show_main_ui()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def _show_main_ui(self):
        self.center_window(1200, 720)
        self.grid_columnconfigure(0, weight=0); self.grid_columnconfigure(1, weight=1)

        self.reload_company_details()
        self.title(f"Gestion - {self.company_details.get('name', 'AUTO ECOLE ABDELKRIM')}")

        self.navigation_frame = self.create_navigation_frame()
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        self.content_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_frame.grid_columnconfigure(0, weight=1); self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.show_dashboard()

    def create_navigation_frame(self):
        frame = customtkinter.CTkFrame(self, corner_radius=0)
        frame.grid_rowconfigure(4, weight=1)

        customtkinter.CTkLabel(frame, text="مؤسسة عبد الكريم لتعليم السياقة", font=self.font_arabic_nav_title).grid(row=0, column=0, padx=40, pady=20)

        buttons = {"Dashboard": self.show_dashboard, "Clients": self.show_clients_frame}
        for i, (text, command) in enumerate(buttons.items(), 1):
            customtkinter.CTkButton(frame, text=text, anchor="w", command=command).grid(row=i, column=0, sticky="ew", padx=10, pady=5)
        
        if self.current_user_role == 'Admin':
            customtkinter.CTkButton(frame, text="Admin", anchor="w", command=self.show_admin_frame).grid(row=len(buttons)+1, column=0, sticky="ew", padx=10, pady=5)
        
        customtkinter.CTkOptionMenu(frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event).grid(row=5, column=0, padx=10, pady=20, sticky="s")
        return frame

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def clear_content_frame(self):
        if self.content_frame:
            for widget in self.content_frame.winfo_children(): widget.destroy()

    def reload_company_details(self):
        admin_profile = database.get_admin_profile()
        self.company_details = {"name": admin_profile[6], "id": admin_profile[7]} if admin_profile and len(admin_profile) > 7 else {"name": "AUTO ECOLE ABDELKRIM", "id": "N/A"}

    def show_dashboard(self): self.clear_content_frame(); DashboardFrame(self.content_frame, self).grid(row=0, column=0, sticky="nsew")
    def show_clients_frame(self): self.clear_content_frame(); ClientsFrame(self.content_frame, self).grid(row=0, column=0, sticky="nsew")
    def show_admin_frame(self): self.clear_content_frame(); AdminFrame(self.content_frame, self).grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    try:
        database.setup_database()
        app = App()
        app.mainloop()
    except Exception:
        with open("error.log", "w") as f:
            f.write(traceback.format_exc())
        traceback.print_exc()

