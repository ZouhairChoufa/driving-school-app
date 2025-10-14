LIGHT_STYLE = """
/* Main window background */
QMainWindow {
    background-color: #f0f0f0;
}

/* --- General Card Style --- */
.card {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 15px;
    border: 1px solid #e0e0e0;
}

/* Sidebar styles */
#Sidebar {
    background-color: #e1e1e1;
    border-radius: 8px;
}
#Sidebar QLabel {
    color: #333;
    padding-right: 5px;
}
#Sidebar QComboBox {
    background-color: white;
    border: 1px solid #ccc;
    color: #333;
}

/* Navigation button styles */
#Sidebar QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px;
    text-align: left;
    border-radius: 5px;
    font-size: 14px;
}
#Sidebar QPushButton:hover {
    background-color: #2980b9;
}
#Sidebar QPushButton:checked { /* Style for the active button */
    background-color: #2c3e50; /* Darker blue for active */
}

/* --- General Content Styles --- */
.TitleLabel, #TitleLabel { /* Allow using as property or object name */
    font-size: 18px;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 10px;
}

/* --- Dashboard Page --- */
#WelcomeLabel {
    font-size: 24px;
    font-weight: bold;
    color: #2c3e50;
}
.StatLabel { font-size: 16px; color: #7f8c8d; }
.StatNumber { font-size: 48px; font-weight: bold; color: #2c3e50; }

/* --- Client & Admin Form Styles --- */
.form-container QLineEdit, .form-container QDateEdit, .form-container QComboBox,
QDialog QLineEdit, QDialog QDateEdit, QDialog QComboBox {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
    background-color: #fdfdfd;
    color: #333;
}
.form-container QLabel, QDialog QLabel {
    font-size: 14px;
    color: #333;
}

#SearchInput { padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; }

/* --- Button Styles --- */
QPushButton { 
    padding: 10px; 
    border-radius: 5px; 
    font-size: 14px; 
    color: white; 
    border: none;
    font-weight: bold;
}
#UploadButton { background-color: #95a5a6; }
#AddClientButton, #AddEmployeeButton { background-color: #2ecc71; }
#ExportButton { background-color: #16a085; }
#EditButton, #EditProfileButton { background-color: #3498db; }
#DeleteButton { background-color: #e74c3c; }
#PrintButton { background-color: #34495e; }

/* --- Client List Styles --- */
#ClientCard { 
    background-color: #f9f9f9; 
    border: 1px solid #eaeaea; 
    border-radius: 6px; 
    padding: 10px; 
    margin-bottom: 10px;
}
#ClientName { font-size: 18px; font-weight: bold; color: #2c3e50; }
#ClientDetailsLabel { font-size: 13px; color: #34495e; }

/* --- Admin Page Styles --- */
#CompanyProfile QLabel, #AdminName { 
    font-size: 14px; 
    color: #333;
}
#AdminName { font-weight: bold; }

/* --- QMessageBox Styles --- */
QMessageBox {
    background-color: #ffffff;
}
QMessageBox QLabel {
    color: #333333;
    font-size: 14px;
}
QMessageBox QPushButton {
    background-color: #3498db;
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 13px;
    min-width: 80px;
}
QMessageBox QPushButton:hover {
    background-color: #2980b9;
}
QDialog {
    background-color: #f0f0f0;
}

/* --- Auth Window Styles --- */
#AuthWindow QFrame.card {
    padding: 20px;
}
#AuthWindow QLabel {
    color: #333;
}
#AuthWindow QLineEdit {
    padding: 3px;
    font-size: 15px;
}
#AuthWindow #LoginButton, #AuthWindow #RegisterButton {
    background-color: #3498db;
    color: white;
    font-weight: bold;
}
#AuthWindow #LinkButton {
    background-color: transparent;
    color: #3498db;
    font-weight: normal;
    text-decoration: underline;
}
/* --- FIX: Added hover effect for the link button --- */
#AuthWindow #LinkButton:hover {
    color: #e74c3c; /* Red color on hover */
}
/* --- End of FIX --- */
"""

