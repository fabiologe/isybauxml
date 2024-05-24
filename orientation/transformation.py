from orientation.validate_CRS import find_CRS
from xml_parser import * 






def tranfsfrom_info():
    given_crs = find_CRS
    print('GK3= 31467 , GK2 = 31466 , UTM32N = 25832')
    print(f'From given CRS: {given_crs} to....?')
    trans_crs = int(input(f'Enter transform CRS as EPSG:'))
    return given_crs, trans_crs

def tranfsfrom_info(all_lists):
    given_crs, trans_crs = tranfsfrom_info()

    pass