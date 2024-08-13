from xml_parser import *
from typing import Union, List
from collections import defaultdict
from earth_filling.area_polygon import AreaCalculator
from earth_filling.vol_polygon import VolumeCalculator


def find_status(schacht_list, haltung_list):
    for Haltung in haltung_list:
        try:
            if Haltung.status == 1 and Haltung.status is not None:
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
            zulauf_schacht = next((schacht for schacht in schacht_list if schacht.objektbezeichnung == haltung.zulauf), None)
            ablauf_schacht = next((schacht for schacht in schacht_list if schacht.objektbezeichnung == haltung.ablauf), None)
            if not zulauf_schacht:
                print(f"Zulauf node not found: {haltung.zulauf}")
            if not ablauf_schacht:
                print(f"Ablauf node not found: {haltung.ablauf}")
            if zulauf_schacht and ablauf_schacht:
                current_haltung = {
                    'Knoten Nr. oben': zulauf_schacht.objektbezeichnung,
                    'Knoten Nr. unten': ablauf_schacht.objektbezeichnung,
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
                print(f'Zulauf-Schacht in CLASS: {haltung.ablauf}')
                print(f'Ablauf-Schacht in CLASS: {haltung.zulauf}')
            zulauf_bauwerk = next((bauwerk for bauwerk in bauwerk_list if bauwerk.objektbezeichnung == haltung.zulauf), None)
            ablauf_bauwerk = next((bauwerk for bauwerk in bauwerk_list if bauwerk.objektbezeichnung == haltung.ablauf), None)
            if not zulauf_bauwerk:
                print(f"Zulauf node not found: {haltung.zulauf}")
            if not ablauf_bauwerk:
                print(f"Ablauf node not found: {haltung.ablauf}")
            if zulauf_bauwerk and ablauf_bauwerk:
                current_haltung_bauwerk = {
                    'Knoten Nr. oben': zulauf_bauwerk.objektbezeichnung,
                    'Knoten Nr. unten': ablauf_bauwerk.objektbezeichnung,
                    'Deckelhoehe oben': float(zulauf_bauwerk.knoten[0].punkte[1].z),
                    'Deckelhoehe unten': float(ablauf_bauwerk.knoten[0].punkte[1].z) 
                }
                if zulauf_bauwerk.knoten[0].punkte[1].z == 0.0: 
                    current_haltung["Deckelhoehe oben"] =  float(zulauf_bauwerk.knoten[0].punkte[0].z)
                    print(f"No DH for {zulauf_bauwerk.objektbezeichnung} using SH instead")
                if ablauf_bauwerk.knoten[0].punkte[1].z == 0.0:
                    current_haltung["Deckelhoehe unten"] =  float(ablauf_bauwerk.knoten[0].punkte[0].z)
                    print(f"No DH for {ablauf_bauwerk.objektbezeichnung} using SH instead")
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

                massen_haltung.append(current_haltung_bauwerk)
            else:
                print("Either zulauf_schacht or ablauf_schacht could not be found in schacht_list.")   
                print(f"Not found matching Schachts for Haltung {haltung.objektbezeichnung}")
                print(f'Zulauf-Schacht in CLASS: {haltung.ablauf}')
                print(f'Ablauf-Schacht in CLASS: {haltung.zulauf}')
    seen = set()
    mass_haltung_unique  = []
    for item in massen_haltung:
 
        key = item['Knoten Nr. oben'], item['Knoten Nr. unten'] 
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
            
def mass_bauwerk(bauwerk_list):
    massen_bauwerk = []
    print("This is MassBauwerk")
    for bauwerk in bauwerk_list:
    
        Bauwerk= bauwerk.objektbezeichnung 
       
        Status = bauwerk.status
        if Status == None:
            Status = 0
        isyCode = bauwerk.bauwerktyp
        Bauwerkart = bauwerktypENUM(isyCode).name
        dh = bauwerk.knoten[0].punkte[0].z
        sh = bauwerk.knoten[0].punkte[1].z
        Tiefe = sh- dh
       
        coords = []
        for poly in bauwerk.polygon:
            for point in poly:
                X=point.x
                Y=point.y
                Z=point.z
            coords.append((X,Y,Z))
    
        area = AreaCalculator.shoelace_formula([(x, y) for x, y, z in coords])
        
        vol = VolumeCalculator(area, height=Tiefe, slope=1.5)
        volume_rect = vol.calculate_rect()
       
        volume_trap = vol.calculate_trap()
       
        current_bauwerk = {
            "Status": Status,
            "Bauwerk": Bauwerk,
            "Bauwerkart": Bauwerkart,
            "Tiefe": Tiefe,
            "Breite OK": 0,
            "Laenge OK": 0,
            "Flaeche OK":  round(area, 2),
            "Flaeche UK": 0,
            "Volumen 1": round(volume_rect, 2),
            "Volumen 2": round(volume_trap,2)}
        massen_bauwerk.append(current_bauwerk)
    print(massen_bauwerk)
    return massen_bauwerk
                
                
