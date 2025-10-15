import os
import shutil
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QLineEdit, 
                             QDateEdit, QComboBox, QPushButton, QScrollArea, 
                             QFileDialog, QMessageBox, QGridLayout)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QDate, pyqtSignal
import database as db
import utils  
from utils import resource_path
from dialogs import EditClientDialog 

class ClientsView(QWidget):
    data_changed_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ClientsPage")
        self.current_client_image_path = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        self.client_form = self._create_client_form()
        self.client_list_view = self._create_client_list_view()

        layout.addWidget(self.client_form, 2)
        layout.addWidget(self.client_list_view, 3)
        
        self.btn_add_client.clicked.connect(self.add_new_client)
        self.btn_upload_client_image.clicked.connect(self.upload_client_image)
        self.search_input.textChanged.connect(self.refresh_client_list)
        self.btn_export.clicked.connect(self.export_clients_to_excel) # Connect export button

        self.refresh_client_list()

    def _create_client_form(self):
        container = QFrame()
        container.setProperty("class", "form-container card")
        main_layout = QVBoxLayout(container)
        
        title = QLabel("إضافة زبون جديد")
        title.setStyleSheet("""
            background-color: #3498db; 
            color: white;            
            font-family: Arial;      
            font-size: 20px;         
            font-weight: bold;       
            padding: 8px;            
            border-radius: 10px;       
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        form_content_widget = QWidget()
        form_content_layout = QVBoxLayout(form_content_widget)
        form_content_layout.setSpacing(10)
        
        grid_widget = QWidget()
        form = QGridLayout(grid_widget)
        form.setSpacing(10)

        self.client_inputs = {
            'first_name': QLineEdit(), 'last_name': QLineEdit(), 'address': QLineEdit(),
            'birthday': QDateEdit(calendarPopup=True), 'cin': QLineEdit(), 'phone': QLineEdit(),
            'hours_practice': QLineEdit("20"), 'hours_theory': QLineEdit("20"),
            'vehicle_matricule': QLineEdit("82-أ-6958"), 'monitor_name': QLineEdit("خالد الغموري"),
            'exam_success_date': QDateEdit(calendarPopup=True), 'license_type': QComboBox()
        }
        
        for key in ['hours_practice', 'hours_theory', 'vehicle_matricule', 'monitor_name']:
            self.client_inputs[key].setEnabled(False)

        self.client_inputs['license_type'].addItems(["(سيارة) B رخصة ", "(دراجة نارية) A رخصة", "(شاحنة) C رخصة"])
        self.client_inputs['birthday'].setDate(QDate.currentDate())
        self.client_inputs['exam_success_date'].setDate(QDate.currentDate())

        for key, widget in self.client_inputs.items():
            if isinstance(widget, QLineEdit):
                if key in ['first_name', 'last_name', 'address', 'monitor_name']:
                    widget.setAlignment(Qt.AlignmentFlag.AlignLeft)
                else:
                    widget.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.client_inputs['first_name'].setPlaceholderText("First Name")
        self.client_inputs['last_name'].setPlaceholderText("Last Name")
        self.client_inputs['address'].setPlaceholderText("Address")
        self.client_inputs['cin'].setPlaceholderText("CIN")
        self.client_inputs['phone'].setPlaceholderText("Phone Number")
        
        labels = {
            'first_name': "الاسم الشخصي", 'last_name': "الاسم العائلي",
            'address': "العنوان", 'birthday': "تاريخ الإزدياد",
            'cin': "رقم البطاقة الوطنية", 'phone': "رقم الهاتف",
            'hours_practice': "ساعات التدريب", 'hours_theory': "ساعات النظري",
            'vehicle_matricule': "رقم تسجيل المركبة", 'monitor_name': "إسم المدرب",
            'exam_success_date': "تاريخ النجاح في الإمتحان", 'license_type': "نوع الرخصة"
        }

        row = 0
        for key, ar_label in labels.items():
            ar_widget = QLabel(f"<b>{ar_label}</b>")
            ar_widget.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
            
            form.addWidget(ar_widget, row, 0, 1, 2)
            row += 1
            
            form.addWidget(self.client_inputs[key], row, 0, 1, 2)
            row += 1
        
        form_content_layout.addWidget(grid_widget)
        scroll.setWidget(form_content_widget)
        main_layout.addWidget(scroll)

        upload_layout = QHBoxLayout()
        self.btn_upload_client_image = QPushButton("Upload Image", objectName="UploadButton")
        self.btn_upload_client_image.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lbl_client_image = QLabel("No Image Selected")
        self.lbl_client_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_layout.addWidget(self.btn_upload_client_image)
        upload_layout.addWidget(self.lbl_client_image, 1)
        main_layout.addLayout(upload_layout)
        
        self.btn_add_client = QPushButton("إضافة زبون", objectName="AddClientButton")
        self.btn_add_client.setCursor(Qt.CursorShape.PointingHandCursor)
        main_layout.addWidget(self.btn_add_client, alignment=Qt.AlignmentFlag.AlignCenter)
        
        return container

    def _create_client_list_view(self):
        container = QFrame()
        container.setProperty("class", "card")
        layout = QVBoxLayout(container)
        
        top_bar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, phone, or CIN...")
        self.search_input.setObjectName("SearchInput")
        
        self.btn_export = QPushButton("Export to Excel", objectName="ExportButton")
        self.btn_export.setCursor(Qt.CursorShape.PointingHandCursor)
        top_bar.addWidget(self.search_input)
        top_bar.addWidget(self.btn_export)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        self.client_list_widget = QWidget()
        scroll.setWidget(self.client_list_widget)
        self.client_list_layout = QVBoxLayout(self.client_list_widget)
        self.client_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addLayout(top_bar)
        layout.addWidget(scroll)
        return container

    def refresh_client_list(self):
        for i in reversed(range(self.client_list_layout.count())): 
            self.client_list_layout.itemAt(i).widget().setParent(None)
        
        search_term = self.search_input.text()
        clients = db.get_clients(search_term)
        for client_data in clients:
            card = self._create_client_card(client_data)
            self.client_list_layout.addWidget(card)
            
    def add_new_client(self):
        data = {key: field.text() if isinstance(field, QLineEdit) else field.date().toString("dd/MM/yyyy") if isinstance(field, QDateEdit) else field.currentText() for key, field in self.client_inputs.items()}
        data['image_path'] = self.current_client_image_path
        data['company_name'] = 'Auto Ecole Abd El Karim'
        data['company_id'] = 5704

        if not data['first_name'] or not data['last_name']:
            QMessageBox.warning(self, "Input Error", "First and Last name are required.")
            return

        try:
            db.add_client(data)
            QMessageBox.information(self, "Success", "Client added successfully!")
            self.clear_form()
            self.data_changed_signal.emit()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not add client: {e}")

    def upload_client_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            new_path = utils.copy_image_to_data_folder(file_name)
            if new_path:
                self.current_client_image_path = new_path
                self.lbl_client_image.setText(os.path.basename(new_path))

    def delete_client(self, client_id):
        reply = QMessageBox.question(self, 'Delete Client', "Are you sure you want to delete this client?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            db.delete_client(client_id)
            self.data_changed_signal.emit()

    def clear_form(self):
        for widget in self.client_inputs.values():
            if isinstance(widget, QLineEdit): widget.clear()
            elif isinstance(widget, QDateEdit): widget.setDate(QDate.currentDate())
            elif isinstance(widget, QComboBox): widget.setCurrentIndex(0)

        self.lbl_client_image.setText("No Image Selected")
        self.current_client_image_path = None

    def _create_client_card(self, client_data):
        client_id, first, last, addr, phone, lic_type, img, _, _, bday, cin, *_ = client_data
        
        card = QFrame(); card.setObjectName("ClientCard")
        card.setFixedHeight(255)
        
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
        if any('\u0600' <= char <= '\u06FF' for char in f"{first}{last}"):
            name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        else:
            name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        details_layout.addWidget(name_label)
        
        grid_widget = QWidget()
        details_grid = QGridLayout(grid_widget)
        details_grid.setContentsMargins(0, 0, 0, 0)
        details_grid.setSpacing(4)
        details_grid.setColumnStretch(0, 1)
        
# --- FIX: Replaced the layout logic with the new inline version ---
        details_grid.addWidget(QLabel(cin, objectName="ClientDetailsLabel", alignment=Qt.AlignmentFlag.AlignLeft), 0, 0)
        details_grid.addWidget(QLabel("البطاقة الوطنية :", objectName="ClientDetailsLabel", alignment=Qt.AlignmentFlag.AlignRight), 0, 1)

        details_grid.addWidget(QLabel(phone, objectName="ClientDetailsLabel", alignment=Qt.AlignmentFlag.AlignLeft), 1, 0)
        details_grid.addWidget(QLabel("رقم الهاتف :", objectName="ClientDetailsLabel", alignment=Qt.AlignmentFlag.AlignRight), 1, 1)

        details_grid.addWidget(QLabel(bday, objectName="ClientDetailsLabel", alignment=Qt.AlignmentFlag.AlignLeft), 2, 0)
        details_grid.addWidget(QLabel("تاريخ الإزدياد :", objectName="ClientDetailsLabel", alignment=Qt.AlignmentFlag.AlignRight), 2, 1)
        
        details_grid.addWidget(QLabel(addr, objectName="ClientDetailsLabel", alignment=Qt.AlignmentFlag.AlignLeft), 3, 0)
        details_grid.addWidget(QLabel("العنوان :", objectName="ClientDetailsLabel", alignment=Qt.AlignmentFlag.AlignRight), 3, 1)

        details_grid.addWidget(QLabel(lic_type, objectName="ClientDetailsLabel", alignment=Qt.AlignmentFlag.AlignLeft), 4, 0)
        details_grid.addWidget(QLabel("نوع الرخصة :", objectName="ClientDetailsLabel", alignment=Qt.AlignmentFlag.AlignRight), 4, 1)
        # --- End of FIX ---

        details_layout.addWidget(grid_widget)
        details_layout.addStretch()

        buttons = QVBoxLayout()
        buttons.setSpacing(5)
        btn_edit = QPushButton("Edit", objectName="EditButton")
        btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_del = QPushButton("Delete", objectName="DeleteButton")
        btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_print = QPushButton("Print Contract", objectName="PrintButton")
        btn_print.setCursor(Qt.CursorShape.PointingHandCursor)
        
        btn_edit.clicked.connect(lambda: self.open_edit_dialog(client_id))
        btn_del.clicked.connect(lambda: self.delete_client(client_id))
        btn_print.clicked.connect(lambda: self.print_client_contract(client_id))
        
        buttons.addWidget(btn_edit)
        buttons.addWidget(btn_del)
        buttons.addWidget(btn_print)
        buttons.addStretch()

        layout.addWidget(img_label)
        layout.addSpacing(15)
        layout.addLayout(details_layout, 1)
        layout.addLayout(buttons)
        return card
    
    
    def open_edit_dialog(self, client_id):
        """Opens a dialog to edit the details of a specific client."""
        client_data = db.get_client_by_id(client_id)
        if not client_data:
            QMessageBox.warning(self, "Error", "Could not retrieve client data.")
            return

        dialog = EditClientDialog(client_data, self)
        
        # The exec() method shows the dialog and waits until the user closes it.
        # It returns True if the user clicked "Save" (accepted), and False otherwise.
        if dialog.exec():
            updated_data = dialog.get_updated_data()
            try:
                db.update_client(client_id, updated_data)
                QMessageBox.information(self, "Success", "Client details updated successfully.")
                self.data_changed_signal.emit() # Refresh the UI
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Could not update client: {e}")

    def print_client_contract(self, client_id):
        client_data = db.get_client_by_id(client_id)
        # This assumes get_admin_profile returns a dictionary-like object or None
        admin_profile = db.get_admin_profile()
        company_details = {'name': 'Auto Ecole Abd El Karim'} # Default
        if admin_profile:
            # Assuming admin_profile tuple indices for name and other details
            company_details['name'] = admin_profile[6] 

        if client_data:
            utils.generate_client_contract(client_data, company_details)
        else:
            QMessageBox.warning(self, "Error", "Could not retrieve client data for contract.")

    def export_clients_to_excel(self):
        headers = ["ID", "First Name", "Last Name", "Birthday", "CIN", "Phone", "Address", "License Type"]
        clients_data = db.get_clients()
        data_to_export = []
        for c in clients_data:
            # Corresponds to headers: id, first, last, bday, cin, phone, addr, lic_type
            data_to_export.append([c[0], c[1], c[2], c[9], c[10], c[4], c[3], c[5]])
            
        utils.export_to_excel_qt(headers, data_to_export, "clients_export.xlsx", self)


