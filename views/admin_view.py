import os
import shutil
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, 
                            QPushButton, QScrollArea, QLineEdit, 
                            QDateEdit, QFileDialog, QMessageBox, QGridLayout)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QDate, pyqtSignal
import database as db
import utils
from dialogs import EditEmployeeDialog, EditAdminDialog
from utils import resource_path

class AdminView(QWidget):
    data_changed_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AdminPage")
        self.current_employee_image_path = None

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        container = QWidget()
        scroll.setWidget(container)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        self.company_profile_section = self._create_company_profile_section()

        employee_management_layout = QHBoxLayout()
        self.employee_management_section = self._create_employee_management_section()
        self.employee_list_section = self._create_employee_list_view()
        
        employee_management_layout.addWidget(self.employee_management_section, 1)
        employee_management_layout.addWidget(self.employee_list_section, 1)

        layout.addWidget(self.company_profile_section)
        layout.addLayout(employee_management_layout)
        layout.addStretch()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        
        self.refresh_admin_profile()
        self.refresh_employee_list()

    def _create_company_profile_section(self):
        container = QFrame()
        container.setProperty("class", "card")
        layout = QVBoxLayout(container)

        title = QLabel("President & Company Profile", objectName="TitleLabel")
        
        details_layout = QHBoxLayout()
        self.profile_image = QLabel()
        self.profile_image.setFixedSize(100, 100)
        self.profile_image.setStyleSheet("background-color: #e0e0e0; border-radius: 5px;")
        
        info_layout = QVBoxLayout()
        self.lbl_admin_name = QLabel("Main Admin", objectName="AdminName")
        self.lbl_company_info = QLabel("Company: Auto Ecole Abd El Karim (ID: 5704)")
        self.lbl_address = QLabel("Address: N/A")
        self.lbl_phone = QLabel("Phone: N/A")
        self.lbl_fax = QLabel("Fax: N/A")
        self.lbl_email = QLabel("Email: N/A")
        info_layout.addWidget(self.lbl_admin_name)
        info_layout.addWidget(self.lbl_company_info)
        info_layout.addWidget(self.lbl_address)
        info_layout.addWidget(self.lbl_phone)
        info_layout.addWidget(self.lbl_fax)
        info_layout.addWidget(self.lbl_email)
        
        details_layout.addWidget(self.profile_image)
        details_layout.addLayout(info_layout)
        
        btn_edit_profile = QPushButton("Edit Profile", objectName="EditProfileButton")
        btn_edit_profile.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_edit_profile.clicked.connect(self.open_edit_admin_dialog)
        
        layout.addWidget(title)
        layout.addLayout(details_layout)
        layout.addWidget(btn_edit_profile, alignment=Qt.AlignmentFlag.AlignCenter)
        return container

    def _create_employee_management_section(self):
        container = QFrame()
        container.setProperty("class", "form-container card")
        main_layout = QVBoxLayout(container)

        title = QLabel("Add New Employee", objectName="TitleLabel")
        main_layout.addWidget(title)
        
        form_scroll = QScrollArea()
        form_scroll.setWidgetResizable(True)
        form_scroll.setStyleSheet("QScrollArea { border: none; }")

        form_content_widget = QWidget()
        form_content_layout = QVBoxLayout(form_content_widget)
        form_content_layout.setSpacing(10)

        grid_widget = QWidget()
        form = QGridLayout(grid_widget)
        form.setSpacing(10)
        
        self.employee_inputs = {
            'first_name': QLineEdit(), 'last_name': QLineEdit(),
            'address': QLineEdit(), 'birthday': QDateEdit(calendarPopup=True),
            'cin': QLineEdit(), 'phone': QLineEdit()
        }
        self.employee_inputs['birthday'].setDate(QDate.currentDate())

        for key, widget in self.employee_inputs.items():
            if isinstance(widget, QLineEdit):
                if key in ['first_name', 'last_name', 'address']:
                    widget.setAlignment(Qt.AlignmentFlag.AlignLeft)
                else:
                    widget.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.employee_inputs['first_name'].setPlaceholderText("First Name")
        self.employee_inputs['last_name'].setPlaceholderText("Last Name")
        self.employee_inputs['address'].setPlaceholderText("Address")
        self.employee_inputs['cin'].setPlaceholderText("CIN")
        self.employee_inputs['phone'].setPlaceholderText("Phone Number")

        labels = {
            'first_name': "الاسم الشخصي", 'last_name': "الاسم العائلي",
            'address': "العنوان", 'birthday': "تاريخ الإزدياد",
            'cin': "رقم البطاقة الوطنية", 'phone': "رقم الهاتف",
        }
        
        row = 0
        for key, ar_label in labels.items():
            ar_widget = QLabel(f"<b>{ar_label}</b>")
            ar_widget.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
            
            form.addWidget(ar_widget, row, 0, 1, 2)
            row += 1
            
            form.addWidget(self.employee_inputs[key], row, 0, 1, 2)
            row += 1
        
        form_content_layout.addWidget(grid_widget)
        form_scroll.setWidget(form_content_widget)
        
        upload_layout = QHBoxLayout()
        self.btn_upload_employee_image = QPushButton("Upload Image", objectName="UploadButton")
        self.btn_upload_employee_image.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lbl_employee_image = QLabel("No Image Selected")
        self.lbl_employee_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_layout.addWidget(self.btn_upload_employee_image)
        upload_layout.addWidget(self.lbl_employee_image, 1)
        
        self.btn_add_employee = QPushButton("إضافة عامل", objectName="AddEmployeeButton")
        self.btn_add_employee.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_upload_employee_image.clicked.connect(self.upload_employee_image)
        self.btn_add_employee.clicked.connect(self.add_new_employee)

        main_layout.addWidget(form_scroll)
        main_layout.addLayout(upload_layout)
        main_layout.addWidget(self.btn_add_employee, alignment=Qt.AlignmentFlag.AlignCenter)

        return container

    def _create_employee_list_view(self):
        container = QFrame()
        container.setProperty("class", "card")
        layout = QVBoxLayout(container)
        
        top_bar = QHBoxLayout()
        title = QLabel("Employee List", objectName="TitleLabel")
        self.btn_export_employees = QPushButton("Export to Excel", objectName="ExportButton")
        self.btn_export_employees.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_export_employees.clicked.connect(self.export_employees_to_excel)
        top_bar.addWidget(title)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_export_employees)
        layout.addLayout(top_bar)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        self.employee_list_widget = QWidget()
        scroll.setWidget(self.employee_list_widget)
        self.employee_list_layout = QVBoxLayout(self.employee_list_widget)
        self.employee_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(scroll)
        return container

    def add_new_employee(self):
        data = {key: field.text() if isinstance(field, QLineEdit) else field.date().toString("dd/MM/yyyy") for key, field in self.employee_inputs.items()}
        data['image_path'] = self.current_employee_image_path

        if not data['first_name'] or not data['last_name']:
            QMessageBox.warning(self, "Input Error", "First and Last name are required.")
            return

        try:
            db.add_employee(data)
            QMessageBox.information(self, "Success", "Employee added successfully!")
            self.data_changed_signal.emit()
            self.clear_employee_form()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not add employee: {e}")

    def upload_employee_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            new_path = utils.copy_image_to_data_folder(file_name)
            if new_path:
                self.current_employee_image_path = new_path
                self.lbl_employee_image.setText(os.path.basename(new_path))

    def clear_employee_form(self):
        for widget in self.employee_inputs.values():
            if isinstance(widget, QLineEdit): widget.clear()
            elif isinstance(widget, QDateEdit): widget.setDate(QDate.currentDate())
        self.lbl_employee_image.setText("No Image Selected")
        self.current_employee_image_path = None

    def refresh_admin_profile(self):
        profile = db.get_admin_profile()
        if profile:
            _, fname, lname, phone, addr, img, cname, cid, _, fax, email = profile
            self.lbl_admin_name.setText(f"{fname} {lname}")
            self.lbl_company_info.setText(f"Company: {cname} (ID: {cid})")
            self.lbl_address.setText(f"Address: {addr or 'N/A'}")
            self.lbl_phone.setText(f"Phone: {phone or 'N/A'}")
            self.lbl_fax.setText(f"Fax: {fax or 'N/A'}")
            self.lbl_email.setText(f"Email: {email or 'N/A'}")

            image_to_load = resource_path(img) if img else None
            if image_to_load and os.path.exists(image_to_load):
                pixmap = QPixmap(image_to_load)
                self.profile_image.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def refresh_employee_list(self):
        for i in reversed(range(self.employee_list_layout.count())): 
            self.employee_list_layout.itemAt(i).widget().setParent(None)
        
        employees = db.get_employees()
        for emp_data in employees:
            card = self._create_employee_card(emp_data)
            self.employee_list_layout.addWidget(card)
        
    def export_employees_to_excel(self):
        headers = ["ID", "First Name", "Last Name", "Birthday", "CIN", "Phone", "Address"]
        employees_data = db.get_employees()
        data_to_export = [[e[0], e[1], e[2], e[3], e[4], e[5], e[6]] for e in employees_data]
        utils.export_to_excel_qt(headers, data_to_export, "employees_export.xlsx", self)

    def _create_employee_card(self, emp_data):
        emp_id, first, last, bday, cin, phone, addr, img = emp_data
        
        card = QFrame(); card.setObjectName("ClientCard")
        card.setFixedHeight(180) 
        
        layout = QHBoxLayout(card)
        
        img_label = QLabel(); img_label.setFixedSize(100, 100)

        image_to_load = resource_path(img) if img else None
        if image_to_load and os.path.exists(image_to_load):
            pixmap = QPixmap(image_to_load)
            img_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            img_label.setStyleSheet("background-color: #e0e0e0; border-radius: 5px;")
        
        
        details_layout = QVBoxLayout()
        name_label = QLabel(f"{first} {last}", objectName="ClientName")
        details_layout.addWidget(name_label)
        
        grid_widget = QWidget()
        details_grid = QGridLayout(grid_widget)
        details_grid.setContentsMargins(0,0,0,0); details_grid.setSpacing(4); details_grid.setColumnStretch(0,1)

        details_grid.addWidget(QLabel(cin, alignment=Qt.AlignmentFlag.AlignLeft), 0, 0)
        details_grid.addWidget(QLabel("البطاقة الوطنية :", alignment=Qt.AlignmentFlag.AlignLeft), 0, 1)
        details_grid.addWidget(QLabel(phone, alignment=Qt.AlignmentFlag.AlignLeft), 1, 0)
        details_grid.addWidget(QLabel("رقم الهاتف :", alignment=Qt.AlignmentFlag.AlignLeft), 1, 1)
        details_grid.addWidget(QLabel(addr, alignment=Qt.AlignmentFlag.AlignLeft), 2, 0)
        details_grid.addWidget(QLabel("العنوان :", alignment=Qt.AlignmentFlag.AlignLeft), 2, 1)
        
        details_layout.addWidget(grid_widget)
        details_layout.addStretch()

        buttons = QVBoxLayout()
        btn_edit = QPushButton("Edit", objectName="EditButton")
        btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_del = QPushButton("Delete", objectName="DeleteButton")
        btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        
        btn_edit.clicked.connect(lambda: self.open_edit_employee_dialog(emp_id))
        btn_del.clicked.connect(lambda: self.delete_employee(emp_id))
        
        buttons.addWidget(btn_edit)
        buttons.addWidget(btn_del)
        buttons.addStretch()

        layout.addWidget(img_label)
        layout.addSpacing(15)
        layout.addLayout(details_layout, 1)
        layout.addLayout(buttons)
        return card
        
    def delete_employee(self, emp_id):
        reply = QMessageBox.question(self, 'Delete Employee', "Are you sure you want to delete this employee?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            db.delete_employee(emp_id)
            self.data_changed_signal.emit()

    def open_edit_employee_dialog(self, emp_id):
        emp_data = db.get_employee_by_id(emp_id)
        if not emp_data:
            QMessageBox.warning(self, "Error", "Could not retrieve employee data.")
            return

        dialog = EditEmployeeDialog(emp_data, self)
        if dialog.exec():
            updated_data = dialog.get_updated_data()
            try:
                db.update_employee(emp_id, updated_data)
                QMessageBox.information(self, "Success", "Employee details updated.")
                self.data_changed_signal.emit()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Could not update employee: {e}")

    def open_edit_admin_dialog(self):
        profile_data = db.get_admin_profile()

        dialog = EditAdminDialog(profile_data, self)
        if dialog.exec():
            updated_data = dialog.get_updated_data()
            try:
                db.update_admin_profile(updated_data)
                QMessageBox.information(self, "Success", "Admin profile updated.")
                self.data_changed_signal.emit()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Could not update profile: {e}")

