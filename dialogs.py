import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QGridLayout, QLabel, QLineEdit, 
                             QDateEdit, QComboBox, QPushButton, QHBoxLayout,
                             QMessageBox, QFileDialog, QScrollArea, QWidget)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QDate
import utils
from utils import resource_path # --- NEW: Import the helper function ---

class EditClientDialog(QDialog):
    """A dialog window for editing an existing client's details."""
    def __init__(self, client_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Client Details")
        # --- FIX: Use resource_path for the icon ---
        self.setWindowIcon(QIcon(resource_path("auto-ecole.ico")))
        self.setFixedWidth(550)
        self.setMaximumHeight(700)
        self.new_image_path = None
        
        # Unpack client data, adding a placeholder for the unused password column
        self.client_id, first, last, addr, phone, lic_type, self.original_image_path, _, _, bday, cin, h_prac, h_theo, v_mat, monitor, exam_date, *_ = client_data
        
        main_layout = QVBoxLayout(self)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        form_widget = QWidget()
        form = QGridLayout(form_widget)
        form.setSpacing(10)

        self.client_inputs = {
            'first_name': QLineEdit(first), 'last_name': QLineEdit(last), 'address': QLineEdit(addr),
            'birthday': QDateEdit(calendarPopup=True), 'cin': QLineEdit(cin), 'phone': QLineEdit(phone),
            'hours_practice': QLineEdit(str(h_prac)), 'hours_theory': QLineEdit(str(h_theo)),
            'vehicle_matricule': QLineEdit(v_mat), 'monitor_name': QLineEdit(monitor),
            'exam_success_date': QDateEdit(calendarPopup=True), 'license_type': QComboBox()
        }
        
        try:
            self.client_inputs['birthday'].setDate(QDate.fromString(bday, "dd/MM/yyyy"))
            self.client_inputs['exam_success_date'].setDate(QDate.fromString(exam_date, "dd/MM/yyyy"))
        except: # Fallback if date is invalid
            self.client_inputs['birthday'].setDate(QDate.currentDate())
            self.client_inputs['exam_success_date'].setDate(QDate.currentDate())

        self.client_inputs['license_type'].addItems(["(سيارة) B رخصة ", "(دراجة نارية) A رخصة", "(شاحنة) C رخصة"])
        self.client_inputs['license_type'].setCurrentText(lic_type)

        for key, widget in self.client_inputs.items():
            if isinstance(widget, QLineEdit):
                if key in ['first_name', 'last_name', 'address', 'monitor_name']:
                     widget.setAlignment(Qt.AlignmentFlag.AlignRight)
                else:
                     widget.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        labels = {
            'first_name': "الاسم الشخصي", 'last_name': "الاسم العائلي", 'address': "العنوان",
            'birthday': "تاريخ الإزدياد", 'cin': "رقم البطاقة الوطنية", 'phone': "رقم الهاتف",
            'hours_practice': "ساعات التدريب", 'hours_theory': "ساعات النظري",
            'vehicle_matricule': "رقم تسجيل المركبة", 'monitor_name': "إسم المدرب",
            'exam_success_date': "تاريخ النجاح في الإمتحان", 'license_type': "نوع الرخصة"
        }

        row = 0
        for key, ar_label in labels.items():
            ar_widget = QLabel(f"<b>{ar_label}</b>")
            ar_widget.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
            form.addWidget(ar_widget, row, 0, 1, 2)
            row += 1
            form.addWidget(self.client_inputs[key], row, 0, 1, 2)
            row += 1

        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area)

        upload_layout = QHBoxLayout()
        self.btn_upload_image = QPushButton("Upload Image", objectName="AddClientButton")
        self.btn_upload_image.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_upload_image.clicked.connect(self.upload_image)
        
        self.lbl_image_status = QLabel(os.path.basename(self.original_image_path) if self.original_image_path and os.path.exists(self.original_image_path) else "No Image Selected")
        
        upload_layout.addWidget(QLabel("<b>Client Image:</b>"))
        upload_layout.addWidget(self.lbl_image_status, 1)
        upload_layout.addWidget(self.btn_upload_image)
        main_layout.addLayout(upload_layout)

        button_layout = QHBoxLayout()
        btn_save = QPushButton("Save Changes", objectName="AddClientButton")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel = QPushButton("Cancel", objectName="DeleteButton")
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        
        button_layout.addStretch()
        button_layout.addWidget(btn_cancel)
        button_layout.addWidget(btn_save)
        
        main_layout.addLayout(button_layout)
        
        btn_save.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

    def get_updated_data(self):
        """Returns the updated data from the form fields."""
        data = {key: field.text() if isinstance(field, QLineEdit) else field.date().toString("dd/MM/yyyy") if isinstance(field, QDateEdit) else field.currentText() for key, field in self.client_inputs.items()}
        if self.new_image_path:
            data['image_path'] = self.new_image_path
        return data

    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            # Generate a more unique filename to prevent overwrites
            _, file_extension = os.path.splitext(file_name)
            new_filename = f"client_{self.client_id}_{QDate.currentDate().toString('yyyyMMdd')}{file_extension}"
            
            self.new_image_path = utils.copy_image_to_data_folder(file_name, fixed_filename=new_filename)
            if self.new_image_path:
                self.lbl_image_status.setText(os.path.basename(self.new_image_path))