DARK_STYLE = """
/* Main window background */
QMainWindow {
    background-color: #2c3e50;
}

/* --- General Card Style --- */
.card {
    background-color: #34495e;
    border-radius: 8px;
    padding: 15px;
    border: 1px solid #4a6572;
}

/* Sidebar styles */
#Sidebar {
    background-color: #283747;
    border-radius: 8px;
}
#Sidebar QLabel {
    color: #ecf0f1;
    padding-right: 5px;
}
#Sidebar QComboBox {
    background-color: #2c3e50;
    border: 1px solid #7f8c8d;
    color: #ecf0f1;
}

/* Navigation button styles */
#Sidebar QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px;
    text-align: left;
    border-radius: 5px;
    font-size: 14px;
}
#Sidebar QPushButton:hover {
    background-color: #5dade2;
}
#Sidebar QPushButton:checked { /* Style for the active button */
    background-color: #85c1e9;
    color: #2c3e50;
}

/* --- General Content Styles --- */
.TitleLabel, #TitleLabel {
    font-size: 18px;
    font-weight: bold;
    color: #ecf0f1;
    margin-bottom: 10px;
}

/* --- Dashboard Page --- */
#WelcomeLabel {
    font-size: 24px;
    font-weight: bold;
    color: #ecf0f1;
}
.StatLabel { font-size: 16px; color: #bdc3c7; }
.StatNumber { font-size: 48px; font-weight: bold; color: #ecf0f1; }

/* --- Client & Admin Form Styles --- */
.form-container QLineEdit, .form-container QDateEdit, .form-container QComboBox,
QDialog QLineEdit, QDialog QDateEdit, QDialog QComboBox {
    padding: 8px;
    border: 1px solid #7f8c8d;
    border-radius: 4px;
    font-size: 14px;
    background-color: #2c3e50;
    color: #ecf0f1;
}
.form-container QLabel, QDialog QLabel {
    font-size: 14px;
    color: #ecf0f1;
}

#SearchInput { 
    padding: 8px; 
    border: 1px solid #7f8c8d; 
    border-radius: 4px; 
    font-size: 14px;
    background-color: #2c3e50;
    color: #ecf0f1;
}

/* --- Button Styles --- */
QPushButton { 
    padding: 10px; 
    border-radius: 5px; 
    font-size: 14px; 
    color: white; 
    border: none;
    font-weight: bold;
}
#UploadButton { background-color: #7f8c8d; }
#AddClientButton, #AddEmployeeButton { background-color: #27ae60; }
#ExportButton { background-color: #16a085; }
#EditButton, #EditProfileButton { background-color: #3498db; }
#DeleteButton { background-color: #c0392b; }
#PrintButton { background-color: #5dade2; color: #2c3e50; }

/* --- Client List Styles --- */
#ClientCard { 
    background-color: #4a6572; 
    border: 1px solid #5f7d8c; 
    border-radius: 6px; 
    padding: 10px; 
    margin-bottom: 10px;
}
#ClientName { font-size: 18px; font-weight: bold; color: #ecf0f1; }
#ClientDetailsLabel { font-size: 13px; color: #bdc3c7; }

/* --- Admin Page Styles --- */
#CompanyProfile QLabel, #AdminName { 
    font-size: 14px; 
    color: #ecf0f1;
}
#AdminName { font-weight: bold; }

/* --- QMessageBox Styles --- */
QMessageBox {
    background-color: #34495e;
}
QMessageBox QLabel {
    color: #ecf0f1;
    font-size: 14px;
}
QMessageBox QPushButton {
    background-color: #3498db;
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 13px;
    min-width: 80px;
}
QMessageBox QPushButton:hover {
    background-color: #5dade2;
}
QDialog {
    background-color: #2c3e50;
}

/* --- Auth Window Styles (Dark) --- */
#AuthWindow {
    background-color: #2c3e50;
}
#AuthWindow QFrame.card {
    background-color: #34495e;
    border-color: #4a6572;
    padding: 20px;
}
#AuthWindow QLabel {
    color: #ecf0f1;
}
#AuthWindow QLineEdit {
    padding: 3px;
    font-size: 15px;
    background-color: #2c3e50;
    border: 1px solid #7f8c8d;
    color: #ecf0f1;
}
#AuthWindow #LoginButton, #AuthWindow #RegisterButton {
    background-color: #3498db;
    color: white;
    font-weight: bold;
}
#AuthWindow #LinkButton {
    background-color: transparent;
    color: #5dade2;
    font-weight: normal;
    text-decoration: underline;
}
/* --- FIX: Added hover effect for the link button --- */
#AuthWindow #LinkButton:hover {
    color: #e74c3c; /* Red color on hover */
}
/* --- End of FIX --- */
"""

