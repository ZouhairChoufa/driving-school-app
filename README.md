Driving School Management App (Customtkinter Version)
This is a desktop application for managing a driving school, built with Python and the Customtkinter library for a modern user interface.

# Features
Dashboard: View key statistics like total clients and employees at a glance.

Client Management: Add, edit, delete, and search for clients. Includes image uploads and contract generation.

Employee Management: Manage employee profiles, including personal details and photos.

Admin Profile: Update company and administrator details.

Data Export: Export client and employee lists to styled Excel files.

Multi-language Support: UI designed to handle both English and Arabic text.

# Technologies Used
Python: The core programming language.

Customtkinter: For creating the modern graphical user interface.

SQLite3: For the local database.

Pillow (PIL): For image processing and display.

Openpyxl: For creating and styling Excel files.

tkcalendar: For a simple calendar date picker widget.

arabic_reshaper & python-bidi: For correct rendering of Arabic text.

# Setup and Installation
Follow these steps to get the application running on your local machine.

1. Clone the repository:

git clone [https://github.com/ZouhairChoufa/driving-school-app.git](https://github.com/ZouhairChoufa/driving-school-app.git)
cd driving-school-app

2. Create and Activate a Virtual Environment:
It is highly recommended to use a virtual environment.

Windows:

python -m venv driving_school
.\driving_school\Scripts\activate

3. Install Dependencies:
Install all the required packages using the requirements.txt file.

pip install -r requirements.txt

# How to Run
Once the environment is activated and dependencies are installed, run the main application file from the project's root directory:

python main.py

The application will start, creating a driving_school.db database file if one does not exist.