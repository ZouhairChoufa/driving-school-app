Driving School Management System (Gestion Auto Ecole)
This is a complete, standalone desktop application built with Python and PyQt6 to manage the operations of a driving school. It provides a clean, modern, and bilingual (Arabic/English) user interface for managing clients, employees, and company information.


# Features
Secure Authentication: A professional login and registration system to protect application data.

Role-Based Access: The "Admin" page and its functionalities are only visible and accessible to users with the 'Admin' role.

Dashboard: A clean home screen displaying key statistics like total clients and employees.

Client Management:

Add new clients with detailed information (name, address, license type, photo, etc.).

View all clients in a clean, scrollable list of cards.

Edit existing client information through a pop-up dialog.

Delete clients with a confirmation step.

Search for clients in real-time.

Export the client list to a styled Excel file.

Generate and print an HTML-based training contract for each client.

Admin Panel:

Company Profile Management: View and edit the driving school's information.

Employee Management: Add, view, edit, and delete employee records.

Export the employee list to Excel.

Modern UI:

A responsive and professional design.

Switchable Light and Dark themes.

Custom icons for a unique look and feel.


# Built With
Programming Language: Python

GUI Framework: PyQt6

Database: SQLite3

Libraries: Pillow (for images), openpyxl (for Excel)

# Getting Started
To run this project on your local machine, follow these steps.

Prerequisites
You must have Python installed on your system.

Installation & Setup
Clone the repository:

git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

Create and activate a virtual environment:

# For Windows
python -m venv venv
.\venv\Scripts\activate

Install the required dependencies:

pip install -r requirements.txt

Run the application:

python main.py

The application will start, and the database file (driving_school.db) will be automatically created in your Documents/GestionAutoEcole folder on the first run.

# Building the Executable
To package the application into a standalone .exe file for Windows, use the provided PyInstaller command.

Install PyInstaller:

pip install pyinstaller

Run the build command from the project's root directory:

pyinstaller --noconsole --onefile --name="Gestion Auto Ecole" --icon="auto-ecole.ico" --add-data "icons;icons" --add-data "images;images" main.py

The final executable will be located in the dist/ folder.