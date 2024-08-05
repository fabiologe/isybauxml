from orientation.validate_CRS import find_CRSfromXML
from pyproj import Proj, transform
import re
import os

def bauwerk_fix(xml_content):
    pattern = r'<></>'
    fixed_content = re.sub(pattern,'', xml_content)
    return fixed_content

def umlaut_mapping(s):
    if isinstance(s, str):
        s = s.replace('Ä', 'Ae').replace('Ö', 'Oe').replace('Ü', 'Ue')
        s = s.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
        s = s.replace('ß', 'ss')
        s = s.replace('�', '_')
    
    return s
def DN_bug(xml_content):
    pattern = r'<Profilart>DN'
    fixed_content = re.sub(pattern,'<Profilart>0',xml_content)
    return fixed_content
    
def replace_umlaut(dom):
    for element in dom.getElementsByTagName('*'):
        for child in element.childNodes:
            if child.nodeType == child.TEXT_NODE:
                original_value = child.nodeValue
                new_value = umlaut_mapping(child.nodeValue)
                if original_value != new_value:
                    print(f"Replaced '{original_value}' with '{new_value}'")
                child.nodeValue = new_value
def update_punkthoehe(dom):
    all_punkt_elements = dom.getElementsByTagName('Punkt')
    for punkt in all_punkt_elements:
        if not punkt.getElementsByTagName('Punkthoehe'):
            new_punkthoehe = dom.createElement('Punkthoehe')
            new_punkthoehe.appendChild(dom.createTextNode('0.00'))
            punkt.appendChild(new_punkthoehe)

def dwa_to_isy(dom):
    all_status = dom.getElementsByTagName('Status')
    for status in all_status:
        if status.firstChild.nodeValue == "B":
            status.firstChild.nodeValue = 0
        elif status.firstChild.nodeValue == "P":
            status.firstChild.nodeValue = 1 

                 
def update_haltunghoehe(dom):
    all_start = dom.getElementsByTagName('Start')
    for punkt in all_start:
        if not punkt.getElementsByTagName('Punkthoehe'):
            new_starthoehe = dom.createElement('Punkthoehe')
            new_starthoehe.appendChild(dom.createTextNode('0.00'))
            punkt.appendChild(new_starthoehe)
    all_end = dom.getElementsByTagName('Ende')
    for punkt in all_end:
        if not punkt.getElementsByTagName('Punkthoehe'):
            new_endehoehe = dom.createElement('Punkthoehe')
            new_endehoehe.appendChild(dom.createTextNode('0.00'))
            punkt.appendChild(new_endehoehe)

def delete_incomplete_points(dom):
    all_punkt_elements = dom.getElementsByTagName('Punkt')
    for punkt in all_punkt_elements:
        punkthoehe = punkt.getElementsByTagName('Punkthoehe')
        rechtswert = punkt.getElementsByTagName('Rechtswert')
        hochwert = punkt.getElementsByTagName('Hochwert')
        
        if punkthoehe and not (rechtswert and hochwert):
            parent = punkt.parentNode
            parent.removeChild(punkt)
        #dom.unlink()       



def kill_duplicates(data_list, attribute):
    return list({getattr(item, attribute): item for item in data_list}.values())
'''def analyze_xml(root):
    """
    Analyze the XML structure and contents.
    
    Parameters:
        xml_root (Element): The root element of the XML document.
        
    Returns:
        dict: A dictionary containing analysis results.
    """
    # Count the number of different elements
    num_knoten_typ_0 = root.getElementsByTagName('KnotenTyp')[0].firstChild.nodeValue == int(0)
    num_knoten_typ_1 = root.getElementsByTagName('KnotenTyp')[0].firstChild.nodeValue == int(1)
    num_knoten_typ_2 = root.getElementsByTagName('KnotenTyp')[0].firstChild.nodeValue == int(2)
    num_kanten_typ_0 = root.getElementsByTagName('KantenTyp')[0].firstChild.nodeValue == int(0)
    num_kanten_typ_1 = root.getElementsByTagName('KantenTyp')[0].firstChild.nodeValue == int(1)
    
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        if num_knoten_typ_0:



    

    return analysis_results'''


