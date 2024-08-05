from flask import Flask, request, send_file, jsonify
import os
from get_mass import process_xml_to_xsls
from xml_parser import * 
from pyproj import Proj, transform
import xml.dom.minidom
import json
import codecs
import traceback

app = Flask(__name__)
UPLOAD_DIRECTORY = "storage/input_xml"
OUTPUT_DIRECTORY = "storage/output_xml"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

'''
__________________
__________________
_____MAIN_________
creates the pycache for where the data gets stored
__________________
__________________
curl -X POST -F 'file=@/path/to/your/file.xml' http://yourserver.com/load_xml
__________________

'''
@app.route('/load_xml', methods = ['POST'])
def load_xml_route():
    file = request.files['file']
    if file:
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        file.save(file_path)
        
      
        xml_loader = XMLDataLoader(file_path)
        xml_data = xml_loader.get_data()
        
        if xml_data:
            root = xml_data.documentElement
            analysis_results = analyze_xml(root)
            print(analysis_results)
            parse_all(root)
            
            global schacht_list, all_lists
            
            print(f"Number of schacht items: {len(schacht_list)}")
            
            for data_list in all_lists:
                data_list = kill_duplicates(data_list, 'objektbezeichnung')
            
            return jsonify({"message": "XML loaded and processed successfully"})
        else:
            return jsonify({"error": "Error loading and processing XML file"}), 500
    return jsonify({"error": "No file uploaded"}), 400




'''
_________________
_________________
___USECASE FUNC1__
Extraction of Massdata and saving it as xsls for download
_________________
_________________

'''
@app.route('/get_mass', methods=['POST'])
def get_mass_route():
    try:
        result = process_xml_to_xsls(schacht_list, bauwerke_list, haltung_list)
        
        if result:
            return jsonify({"message": "File processed successfully", "file_path": result})
        else:
            return jsonify({"error": "Error processing XML file"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_xsls(filename):
    try:
        output_dir = "storage/output_xlsx_csv"
        return send_file(os.path.join(output_dir, filename), as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404



'''
_________________
_________________
___USECASE FUNC2__
Transforming the Crs of the input Xml 

curl -F "file=@storage/input_xml/scaling.xml" -F 'given_crs=31466' -F 'trans_crs=25832' -o ~/Downloads/transformed_scaling.xml http://localhost:5000/transform_crs

_________________
_________________

'''

CRS_MAPPING = {
    "31466": "GK2",
    "31467": "GK3",
    "25832": "UTM32N"
}
@app.route('/crs_mappings', methods=['GET'])
def get_crs_mappings():
    return jsonify(CRS_MAPPING)

@app.route('/transform_crs', methods=['POST'])
def transform_crs_route():
    file = request.files['file']
    if file:
        filename = file.filename
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        file.save(file_path)
        
        given_crs = request.form.get('given_crs')
        trans_crs = request.form.get('trans_crs')

        if not given_crs or not trans_crs:
            return jsonify({"error": "Both 'given_crs' and 'trans_crs' are required", "crs_mapping": CRS_mapping}), 400
        
        if given_crs not in CRS_MAPPING or trans_crs not in CRS_MAPPING:
            return jsonify({"error": "Invalid CRS provided", "crs_mapping": CRS_mapping}), 400
        
        try:
            with codecs.open(file_path, 'r', encoding='ISO-8859-1') as file:
                xml_content = file.read()
            
            fixed_content = umlaut_mapping(xml_content)
            fixed_content = bauwerk_fix(fixed_content)
            fixed_content = DN_bug(fixed_content)
        
            if isinstance(fixed_content, bytes):
                fixed_content = fixed_content.decode('ISO-8859-1')
            
            dom = xml.dom.minidom.parseString(fixed_content)
            replace_umlaut(dom)
            update_punkthoehe(dom)
            update_haltunghoehe(dom)
            delete_incomplete_points(dom)
            replace_umlaut(dom)
            print("tringing to get transform")
            print(given_crs)
            print(trans_crs)
            transform_crs(dom, given_crs, trans_crs)
            
            output_file_path = os.path.join(OUTPUT_DIRECTORY, filename)
            transformed_content = dom.toxml(encoding='ISO-8859-1')
            with open(output_file_path, 'wb') as file:
                file.write(transformed_content)
            
            return send_file(output_file_path, as_attachment=True)
        
            
            return jsonify({"message": "CRS transformation successful", "file_path": file_path}), 200
        
        except Exception as e:
            error_message = traceback.format_exc()
            print(f"Error processing file: {e}\n{error_message}")
            return jsonify({"error": f"Error processing file: {e}"}), 500
    
    return jsonify({"error": "No file provided"}), 400





if __name__ == '__main__':
    app.run(debug=True)