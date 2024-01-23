from io import StringIO
from flask import Flask, request, jsonify, json, send_file
import requests
import csv
from datetime import datetime
import pandas as pd
from docx import Document
from flask_cors import CORS
from docx2pdf import convert

'''
'StringIO' To provide a file-like object interface to the CSV data stored in the 
 variable csv_content without the need to write it to a physical file on disk.
'request' to access incoming request data
'jsonify' to convert Python dictionaries to JSON responses
'pandas' for reading csv files into a data frame
'Document' for creating and manipulating word documents
'''

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/api/generate_report", methods=['POST'])

def generate_report():
    try:
    # Get form data from the request
       report_type = request.form.get('report_type')
       client = request.form.get('client')
       date = request.form.get('date')
       csv_file = request.files.get('csv_file')
       #pdf_file = request.files.get('pdf_file') if report_type == 'monthly' else None

     # Check if required fields are missing
       missing_fields = []
       if report_type is None:
         missing_fields.append("Report Type")
       if client is None:
         missing_fields.append("Client")
       if date is None:
         missing_fields.append("Date")

       if csv_file is None or not allowed_file(csv_file.filename):
         missing_fields.append("CSV File is missing or has an invalid extension.")

       if missing_fields:
         raise ValueError("Missing required fields: " + ", ".join(missing_fields))
       
       json_data = csv_to_json(csv_file)

      # Print the JSON data to the console
       print(json_data) 

       document = generate_word(report_type, client, date, json_data)

      # Save the Word document with a filename based on client name and selected date
       word_file = f"{report_type} {client} {date}.docx"
       document.save(word_file)

       pdf_file = f"{report_type} {client} {date}.pdf"
       convert(word_file, pdf_file)

      # send the file
       return send_file(word_file, as_attachment=True), send_file(pdf_file, as_attachment=True)


    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 400
     

def csv_to_json(csv_file):
    data = []

    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)

    return json.dumps(data, indent=2)



def generate_word(report_type, client, date, json_data):
   document  = Document("template.docx")
   return

def AbuseIPDB(IP):
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress':IP,
        'maxAgeInDays':'300',
    }

    headers = {
        'Accept': 'application/json',
        'Key': 'a583db48791dbdabf54a208dd89bdadc2bcd127c98d69fa45f9037ed965dd672f06bfd9d1db63be1'
    }

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)

    # Formatted output
    decodedResponse = json.loads(response.text)
    return ((decodedResponse["data"]))
   
app.run(host="0.0.0.0", port=5000, debug=True)

