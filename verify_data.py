import os
import sys
import pandas as pd

def check_data():
    """Check the existence and contents of the data file"""
    
    required_files = {
        'Bank.csv': (27129, 16),  # (Expected number of rows and columns)
    }
    
    all_ok = True
    
    print("Data verification in progress...")
    print("-" * 50)
    
    for filepath, (expected_rows, expected_cols) in required_files.items():
        if not os.path.exists(filepath):
            print(f"✗ {filepath} not found")
            all_ok = False
            continue
        
        try:
            df = pd.read_csv(filepath)
            rows, cols = df.shape
            
            if rows >= expected_rows * 0.9:  # Allow for a 10% error
                print(f"✓ {filepath}: {rows} rows, {cols} columns")
            else:
                print(f"⚠ {filepath}: {rows} rows (Expected number of rows are approximately {expected_rows})")
                all_ok = False
                
        except Exception as e:
            print(f"✗ {filepath}: Loading error - {e}")
            all_ok = False
    
    print("-" * 50)
    
    if all_ok:
        print("✓ All data files are OK!")
        return 0
    else:
        print("✗ The preparation of the data has not been completed")
        print("\nCheck out the "Preparing Your Data" section in README.md")
        return 1

if __name__ == "__main__":
    sys.exit(check_data())
