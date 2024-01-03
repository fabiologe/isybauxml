from xml_parser.parse_all import all_lists
from datetime import datetime


class SimulationMetadata:
    def __init__(self, title, name):
        self.title = title
        self.name = name
        self.date = datetime.now().strftime('%Y-%m-%d')

    def to_title_string(self):
        return f"{self.title}\n{self.name}\n{self.date}\n"
    
def create_inp(metadata):
    with open("model.inp", "w") as f:
        f.write("[TITLE]\n")
        f.write(metadata.to_title_string())
        f.write("\n")
