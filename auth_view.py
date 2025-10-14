from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFrame, QLabel, 
                             QLineEdit, QPushButton, QStackedWidget, QMessageBox,
                             QComboBox)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, pyqtSignal
import database as db

class AuthWindow(QDialog):
    login_successful = pyqtSignal(str)
    # --- NEW: Signal to notify when the theme is changed ---
    theme_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Driving School Management - Login")
        self.setWindowIcon(QIcon("auto-ecole.ico"))
        self.setFixedSize(500, 450)
        self.setObjectName("AuthWindow")

        main_layout = QVBoxLayout(self)
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget, 1) # Give stack view stretch priority

        login_widget = self._create_login_widget()
        register_widget = self._create_register_widget()

        self.stacked_widget.addWidget(login_widget)
        self.stacked_widget.addWidget(register_widget)
        
        # --- NEW: Create and add the theme switcher at the bottom ---
        bottom_layout = QHBoxLayout()
        theme_combo = QComboBox()
        theme_combo.addItems(["Light", "Dark"])
        theme_combo.currentTextChanged.connect(self.theme_changed.emit) # Emit the signal
        
        bottom_layout.addWidget(theme_combo)
        bottom_layout.addStretch() # Push combo box to the left
        main_layout.addLayout(bottom_layout)
        # --- End of NEW ---


    def _create_login_widget(self):
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        form_frame = QFrame()
        form_frame.setProperty("class", "card")
        form_layout = QVBoxLayout(form_frame)
        form_frame.setFixedWidth(350)

        title = QLabel("تسجيل الدخول")
        title.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Username or Company ID")
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_password.returnPressed.connect(self._login_event)

        btn_login = QPushButton("Login")
        btn_login.setObjectName("LoginButton")
        btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_login.clicked.connect(self._login_event)
        
        btn_go_to_register = QPushButton("إنشاء حساب جديد")
        btn_go_to_register.setObjectName("LinkButton")
        btn_go_to_register.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_go_to_register.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        form_layout.addWidget(title)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.login_username)
        form_layout.addWidget(self.login_password)
        form_layout.addSpacing(20)
        form_layout.addWidget(btn_login)
        form_layout.addWidget(btn_go_to_register)

        layout.addWidget(form_frame)
        return container

    def _create_register_widget(self):
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        form_frame = QFrame()
        form_frame.setProperty("class", "card")
        form_layout = QVBoxLayout(form_frame)
        form_frame.setFixedWidth(350)
        
        title = QLabel("إنشاء حساب")
        title.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.reg_fname = QLineEdit(); self.reg_fname.setPlaceholderText("First Name - الإسم الأول")
        self.reg_lname = QLineEdit(); self.reg_lname.setPlaceholderText("Last Name - الإسم العائلي")
        self.reg_username = QLineEdit(); self.reg_username.setPlaceholderText("Username - إسم المستخدم")
        self.reg_company_id = QLineEdit(); self.reg_company_id.setPlaceholderText("Company ID - رقم المؤسسة")
        self.reg_password = QLineEdit(); self.reg_password.setPlaceholderText("Password - كلمة السر")
        self.reg_password.setEchoMode(QLineEdit.EchoMode.Password)
        
        btn_register = QPushButton("Register")
        btn_register.setObjectName("RegisterButton")
        btn_register.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_register.clicked.connect(self._register_event)

        btn_go_to_login = QPushButton("عودة")
        btn_go_to_login.setObjectName("LinkButton")
        btn_go_to_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_go_to_login.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        form_layout.addWidget(title)
        form_layout.addWidget(self.reg_fname)
        form_layout.addWidget(self.reg_lname)
        form_layout.addWidget(self.reg_username)
        form_layout.addWidget(self.reg_company_id)
        form_layout.addWidget(self.reg_password)
        form_layout.addSpacing(20)
        form_layout.addWidget(btn_register)
        form_layout.addWidget(btn_go_to_login)

        layout.addWidget(form_frame)
        return container

    def _login_event(self):
        username = self.login_username.text()
        password = self.login_password.text()
        if not username or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter both username and password.")
            return

        role = db.check_login(username, password)
        if role:
            self.login_successful.emit(role)
            self.accept()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid credentials.")

    def _register_event(self):
        fname = self.reg_fname.text()
        lname = self.reg_lname.text()
        username = self.reg_username.text()
        company_id = self.reg_company_id.text()
        password = self.reg_password.text()

        if not all([fname, lname, username, company_id, password]):
            QMessageBox.warning(self, "Registration Failed", "All fields are required.")
            return
        
        if company_id != '5704':
            QMessageBox.critical(self, "Registration Failed", "Invalid Company ID.")
            return

        try:
            db.create_user(fname, lname, username, company_id, password)
            QMessageBox.information(self, "Success", "Account created successfully! You can now log in.")
            self.stacked_widget.setCurrentIndex(0)
        except Exception as e:
            QMessageBox.critical(self, "Registration Error", f"An error occurred: {e}")

