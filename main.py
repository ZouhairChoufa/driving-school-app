import sys
import signal
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                            QVBoxLayout, QPushButton, QStackedWidget, QButtonGroup,
                            QLabel, QComboBox)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt

from views.dashboard_view import DashboardView
from views.clients_view import ClientsView
from views.admin_view import AdminView
from auth_view import AuthWindow 
from styles import LIGHT_STYLE, DARK_STYLE
import database as db
from utils import resource_path 

class MainWindow(QMainWindow):
    def __init__(self, app, user_role):
        super().__init__()
        self.app = app
        self.user_role = user_role

        self.setWindowTitle("Gestion - Auto Ecole Abd El Karim")
        self.setWindowIcon(QIcon(resource_path("auto-ecole.ico")))
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.sidebar = self._create_sidebar()
        self.stacked_widget = QStackedWidget()

        self.dashboard_page = DashboardView()
        self.clients_page = ClientsView()
        self.admin_page = AdminView()

        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.clients_page)
        
        if self.user_role == 'Admin':
            self.stacked_widget.addWidget(self.admin_page)

        main_layout.addWidget(self.sidebar, 1)
        main_layout.addWidget(self.stacked_widget, 5)

        self._connect_signals()
        self.dashboard_page.refresh_stats()

    def _create_sidebar(self):
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(15)

        school_title = QLabel("مؤسسة عبد الكريم لتعليم السياقة")
        school_title.setAlignment(Qt.AlignmentFlag.AlignRight)
        school_title.setFont(QFont("Arial", 12))

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_dashboard.setIcon(QIcon(resource_path("icons/dashboard.svg")))
        self.btn_dashboard.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_clients = QPushButton("Clients")
        self.btn_clients.setIcon(QIcon(resource_path("icons/clients.svg")))
        self.btn_clients.setCursor(Qt.CursorShape.PointingHandCursor)
        
        if self.user_role == 'Admin':
            self.btn_admin = QPushButton("Admin")
            self.btn_admin.setIcon(QIcon(resource_path("icons/admin.svg")))
            self.btn_admin.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.btn_admin = None

        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        
        buttons_to_add = [self.btn_dashboard, self.btn_clients]
        if self.btn_admin:
            buttons_to_add.append(self.btn_admin)
            
        for btn in buttons_to_add:
            btn.setCheckable(True)
            self.button_group.addButton(btn)

        self.btn_dashboard.setChecked(True)

        sidebar_layout.addWidget(school_title)
        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_clients)
        if self.btn_admin:
            sidebar_layout.addWidget(self.btn_admin)
        sidebar_layout.addStretch()

        theme_combo = QComboBox()
        theme_combo.addItems(["Light", "Dark"])
        theme_combo.currentTextChanged.connect(self._change_theme)
        sidebar_layout.addWidget(theme_combo)

        return sidebar_widget

    def _change_theme(self, theme_name):
        if theme_name == "Dark":
            self.app.setStyleSheet(DARK_STYLE)
        else:
            self.app.setStyleSheet(LIGHT_STYLE)

    def _connect_signals(self):
        self.btn_dashboard.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_clients.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        if self.btn_admin:
            self.btn_admin.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        
        self.clients_page.data_changed_signal.connect(self.on_data_changed)
        if self.user_role == 'Admin':
            self.admin_page.data_changed_signal.connect(self.on_data_changed)
    
    def on_data_changed(self):
        self.dashboard_page.refresh_stats()
        self.clients_page.refresh_client_list()
        if self.user_role == 'Admin':
            self.admin_page.refresh_employee_list()
            self.admin_page.refresh_admin_profile()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    app = QApplication(sys.argv)
    
    db.setup_database()
    
    app.setStyleSheet(LIGHT_STYLE)

    def change_auth_theme(theme_name):
        if theme_name == "Dark":
            app.setStyleSheet(DARK_STYLE)
        else:
            app.setStyleSheet(LIGHT_STYLE)

    auth_window = AuthWindow()
    auth_window.theme_changed.connect(change_auth_theme)

    login_info = {'role': ""} 
    def on_login(role):
        login_info['role'] = role

    auth_window.login_successful.connect(on_login)
    
    result = auth_window.exec()
    
    if result == 1 and login_info['role']:
        window = MainWindow(app, login_info['role'])
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)


