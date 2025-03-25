import pandas as pd
import numpy as np
from Function.file_utils import findpath
from  Function.matching import match_name
from  Function.tax_calculator import add_fee_data

# Select Trade Data
file_path = findpath("Select TradeData file or Dhan file")
if not file_path:
    exit()

data = pd.read_csv(file_path)
data.to_csv('cleanUpTradeData.csv', columns=['Date', 'Time', 'Name', 'Buy/Sell', 'Quantity/Lot', 'Trade Value'], index=False)

# Select Key Value File
file_path = findpath("Select MyKeyValue file")
if not file_path:
    exit()

key_value = pd.read_csv(file_path)

# Select Cleaned Trade Data File
file_path = findpath("Select cleanUpTradeData file")
if not file_path:
    exit()

data = pd.read_csv(file_path)

data['Name'] = data['Name'].astype(str).str.strip()
key_value['Name'] = key_value['Name'].astype(str).str.strip()


# Create a lookup dictionary
name_dict = dict(zip(key_value['Name'], key_value['Symbol']))

# Apply name matching
data['Symbol'] = data['Name'].apply(lambda x: match_name(x, name_dict))
data['Symbol'].replace('NA', 'Rohit', inplace=True)

# Save merged data
data.to_csv('merge.csv', index=False)

# Rename columns in merged file
file_path = findpath("Select merge file")
if not file_path:
    exit()

merge_file = pd.read_csv(file_path)
merge_file = merge_file.rename(columns={
    "Buy/Sell": "Type",
    "Quantity/Lot": "Shares",
    "Trade Value": "Value",
    "Symbol": "Ticker Symbol"
})

merge_file.drop(merge_file.columns[merge_file.columns.str.contains('Unnamed', case=False)], axis=1, inplace=True)
merge_file.to_csv('merge.csv')

# Add tax data
add_fee_data(file_path)
print("Processing complete.")
