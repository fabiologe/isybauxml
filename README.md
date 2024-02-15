# spartanic parser
it uses the german isybauxml 2001 format and storing it inside python classes ( which have the same logic structure as the schema) 

for example: manhole-cover (z-point) = schacht.knoten[0].punkte[0].z 


# small TO DO's: 
- fixing logic parentclass --> Knoten ---> Punkt
- clearify Aufbauform : 'E' ; 'R' ; 'Z' 
- adding raingage data
- reformatting xml_parser parentclasses to be more dynm.


# big TO DO's :
- some hydraulic calculation like the DWA A531 / pyswmm need to create an .inp from the data
- adding cost calculation and serialize to GAEB and adding an json based building specifications DB
- an serializer for ifc (currently struggeling with the creation of the geometrie but semantic is finished comming soon)
- an branch for working with elevation and survey data 


# install Windows : 
python -m venv venv

venv\Scripts\activate 

pip install -r requirements.txt