def analyze_xml(root):
    """
    Analyze the XML structure and contents.
    
    Parameters:
        xml_root (Element): The root element of the XML document.
        
    Returns:
        dict: A dictionary containing analysis results.
    """
    # Initialize counters
    num_knoten_typ_0 = 0
    num_knoten_typ_1 = 0
    num_knoten_typ_2 = 0
    num_kanten_typ_0 = 0
    num_kanten_typ_1 = 0
    
    # Iterate over AbwassertechnischeAnlage elements
    for abwasser_objekt in root.getElementsByTagName('AbwassertechnischeAnlage'):
        # Check for KnotenTyp and increment counters
        try:
            knoten_typ_element = abwasser_objekt.getElementsByTagName('KnotenTyp')
            knoten_typ_value = int(knoten_typ_element[0].firstChild.nodeValue)
            if knoten_typ_value == 0:
                num_knoten_typ_0 += 1
            elif knoten_typ_value == 1:
                num_knoten_typ_1 += 1
            elif knoten_typ_value == 2:
                num_knoten_typ_2 += 1
        except:
            # Check for KantenTyp and increment counters
            kanten_typ_element = abwasser_objekt.getElementsByTagName('KantenTyp')
            kanten_typ_value = int(kanten_typ_element[0].firstChild.nodeValue)
            if kanten_typ_value == 0:
                num_kanten_typ_0 += 1
            elif kanten_typ_value == 1:
                num_kanten_typ_1 += 1
    
    # Prepare analysis results
    analysis_results = {
        "Schacht": num_knoten_typ_0,
        "Anschlusspunkt": num_knoten_typ_1,
        "Bauwerk": num_knoten_typ_2,
        "Haltung": num_kanten_typ_0,
        "Leitung": num_kanten_typ_1
    }

    return analysis_results


def transform_crs(dom, given_crs, trans_crs, output_dir, filename):
    all_points = []
    elements_to_update = []

    # Get all elements in the document
    all_elements = dom.getElementsByTagName('*')

    for element in all_elements:
        # Check if the element has both 'Rechtswert' and 'Hochwert' children
        rechtswert_elements = element.getElementsByTagName('Rechtswert')
        hochwert_elements = element.getElementsByTagName('Hochwert')

        if rechtswert_elements and hochwert_elements:
            rechtswert = float(rechtswert_elements[0].firstChild.nodeValue)
            hochwert = float(hochwert_elements[0].firstChild.nodeValue)

            all_points.append((rechtswert, hochwert))
            elements_to_update.append(element)
    
    # Print or process the original points before transformation
    print("Original Points:", all_points)
    print("Number of Points:", len(all_points))
    
    total_rechtswert = sum(point[0] for point in all_points)
    total_hochwert = sum(point[1] for point in all_points)
    count = len(all_points)
    
    if count == 0:
        return None
    
    source_proj = Proj(init=f'EPSG:{given_crs}')
    target_proj = Proj(init=f'EPSG:{trans_crs}')
    
    transformed_points = [transform(source_proj, target_proj, x, y) for x, y in all_points]
    
    # Print the transformed points
    print("Transformed Points:", transformed_points)
    
    # Update the XML with transformed coordinates
    for i, element in enumerate(elements_to_update):
        element.getElementsByTagName('Rechtswert')[0].firstChild.nodeValue = str(transformed_points[i][0])
        element.getElementsByTagName('Hochwert')[0].firstChild.nodeValue = str(transformed_points[i][1])
    
    # Save transformed XML to a file
    output_filename = os.path.join(output_dir, f"transformed_{filename}")
    with open(output_filename, 'w', encoding='ISO-8859-1') as f:
        f.write(dom.toxml())
    
    return output_filename