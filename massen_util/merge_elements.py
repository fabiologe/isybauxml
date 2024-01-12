from xml_parser import *
from typing import Union
from collections import defaultdict

def find_status(schacht_list, haltung_list):
    for Haltung in haltung_list:
        try:
            if Haltung.status == 1 and Haltung.status is not None:
                merger(schacht_list, haltung_list)
                print("Found planning objects")
        except ValueError:
            print("Could not find planning objects") 
                

def merger(schacht_list, haltung_list):
    massen_haltung = []
    print(f"Merging {len(set(h.objektbezeichnung for h in haltung_list))} Haltungen ....")
    for Haltung in haltung_list:
            zulauf_schacht = next((schacht for schacht in schacht_list if schacht.objektbezeichnung == Haltung.zulauf), None)
            ablauf_schacht = next((schacht for schacht in schacht_list if schacht.objektbezeichnung == Haltung.ablauf), None)
            if zulauf_schacht and ablauf_schacht:
                current_haltung = {
                    'Schacht Nr. oben': zulauf_schacht.objektbezeichnung,
                    'Deckelhoehe oben': float(zulauf_schacht.knoten[0].punkte[0].z),
                    'Sohlhoehe oben': float(zulauf_schacht.knoten[0].punkte[1].z),
                    'Schacht Nr. unten': ablauf_schacht.objektbezeichnung,
                    'Deckelhoehe unten': float(ablauf_schacht.knoten[0].punkte[0].z),
                    'Sohlhoehe unten': float(ablauf_schacht.knoten[0].punkte[1].z),
                }

                if Haltung.rohrlaenge is not None:
                    current_haltung["Laenge"] = float(Haltung.rohrlaenge)
                if Haltung.profilhoehe is not None:
                    current_haltung["DN"] = float(Haltung.profilhoehe)
                if Haltung.status is not None:
                    current_haltung["Status"]= Haltung.status

                massen_haltung.append(current_haltung)
            else:
                print("Either zulauf_schacht or ablauf_schacht could not be found in schacht_list.")
                print(f"Not found matching Schachts for Haltung {Haltung.objektbezeichnung}")
    seen = set()
    massen_haltung_unique  = []
    for item in massen_haltung:
 
        key = item['Schacht Nr. oben'], item['Schacht Nr. unten'] 
        if key not in seen:
            seen.add(key)
            massen_haltung_unique.append(item)
    return massen_haltung_unique


'''TO DO - bauwerks-merger'''



            
def sum_lengths(leitung_list):
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
            
