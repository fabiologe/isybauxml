
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
