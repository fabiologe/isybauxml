
def update_punkthoehe(dom):
    all_punkt_elements = dom.getElementsByTagName('Punkt')
    for punkt in all_punkt_elements:
        if not punkt.getElementsByTagName('Punkthoehe'):
            new_punkthoehe = dom.createElement('Punkthoehe')
            new_punkthoehe.appendChild(dom.createTextNode('0.00'))
            punkt.appendChild(new_punkthoehe)

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

