from io import StringIO
from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
from docx import Document
from flask_cors import CORS

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

app.run(host="0.0.0.0", port=5000, debug=True)