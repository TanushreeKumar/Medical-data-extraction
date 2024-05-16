from pdf2image import convert_from_path
import pytesseract
import numpy as np 
import cv2 
from PIL import Image
import re



images= convert_from_path(r"C:\Users\Tanushree\OneDrive\Desktop\medical data extraction\Patient Details\jk 2.pdf")
for i in range(len(images)):
    images[i].save('jk2_'+str(i)+'.jpg','JPEG')



images



images[0].show()



pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
text = text = pytesseract.image_to_string(images[0],lang='eng')
print(text)



img = cv2.imread("jk2_0.jpg")
# Convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Apply threshold to convert to binary image
threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
# Pass the image through pytesseract
text = pytesseract.image_to_string(threshold_img)
# Print the extracted text
print(text)



import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    with Image.open(image_path) as img:
        extracted_text = pytesseract.image_to_string(img)
    return extracted_text

# Function to validate patient details
def validate_patient_details(image_path):
    # Extract patient details from the image
    extracted_text = extract_text_from_image(image_path)
    
    # Define patient details
    patient_details = {
        'Name': '',
        'Date': '',
        'Mobile': '',
        'Age/Sex':'',
        'Office ID':'',
        'Symptoms':'',
        'Findings':'',
        'Diagnosis':'',
        'Advised Investigation':'',
        'Instructions':''
        # Add more patient details as needed
    }

    # Extract patient details from the extracted text
    for key in patient_details:
        # Find the index of the key in the extracted text
        key_index = extracted_text.lower().find(key.lower())
        if key_index != -1:
            # Find the start index of the value associated with the key
            value_start_index = key_index + len(key)
            # Find the end index of the value associated with the key
            next_key_index = len(extracted_text)
            for next_key in patient_details.keys():
                next_key_occurrence = extracted_text.lower().find(next_key.lower(), key_index + len(key))
                if next_key_occurrence != -1 and next_key_occurrence < next_key_index:
                    next_key_index = next_key_occurrence
            # Extract the value from the text
            value = extracted_text[value_start_index:next_key_index].strip()
            patient_details[key] = value

    return patient_details

# Example usage
image_path = 'jk2_0.jpg'

# Validate patient details from the provided image
patient_details = validate_patient_details(image_path)

# Print the extracted patient details
print("Extracted Patient Details:")
for key, value in patient_details.items():
    print(f"{key}: {value}")




def create_test_dict_file(test_dict, folder_path):
    file_path = folder_path + '/test_dict.txt'
    with open(file_path, 'w', encoding='utf-8') as file:
        for package, tests in test_dict.items():
            total_cost_package = 0  # Initialize total cost for the package
            file.write(f"Package: {package}\n")
            for test, cost in tests.items():
                file.write(f"- {test}: ₹{cost}\n")
                total_cost_package += cost  # Accumulate test cost for the package
            file.write(f"Total Cost for {package}: ₹{total_cost_package}\n\n")
# Example usage:
test_dict = {
    'Package A': {'TSH': 300, 'Test A2': 75, 'Test A3': 100},
    'Package B': {'HbA1c': 299, 'Dexa Scan': 2800},
    'Package C': {'Test C1': 70, 'Test C2': 90, 'Test C3': 110, 'Test C4': 120}
}
folder_path = 'C:\\Users\\Tanushree\\OneDrive\\Desktop\\medical data extraction\\Patient Details'  # Replace '/path/to/your/folder' with the desired folder path
create_test_dict_file(test_dict, folder_path)



def extract_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text
# Example usage:
file_path = "C:\\Users\\Tanushree\\OneDrive\\Desktop\\medical data extraction\\Patient Details\\test_dict.txt"
file_text = extract_text_from_file(file_path)
print(file_text)



pip install fpdf



from PIL import Image
import pytesseract
from fpdf import FPDF
def extract_text_from_image(image_path):
    with Image.open(image_path) as img:
        extracted_text = pytesseract.image_to_string(img)
    return extracted_text
    
