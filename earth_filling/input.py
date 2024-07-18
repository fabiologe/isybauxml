import numpy as np
import pandas as pd
import ezdxf
import tkinter as tk
from tkinter import filedialog

class Handler:
    _readers = {}

    @staticmethod
    def select_file():
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=(("DXF files", "*.dxf"), ("CSV files", "*.csv"), ("All files", "*.*"))
        )
        return file_path

    @staticmethod
    def register_reader(extension, reader):
        Handler._readers[extension.lower()] = reader

    @staticmethod
    def read_file(file_path):
        extension = file_path.split('.')[-1].lower()
        if extension in Handler._readers:
            try:
                return Handler._readers[extension](file_path)
            except Exception as e:
                raise ValueError(f"Failed to read the file: {e}")
        else:
            raise ValueError(f"Unsupported file type: .{extension}")

def read_dxf(file_path):
    try:
        doc = ezdxf.readfile(file_path)
        msp = doc.modelspace()
        polylines = {}
        
        for entity in msp.query('LWPOLYLINE'):
            if entity.dxf.layer not in polylines:
                polylines[entity.dxf.layer] = []
            points = [(point[0], point[1], point[2] if len(point) > 2 else 0) for point in entity]
            polylines[entity.dxf.layer].append(points)
        
        unified_polylines = {name: np.array(points[0]) for name, points in polylines.items()}
        
        return unified_polylines
    except Exception as e:
        raise ValueError(f"Failed to read DXF file: {e}")

def read_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        grouped = data.groupby('Name')
        polylines = {}
        for name, group in grouped:
            polylines[name] = group[['X', 'Y', 'Z']].values
        
        return polylines
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {e}")

Handler.register_reader('dxf', read_dxf)
Handler.register_reader('csv', read_csv)
