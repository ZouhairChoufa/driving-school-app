# -*- coding: utf-8 -*-
import customtkinter
import database

class DashboardFrame(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, corner_radius=10)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) 

        font_arabic_welcome = customtkinter.CTkFont(family="Arial", size=32, weight="bold")
        company_name_stat = "مرحبا بكم في مؤسسة عبد الكريم لتعليم السياقة"
        
        total_clients, total_employees = database.get_dashboard_stats()
        welcome_label = customtkinter.CTkLabel(self, text=company_name_stat, font=font_arabic_welcome)
        welcome_label.grid(row=0, column=0, pady=(40, 20), padx=20)
        stats_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        stats_frame.grid(row=1, column=0, pady=20)
        stats_frame.grid_columnconfigure((0, 1), weight=0)

        clients_card = self.create_stat_card(stats_frame, "Total Clients", total_clients)
        clients_card.grid(row=0, column=0, padx=20, pady=20)

        employees_card = self.create_stat_card(stats_frame, "Total Employees", total_employees)
        employees_card.grid(row=0, column=1, padx=20, pady=20)

    def create_stat_card(self, parent, title, value):
        card = customtkinter.CTkFrame(parent, corner_radius=10, width=200, height=120)
        card.pack_propagate(False)
        
        title_label = customtkinter.CTkLabel(card, text=title, font=customtkinter.CTkFont(size=20))
        title_label.pack(pady=(20, 5), padx=20)
        
        value_label = customtkinter.CTkLabel(card, text=str(value), font=customtkinter.CTkFont(size=36, weight="bold"))
        value_label.pack(pady=(0, 20), padx=20)
        
        return card
