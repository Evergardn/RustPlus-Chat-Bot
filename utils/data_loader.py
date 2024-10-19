import json, os

def load_data():
    try:
        with open('data/data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("Error: File data.json not found.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON from data file.")
    
def get_cctv():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, '../data/cctv.json')
        with open(file_path, 'r') as f:
            codes = json.load(f)
        return (codes.get(key, []) for key in ["LargeOilCodes", "BanditCampCodes", "DomeCodes", "SiloCodes", "OutpostCodes", "SmoilCodes"])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading CCTV codes: {e}")
        return [], [], [], [], [], []