class EditEmployeeDialog(QDialog):
    def __init__(self, emp_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Employee Details")
        # --- FIX: Use resource_path for the icon ---
        self.setWindowIcon(QIcon(resource_path("auto-ecole.ico")))
        self.setMinimumWidth(500)

        self.emp_id, first, last, bday, cin, phone, addr, _ = emp_data
        
        main_layout = QVBoxLayout(self)
        form_widget = QWidget()
        form = QGridLayout(form_widget)
        form.setSpacing(10)

        self.employee_inputs = {
            'first_name': QLineEdit(first), 'last_name': QLineEdit(last),
            'address': QLineEdit(addr), 'birthday': QDateEdit(calendarPopup=True),
            'cin': QLineEdit(cin), 'phone': QLineEdit(phone)
        }
        try:
            self.employee_inputs['birthday'].setDate(QDate.fromString(bday, "dd/MM/yyyy"))
        except:
            self.employee_inputs['birthday'].setDate(QDate.currentDate())
        
        labels = {
            'first_name': "الاسم الشخصي", 'last_name': "الاسم العائلي",
            'address': "العنوان", 'birthday': "تاريخ الإزدياد",
            'cin': "رقم البطاقة الوطنية", 'phone': "رقم الهاتف",
        }
        
        row = 0
        for key, ar_label in labels.items():
            ar_widget = QLabel(f"<b>{ar_label}</b>")
            ar_widget.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
            form.addWidget(ar_widget, row, 0, 1, 2)
            row += 1
            form.addWidget(self.employee_inputs[key], row, 0, 1, 2)
            row += 1

        main_layout.addWidget(form_widget)

        button_layout = QHBoxLayout()
        btn_save = QPushButton("Save Changes", objectName="AddEmployeeButton")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel = QPushButton("Cancel", objectName="DeleteButton")
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout.addStretch()
        button_layout.addWidget(btn_cancel)
        button_layout.addWidget(btn_save)
        main_layout.addLayout(button_layout)
        
        btn_save.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

    def get_updated_data(self):
        return {key: field.text() if isinstance(field, QLineEdit) else field.date().toString("dd/MM/yyyy") for key, field in self.employee_inputs.items()}

class EditAdminDialog(QDialog):
    def __init__(self, profile_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Company Profile")
        # --- FIX: Use resource_path for the icon ---
        self.setWindowIcon(QIcon(resource_path("auto-ecole.ico")))
        self.setMinimumWidth(500)
        self.new_image_path = None

        if profile_data:
            _, fname, lname, phone, addr, self.original_image_path, cname, cid, fax, email, _ = profile_data
        else: # Handle case where no profile exists yet
            fname, lname, phone, addr, self.original_image_path, cname, cid, fax, email = ("",)*9
            cid = 5704 # Default company ID
            cname = "Auto Ecole Abd El Karim"

        main_layout = QVBoxLayout(self)
        form_widget = QWidget()
        form = QGridLayout(form_widget)
        form.setSpacing(10)

        self.admin_inputs = {
            'first_name': QLineEdit(fname), 'last_name': QLineEdit(lname),
            'company_name': QLineEdit(cname), 'company_id': QLineEdit(str(cid)),
            'address': QLineEdit(addr), 'phone': QLineEdit(phone),
            'fax': QLineEdit(fax), 'email': QLineEdit(email),
        }

        labels = {
            'first_name': "First Name", 'last_name': "Last Name",
            'company_name': "Company Name", 'company_id': "Company ID",
            'address': "Address", 'phone': "Phone", 'fax': "Fax", 'email': "Email",
        }
        
        row = 0
        for key, label_text in labels.items():
            label = QLabel(f"<b>{label_text}</b>")
            form.addWidget(label, row, 0)
            form.addWidget(self.admin_inputs[key], row, 1)
            row += 1

        main_layout.addWidget(form_widget)

        upload_layout = QHBoxLayout()
        self.btn_upload_image = QPushButton("Upload Profile Image", objectName="AddClientButton")
        self.btn_upload_image.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_upload_image.clicked.connect(self.upload_image)
        self.lbl_image_status = QLabel(os.path.basename(self.original_image_path) if self.original_image_path else "No Image Selected")
        upload_layout.addWidget(QLabel("<b>Profile Image:</b>"))
        upload_layout.addWidget(self.lbl_image_status, 1)
        upload_layout.addWidget(self.btn_upload_image)
        main_layout.addLayout(upload_layout)

        button_layout = QHBoxLayout()
        btn_save = QPushButton("Save Changes", objectName="EditProfileButton")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel = QPushButton("Cancel", objectName="DeleteButton")
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout.addStretch()
        button_layout.addWidget(btn_cancel)
        button_layout.addWidget(btn_save)
        main_layout.addLayout(button_layout)
        
        btn_save.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)
        
    def get_updated_data(self):
        data = {key: field.text() for key, field in self.admin_inputs.items()}
        if self.new_image_path:
            data['image_path'] = self.new_image_path
        return data

    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            self.new_image_path = utils.copy_image_to_data_folder(file_name, fixed_filename="admin_profile.png")
            if self.new_image_path:
                self.lbl_image_status.setText(os.path.basename(self.new_image_path))


