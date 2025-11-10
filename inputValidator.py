import os
import numpy as np


#validator function
def validate_input_file(file_path):
    #this checks if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[ERROR] File not found: {file_path}")
    
    try:
        points = np.loadtxt(file_path)
    except Exception as e:
        raise ValueError(f"[ERROR] Could not read the file '{file_path}': {e}")
    
    #make sure the file has the correct Nx2 format
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("[ERROR] Input file must have exactly two columns (x and y).")
    
    num_points = points.shape[0]

    #check the range
    if num_points > 4096:
        raise ValueError("[ERROR] Input exceeds 4096 locations (max allowed).")
    
    print(f"[SUCCESS] Loaded {num_points} locations successfully.")
    return points
