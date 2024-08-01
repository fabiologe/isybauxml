from flask import Flask, request, send_file, jsonify
import os
from get_mass import process_xml_to_xsls

app = Flask(__name__)
UPLOAD_DIRECTORY = "input_xml"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.route('/process-xml', methods=['POST'])
def process_xml_route():
    file = request.files['file']
    if file:
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        file.save(file_path)
        
      
        result = process_xml_to_xsls(file_path)
        
        if result:
            return jsonify({"message": "File processed successfully", "file_path": result})
        else:
            return jsonify({"error": "Error processing XML file"}), 500
    else:
        return jsonify({"error": "No file uploaded"}), 400

@app.route('/download/<filename>', methods=['GET'])
def download_xsls(filename):
    try:
        output_dir = "output_xlsx_csv"
        return send_file(os.path.join(output_dir, filename), as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
