from xml_parser import *
from typing import Union
from collections import defaultdict

def find_status(schacht_list, haltung_list):
    for Haltung in haltung_list:
        try:
            if Haltung.status == 1 and Haltung.status is not None:
                mass_haltung(schacht_list, haltung_list)
                print("Found planning objects")
        except ValueError:
            print("Could not find planning objects") 
                
def mass_schacht(schacht_list, haltung_list):
    mass_schacht = []
    for schacht in schacht_list:
        zulauf = next((haltung for haltung in haltung_list if haltung.zulauf == schacht.objektbezeichnung), None)
        ablauf = next((haltung for haltung in haltung_list if haltung.ablauf == schacht.objektbezeichnung), None)
        if zulauf and ablauf:
            current_schacht = {
                'Schacht': schacht.objektbezeichnung,
                'Tiefe': schacht.schachttiefe
            }
            if zulauf.profilhoehe is not None:
                current_schacht['DN Zulauf'] = float(zulauf.profilhoehe)
            if ablauf.profilhoehe is not None:
                current_schacht['DN Ablauf'] = float(ablauf.profilhoehe)
            if schacht.anzahl_anschluesse >= 3:
                range = schacht.anzahl_anschluesse
                print(f'More then 2 connection at schacht:{schacht.objektbezeichung}')
                for i in range:
                    current_schacht['DN X'] = 0
            mass_schacht.append(current_schacht)
        else:
            if zulauf and not ablauf:
                print(f"Only one zulauf found for schacht: {schacht.objektbezeichnung}")
            elif not zulauf and ablauf:
                print(f"Only one ablauf found for schacht: {schacht.objektbezeichnung}")
            else:
                print(f"Neither zulauf nor ablauf found in haltung_list for schacht: {schacht.objektbezeichnung}")
    return mass_schacht



def mass_haltung(schacht_list, bauwerk_list, haltung_list):
    massen_haltung = []
    node_list= schacht_list + bauwerk_list
    print(f"Merging {len(set(h.objektbezeichnung for h in haltung_list))} Haltungen ....")
    for haltung in haltung_list:
            zulauf_schacht = next((node for node in node_list if node.objektbezeichnung == haltung.zulauf), None)
            ablauf_schacht = next((node for node in node_list if node.objektbezeichnung == haltung.ablauf), None)
            if zulauf_schacht and ablauf_schacht:
                current_haltung = {
                    'Schacht Nr. oben': zulauf_schacht.objektbezeichnung,
                    'Schacht Nr. unten': ablauf_schacht.objektbezeichnung,
                    'Deckelhoehe oben': float(zulauf_schacht.knoten[0].punkte[1].z),
                    'Deckelhoehe unten': float(ablauf_schacht.knoten[0].punkte[1].z)
                }
                if zulauf_schacht.knoten[0].punkte[1].z == 0.0: 
                    current_haltung["Deckelhoehe oben"] =  float(zulauf_schacht.knoten[0].punkte[0].z)
                    print(f"No DH for {zulauf_schacht.objektbezeichnung} using SH instead")
                if ablauf_schacht.knoten[0].punkte[1].z == 0.0:
                    current_haltung["Deckelhoehe unten"] =  float(ablauf_schacht.knoten[0].punkte[0].z)
                    print(f"No DH for {ablauf_schacht.objektbezeichnung} using SH instead")
                if haltung.zulauf_sh is not None:
                    current_haltung["Sohlhoehe oben"] = float(haltung.zulauf_sh)
                if haltung.ablauf_sh is not None:
                    current_haltung["Sohlhoehe unten"] = float(haltung.ablauf_sh)
                if haltung.rohrlaenge is not None:
                    current_haltung["Laenge"] = float(haltung.rohrlaenge)
                if haltung.profilhoehe is not None:
                    current_haltung["DN"] = float(haltung.profilhoehe)
                if haltung.status is not None:
                    current_haltung["Status"]= haltung.status

                massen_haltung.append(current_haltung)
            else:
                print("Either zulauf_schacht or ablauf_schacht could not be found in schacht_list.")
                print(f"Not found matching Schachts for Haltung {haltung.objektbezeichnung}")
    seen = set()
    mass_haltung_unique  = []
    for item in massen_haltung:
 
        key = item['Schacht Nr. oben'], item['Schacht Nr. unten'] 
        if key not in seen:
            seen.add(key)
            mass_haltung_unique.append(item)
    return mass_haltung_unique

            
def mass_leitung(leitung_list):
    plan_leitungen = {}
    for leitung in leitung_list:
        if leitung.status == '1':
            if leitung.profilhoehe in plan_leitungen:
                plan_leitungen[leitung.profilhoehe].append(leitung)
            else:
                plan_leitungen[leitung.profilhoehe] = [leitung]

    massen_leitung = []
    for profilhoehe, leitungen in plan_leitungen.items():
        sum_rohrlaenge = sum(leitung.laenge for leitung in leitungen if leitung.laenge is not None)
        current_leitung_type = {
            "Status": 1,
            "DN": profilhoehe,
            "Rohrlaenge": round(sum_rohrlaenge, 2)
        }
        massen_leitung.append(current_leitung_type)

    for current_leitung_type in massen_leitung:
        print(current_leitung_type)
    print(f'End of sum_lengths, massen_leitung: {massen_leitung}')
    return massen_leitung
            
