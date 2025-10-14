# -*- coding: utf-8 -*-
import os
import shutil
import webbrowser
import re
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import customtkinter
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
import arabic_reshaper
from bidi.algorithm import get_display

def export_to_excel(headers, data, default_filename="export.xlsx"):
    """Prompts user for a save location and exports data to a styled Excel file."""
    
    filepath = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        initialfile=default_filename
    )

    if not filepath: 
        return

    try:
        wb = Workbook()
        ws = wb.active
        
        header_font = Font(name='Calibri', size=12, bold=True, color='FFFFFF')
        header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')

        ws.append(headers)
        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill

        for row_data in data:
            ws.append(row_data)
        
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column].width = adjusted_width

        wb.save(filepath)
        messagebox.showinfo("Export Successful", f"Data successfully exported to\n{filepath}")

    except Exception as e:
        messagebox.showerror("Export Failed", f"An error occurred: {e}")


def handle_image_upload(preview_label, fixed_filename=None):
    """Handles image selection, copying, and updating a preview label."""
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
    if not path:
        return None
    
    os.makedirs("images", exist_ok=True)
    
    filename = fixed_filename if fixed_filename else os.path.basename(path)
    dest = os.path.join("images", filename)
    shutil.copy(path, dest)
    preview_label.configure(text=os.path.basename(dest))
    return dest

def get_image_for_card(image_path, size=(80, 80)):
    """Safely loads an image for display, providing a placeholder on failure."""
    try:
        if image_path and os.path.exists(image_path):
            return customtkinter.CTkImage(Image.open(image_path), size=size)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
    
    placeholder = Image.new("RGB", size, "#555")
    return customtkinter.CTkImage(placeholder, size=size)

def validate_and_format_date(date_string):
    """Validates and formats a date string to DD/MM/YYYY, returns empty for empty input."""
    if not date_string or not date_string.strip():
        return ""
    try:
        parts = date_string.replace('-', '/').replace('.', '/').strip().split('/')
        if len(parts) != 3: return None
        day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
        if year < 100: year += 2000 if year < 50 else 1900
        dt_object = datetime(year, month, day)
        return dt_object.strftime('%d/%m/%Y')
    except (ValueError, IndexError):
        return None

def validate_email(email_string):
    """Validates an email address format."""
    if not email_string.strip():
        return True # Allow empty email
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email_string) is not None

def generate_client_contract(client_data, company_details):
    """Generates an HTML contract for a client and opens it in a web browser."""
    if not client_data: return
    (client_id, fname, lname, address, phone, license_type, _, company_name, company_id, bday, cin, h_prac, h_theo, v_mat, exam_date , monitor) = client_data
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr" dir="rtl"><head><meta charset="UTF-8"><title>Contrat de Formation - {fname} {lname}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; margin: 40px; direction: rtl; text-align: right; border: 2px solid #000; padding: 30px; }}
        .header {{ text-align: center; margin-bottom: 40px; }} .header h1 {{ margin: 0; padding: 10px; border-bottom: 2px solid #000; }}
        .contract-section h2 {{ border-bottom: 1px solid #ccc; padding-bottom: 5px; }}
        .info-table {{ width: 100%; border-collapse: collapse; }} .info-table td {{ padding: 8px; border: 1px solid #ddd; }}
        .footer {{ margin-top: 50px; display: flex; justify-content: space-between; }}
        .signature-box {{ border-top: 1px solid #000; width: 250px; text-align: center; padding-top: 10px; }}
    </style></head>
    <body>
        <div class="header"><h1>عقد التكوين</h1><h2>{company_details.get('name', 'Auto Ecole Abd El Karim')}</h2></div>
        <h2>معلومات المترشح</h2>
        <table class="info-table">
            <tr><td>الإسم الكامل:</td><td>{fname} {lname}</td></tr> <tr><td>رقم البطاقة الوطنية:</td><td>{cin or 'N/A'}</td></tr>
            <tr><td>تاريخ الإزدياد:</td><td>{bday or 'N/A'}</td></tr> <tr><td>العنوان:</td><td>{address or 'N/A'}</td></tr>
        </table>
        <h2>تفاصيل التكوين</h2>
        <table class="info-table">
            <tr><td>معرف الشركة:</td><td>{company_id or 'N/A'}</td></tr>
            <tr><td>إسم الشركة:</td><td>{company_name or 'N/A'}</td></tr>
            <tr><td>نوع الرخصة:</td><td>{license_type}</td></tr>
            <tr><td>ساعات التدريب:</td><td>{h_prac} ساعة</td></tr>
            <tr><td>ساعات النظرية:</td><td>{h_theo} ساعة</td></tr>
            <tr><td>اسم المدرب:</td><td>{monitor}</td></tr>
            <tr><td>تاريخ النجاح فالإمتحان:</td><td>{exam_date}</td></tr>
        </table>
        <div class="footer"><div class="signature-box">توقيع المترشح</div><div class="signature-box">خاتم المؤسسة</div></div>
    </body></html>
    """
    contract_path = os.path.join("images", f"contract_{client_id}.html")
    with open(contract_path, "w", encoding="utf-8") as f: f.write(html_content)
    webbrowser.open(f'file://{os.path.realpath(contract_path)}')

def fix_arabic_text(text):
    """Corrects the display of Arabic text for GUI labels."""
    if not text:
        return ""
    reshaped_text = arabic_reshaper.reshape(str(text))
    bidi_text = get_display(reshaped_text)
    return bidi_text
