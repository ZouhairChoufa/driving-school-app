from PyQt6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox
from PyQt6.QtCore import Qt
import database as db

class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DashboardPage")

        # Main container for this view
        content_widget = QFrame()
        content_widget.setProperty("class", "card")
        
        layout = QVBoxLayout(self)
        layout.addWidget(content_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Content Layout
        content_layout = QVBoxLayout(content_widget)
        
        welcome = QLabel("مرحبا بكم في مؤسسة عبد الكريم لتعليم السياقة", objectName="WelcomeLabel")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        stats_layout = QHBoxLayout()
        stats_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # # Client Stats
        # client_stat_layout = QVBoxLayout()
        # client_stat_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.lbl_total_clients_num = QLabel("0", objectName="StatNumber")
        # client_stat_layout.addWidget(QLabel("Total Clients", objectName="StatLabel"))
        # client_stat_layout.addWidget(self.lbl_total_clients_num)
        
        # # Employee Stats
        # employee_stat_layout = QVBoxLayout()
        # employee_stat_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.lbl_total_employees_num = QLabel("0", objectName="StatNumber")
        # employee_stat_layout.addWidget(QLabel("Total Employees", objectName="StatLabel"))
        # employee_stat_layout.addWidget(self.lbl_total_employees_num)
        
        self.setStyleSheet("""
            /* Style for the main container boxes */
            QGroupBox {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }

            /* Style for the descriptive text like "Total Clients" */
            QLabel#StatLabel {
                font-size: 27px;
                font-weight: bold;
                color: #555555; 
                qproperty-alignment: 'AlignCenter';
                padding: 0 20px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            /* Style for the main numbers like "0" */
            QLabel#StatNumber {
                font-size: 45px;
                font-weight: bold;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #000000; 
                qproperty-alignment: 'AlignCenter';
            }
        """)
        
        # --- Client Stats ---
        client_stat_layout = QVBoxLayout()
        self.lbl_total_clients_num = QLabel("0", objectName="StatNumber")
        client_stat_layout.addWidget(QLabel("Total Clients", objectName="StatLabel"))
        client_stat_layout.addWidget(self.lbl_total_clients_num)
        
        # --- Employee Stats ---
        employee_stat_layout = QVBoxLayout()
        self.lbl_total_employees_num = QLabel("0", objectName="StatNumber")
        employee_stat_layout.addWidget(QLabel("Total Employees", objectName="StatLabel"))
        employee_stat_layout.addWidget(self.lbl_total_employees_num)
        
        stats_layout.addLayout(client_stat_layout)
        stats_layout.addLayout(employee_stat_layout)
        
        content_layout.addWidget(welcome)
        content_layout.addStretch()
        content_layout.addLayout(stats_layout)
        content_layout.addStretch()
        
    def refresh_stats(self):
        """Fetches the latest stats from the database and updates the labels."""
        try:
            clients, employees = db.get_dashboard_stats()
            self.lbl_total_clients_num.setText(str(clients))
            self.lbl_total_employees_num.setText(str(employees))
        except Exception as e:
            print(f"Error refreshing dashboard stats: {e}")