def validate_patient_details(image_path):
    # Extract patient details from the image
    extracted_text = extract_text_from_image(image_path)
    # Define patient details
    patient_details = {
        'Name': '',
        'Date': '',
        'Mobile': '',
        'Age/Sex':'',
        'Office ID':'',
        'Symptoms':'',
        'Findings':'',
        'Diagnosis':'',
        'Advised Investigation':'',
        # Add more patient details as needed
    }
    # Extract patient details from the extracted text
    for key in patient_details:
        # Find the index of the key in the extracted text
        key_index = extracted_text.lower().find(key.lower())
        if key_index != -1:
            # Find the start index of the value associated with the key
            value_start_index = key_index + len(key)
            # Find the end index of the value associated with the key
            next_key_index = len(extracted_text)
            for next_key in patient_details.keys():
                next_key_occurrence = extracted_text.lower().find(next_key.lower(), key_index + len(key))
                if next_key_occurrence != -1 and next_key_occurrence < next_key_index:
                    next_key_index = next_key_occurrence
            # Extract the value from the text
            value = extracted_text[value_start_index:next_key_index].strip()
            patient_details[key] = value
    return patient_details
    
def match_tests_with_packages(advised_investigation_tests, packages_dict):
    matching_tests = {}
    total_cost = 0  # Initialize total cost
    for package, tests in packages_dict.items():
        for test, cost in tests.items():
            if any(advised_test.lower() in test.lower() for advised_test in advised_investigation_tests):
                matching_tests[f"{test} in {package}"] = cost
                total_cost += cost
    return matching_tests, total_cost

def create_pdf(patient_details, matching_tests, total_cost):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add patient details to PDF
    pdf.cell(200, 10, txt="Extracted Patient Details:", ln=True, align="C")
    for key, value in patient_details.items():
        pdf.cell(200, 10, txt=f"{key}: {value}".encode('latin-1', 'replace').decode('latin-1'), ln=True)

    # Add matching tests with their costs to PDF
    pdf.cell(200, 10, txt="\nMatching Tests with Packages:", ln=True)
    for test, cost in matching_tests.items():
        pdf.cell(200, 10, txt=f"{test} cost is ₹{cost}".encode('latin-1', 'replace').decode('latin-1'), ln=True)
    pdf.cell(200, 10, txt=f"\nTotal Cost for all matching tests: ₹{total_cost}".encode('latin-1', 'replace').decode('latin-1'), ln=True)

    # Save the PDF
    pdf.output("C:/Users/Tanushree/OneDrive/Desktop/medical data extraction/Patient Details/patient_details.pdf", "F")

# Example usage
image_path = 'jk2_0.jpg'

# Validate patient details from the provided image
patient_details = validate_patient_details(image_path)

# Extracted advised investigation tests
advised_investigation_tests = ["HbA1c", "DEXA Scan"]

# Extracted packages and their tests with costs from the file
packages_dict = {
    'Package A': {'TSH': 300, 'Test A2': 75, 'Test A3': 100},
    'Package B': {'HbA1c': 299, 'Dexa Scan': 2800},
    'Package C': {'Test C1': 70, 'Test C2': 90, 'Test C3': 110, 'Test C4': 120}
}

# Match advised investigation tests with package tests and their costs
matching_tests, total_cost = match_tests_with_packages(advised_investigation_tests, packages_dict)

# Print the extracted patient details
print("Extracted Patient Details:")
for key, value in patient_details.items():
    print(f"{key}: {value}")

# Print the individual test costs along with their corresponding packages
if matching_tests:
    for test, cost in matching_tests.items():
        print(f"{test} cost is ₹{cost}")
    print(f"\nTotal Cost for all matching tests: ₹{total_cost}")
else:
    print("No matching tests found in the packages.")

# Create PDF with patient details and matching tests
create_pdf(patient_details, matching_tests, total_cost)



pip install reportlab



from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors

def preprocess_text(text):
    # Remove unwanted characters or patterns
    cleaned_text = text.replace("—__—_", "")
    return cleaned_text

def create_pdf(patient_details, matching_tests, total_cost, pdf_path):
    try:
        # Create a new PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        normal_style = styles['Normal']
        bold_style = styles['Heading1']
        bullet_style = styles['Bullet']

        # Define content for the PDF
        content = []

        # Add patient details to content
        content.append(Paragraph("<b>Patient Details</b>", bold_style))
        for key, value in patient_details.items():
            formatted_value = '<br/>'.join(value.split('\n'))  # Break multiline values
            cleaned_value = preprocess_text(formatted_value)  # Clean the value
            content.append(Paragraph(f"<b>{key}:</b> {cleaned_value}", normal_style))

        # Add matching tests with their costs to content
        content.append(Paragraph("<b>Matching Tests with Packages</b>", bold_style))
        for test, cost in matching_tests.items():
            cleaned_test = preprocess_text(test)  # Clean the test
            content.append(Paragraph(f"{cleaned_test} cost is \u20B9{cost}", normal_style))  # Unicode for ₹ symbol
        content.append(Paragraph(f"<b>Total Cost for all matching tests:</b> \u20B9{total_cost}", normal_style))  # Unicode for ₹ symbol

        # Build PDF document
        doc.build(content)

        print(f"PDF saved successfully to {pdf_path}")
    except Exception as e:
        print(f"Error creating PDF: {e}")

