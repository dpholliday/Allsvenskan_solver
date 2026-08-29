import pandas as pd

# 1. Load your CSV file
# Replace 'your_file.csv' with the actual path to your file
file_path = './data/VampsClean.csv'
df = pd.read_csv(file_path)

# Step 1 & 3: Rename 'id' to 'ID' and 'price' to 'BV'
df = df.rename(columns={'id': 'ID', 'price': 'BV', 'name': 'Name'})

# Step 2: Extract the leftmost substring from 'position' before the underscore '_'
# Adjust the split delimiter if your text uses spaces or hyphens instead
if 'position' in df.columns:
    pos_idx = df.columns.get_loc('position')
    df.insert(pos_idx + 1, 'POS', df['position'].astype(str).str.split('_').str[0])

# Step 4: Duplicate 'BV' into a new column 'SV' right next to it
if 'BV' in df.columns:
    bv_idx = df.columns.get_loc('BV')
    df.insert(bv_idx + 1, 'SV', df['BV'])

# Step 5: Insert an '_xMins' column directly in front of every '_xPts' column
# We find the target columns first to avoid modifying the dataframe size during the loop
xpts_columns = [col for col in df.columns if 'Pts' in col]

for col in xpts_columns:
    idx = df.columns.get_loc(col)
    mins_col_name = col.replace('Pts', 'xMins')
    
    # Inserts the new column directly in front of the xPts column. 
    # Defaulting value to 0 so it does not break your solver matrix.
    df.insert(idx, mins_col_name, 80)

# Save the modifications back to a CSV file
# index=False prevents pandas from adding an unwanted row-number column
output_file_path = './data/Vamps.csv'
df.to_csv(output_file_path, index=False)

print(f"Success! Saved formatted file as: {output_file_path}")