# spartanic parser
it uses the german isybauxml 2001 format and storing it inside python classes ( which have the same logic structure as the schema) 

for example: manhole-cover (z-point) = schacht.knoten[0].punkte[1].z 


# Currently working:
- Transform ISYBAUXML CRS to other CRS (needs as input EPSG(given) and EPSG(wanted) codes):
crs_transform.py
- extract ready to use CSV and xlsx mass data for overall cost calculation for Leitung; Haltung; Bauwerk and Schacht:
xxxxx.py
- an way of calculating an discharge of an container based on volume, height, diameter of the opening and plotting as csv and with matplot
/flow_creation/discharge.py



# small TO DO's: 
- reformatting xml_parser parentclasses to be more dynm.



# big TO DO's :
- some hydraulic calculation like the DWA A531 / pyswmm need to create an .inp from the data
- adding cost calculation and serialize to GAEB and adding an json based building specifications DB
- an serializer for ifc (currently struggeling with the creation of the geometrie but semantic is finished comming soon)
- an branch for working with elevation and survey data 
- 2D watershed runoff 


# install Windows : 
python -m venv venv

venv\Scripts\activate 

pip install -r requirements.txt

# install Linux : 
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