# Example usage
image_path = 'jk2_0.jpg'

# Validate patient details from the provided image
patient_details = validate_patient_details(image_path)

# Extracted advised investigation tests
advised_investigation_tests = ["HbA1c", "DEXA Scan"]

# Extracted packages and their tests with costs from the file
packages_dict = {
    'Package A': {'TSH': 300, 'Test A2': 75, 'Test A3': 100},
    'Package B': {'HbA1c': 299, 'Dexa Scan': 2800},
    'Package C': {'Test C1': 70, 'Test C2': 90, 'Test C3': 110, 'Test C4': 120}
}

# Match advised investigation tests with package tests and their costs
matching_tests, total_cost = match_tests_with_packages(advised_investigation_tests, packages_dict)

# Specify the path to save the PDF
pdf_path = 'C:/Users/Tanushree/OneDrive/Desktop/medical data extraction/Patient Details/patient_details.pdf'

# Create PDF with patient details and matching tests
create_pdf(patient_details, matching_tests, total_cost, pdf_path)



pip install mysql-connector-python



import mysql.connector
def create_database():
    try:
        # Connect to MySQL server (assuming it's running locally)
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tanu_@2305"
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Create the Clinic database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS Clinic")

        # Switch to the Clinic database
        cursor.execute("USE Clinic")

        # Create the Patient_Records table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Patient_Records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age VARCHAR(50),
                mobile VARCHAR(20),
                date VARCHAR(50),
                symptoms TEXT,
                advised_investigations TEXT,
                test_name VARCHAR(255),
                test_cost DECIMAL(10, 2)
            )
        """)

        # Commit changes and close the connection
        connection.commit()
        connection.close()
        print("Database and table created (if necessary).")
    except mysql.connector.Error as error:
        print(f"Error creating database: {error}")


def insert_records(patient_details, matching_tests, total_cost):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tanu_@2305",
            database="Clinic"
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Insert patient details into the Patient_Records table
        cursor.execute("""
            INSERT INTO Patient_Records (name, age, mobile, date, symptoms, advised_investigations, test_name, test_cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            patient_details['Name'],
            patient_details['Age/Sex'],
            patient_details['Mobile'],
            patient_details['Date'],
            patient_details['Symptoms'],
            ", ".join(advised_investigation_tests),  # Convert list to comma-separated string
            ", ".join(matching_tests.keys()),       # Convert test names to comma-separated string
            total_cost                               # Total cost of all matching tests
        ))

        # Commit changes and close the connection
        connection.commit()
        connection.close()
        print("Records inserted successfully.")
    except mysql.connector.Error as error:
        print(f"Error inserting records: {error}")


def match_tests_with_packages(advised_investigation_tests, packages_dict):
    matching_tests = {}
    total_cost = 0
    for package, tests_costs in packages_dict.items():
        for test, cost in tests_costs.items():
            if test in advised_investigation_tests:
                matching_tests[test] = cost
                total_cost += cost
    return matching_tests, total_cost

# Call the function to create the database and table
create_database()

# Example usage
# Assuming you have extracted patient details and advised investigation tests from the PDF
patient_details = {
    'Name': 'Jitender Kumar',
    'Age/Sex': 'Sty ’M',
    'Mobile': '9876543210',
    'Date': '28-12-2022',
    'Symptoms': 'Last consultation on (Sep 1, 2022)'
}

advised_investigation_tests = ["HbA1c", "DEXA Scan"]

packages_dict = {
    'Package A': {'TSH': 300, 'Test A2': 75, 'Test A3': 100},
    'Package B': {'HbA1c': 299, 'Dexa Scan': 2800},
    'Package C': {'Test C1': 70, 'Test C2': 90, 'Test C3': 110, 'Test C4': 120}
}

# Match advised investigation tests with package tests and their costs
matching_tests, total_cost = match_tests_with_packages(advised_investigation_tests, packages_dict)

# Insert records into the database
insert_records(patient_details, matching_tests, total_cost)
