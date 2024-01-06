from io import StringIO
from flask import Flask, request, jsonify, send_file
from datetime import datetime
import os
import csv
import pandas as pd
import fitz  # pymupdf
from docx import Document
from flask_cors import CORS

# 'request' to access incoming request data
# 'jsonify' to convert Python dictionaries to JSON responses
# 'send_file' sends a file to the client for download
# 'OS' for file and directory operations
# 'csv' for reading a csv file
# 'pandas' for reading csv files into a data frame
# 'fitz' for opening and reading text from pdf files
# 'Document' for creating and manipulating word documents

app = Flask(__name__)
CORS(app)

@app.route("/api/generate_report", methods=['POST'])
def generate_report():
    # Get form data from the request

    report_type = request.form.get('report_type')
    client = request.form.get('client')
    date = request.form.get('date')
    csv_file = request.files.get('csv_file')
    pdf_file = request.files.get('pdf_file') if report_type == 'monthly' else None

    #file_path = r'C:\Users\salmahmoud\Desktop\Reporting\Backend\csv'
    #csv_file.save(file_path)

    if 'csv_file' not in request.files:
        return jsonify({'error': 'No file part'})

    if csv_file.filename == '':
        return jsonify({'error': 'No selected file'})

    if csv_file:
        # Read the CSV file from the in-memory file-like object
        csv_content = csv_file.read().decode('utf-8')
        
        # Check if the file is empty
        if not csv_content:
            return jsonify({'error': 'Empty file'})

        data = pd.read_csv(StringIO(csv_content))

        # Perform further operations on the 'data' DataFrame if needed

        # Example: Convert the DataFrame to JSON and print it
        data_json = data.to_json(orient='records')
        print(data_json)

        return jsonify({'success': True})

    # Check file types
   # if report_type == 'weekly' and csv_file and csv_file.filename.endswith('.csv'):
        
     #   word_file = weekly_report(data_js, client, date, report_type)

    #elif report_type == 'monthly' and csv_file and pdf_file and csv_file.filename.endswith('.csv') and pdf_file.filename.endswith('.pdf'):
       
       # word_file = monthly_report(data_js, pdf_file, client, date)
   # else:
        #return jsonify({'error': 'Invalid file type'}), 400


   # Save the files with the original filename
   # csv_file.save(os.path.join('CSV', csv_file.filename))
   # pdf_file.save(os.path.join('PDF', pdf_file.filename))

    


#def weekly_report(data_js, client, date, report_type):

    # Path to the word template
   # template_path = 'template path'

    # Generate Word file
   # doc = Document(template_path)
  #  doc.add_heading('Weekly Report', 0)
   # doc.add_paragraph(f'Client Name: {client}')
   # doc.add_paragraph(f'Date: {date}')

   # word_file = ''

  #  return send_file(word_file, download_name=f'{client}_{report_type}.docx')

    
app.run(host="0.0.0.0", port=5000, debug=True)

