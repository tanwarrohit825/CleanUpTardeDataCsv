import pandas as pd
import numpy as np

import easygui

from fuzzywuzzy import process, fuzz

#find the file path 
def findpath(title):
    global file_path
    file_path = easygui.fileopenbox(title)

    # Check if a file was selected
    if file_path:
        # Replace backslashes with forward slashes
        converted_path = file_path.replace('\\', '/')
    else:
        print("No file selected.")


#find the name and this similar
def match_name(name, name_dict, threshold=93):
    match, score = process.extractOne(name, name_dict.keys(), scorer=fuzz.token_set_ratio)
    if score >= threshold:
        return name_dict[match]
    else:
        return 'NA'
#find the TradeData file getting form brocker
findpath("Select TradeData file or dhan file")
dataForBrocker = pd.read_csv(file_path)
dataForBrocker.to_csv('cleanUpTradeData.csv', columns=['Date','Time','Name','Buy/Sell' , 'Quantity/Lot' , 'Trade Value'],index=False)



#find the Keyfile create my me 
findpath("Select MyKeyValue file ")
keyValue = pd.read_csv(file_path)

#select new cleanUpTradeData 
findpath("Select cleanUpTradeData file")

dataForBrocker = pd.read_csv(file_path)
#New Keyvalue
# findpath("Select cleanUpKeyvalue file")

# keyValue = pd.read_csv(file_path)

dataForBrocker['Name'] = dataForBrocker['Name'].str.strip()
keyValue['Name'] = keyValue['Name'].str.strip()

#  Create a dictionary for quick lookup using fuzzy matching
name_dict = dict(zip(keyValue['Name'], keyValue['Symbol']))

# Apply the matching function to the 'Name' column in dataForBrocker
dataForBrocker['Symbol'] = dataForBrocker['Name'].apply(lambda x: match_name(x, name_dict))


dataForBrocker['Symbol'].replace('NA', 'Rohit', inplace=True)

#replace the NAn with rohit
#dataForBrocker = dataForBrocker.replace(np.nan, 'Rohit', regex=True)

# Write the merged DataFrame to a CSV file
dataForBrocker.to_csv('merge.csv', index=False)

#find the merge file for remane its colloume 
findpath("Select merge file")

mergefile= pd.read_csv(file_path)

mergefile = mergefile.rename({"Buy/Sell":"Type","Quantity/Lot":"Shares","Trade Value":"Value","Symbol":"Ticker Symbol"}, axis='columns')

mergefile.drop(mergefile.columns[mergefile.columns.str.contains('Unnamed', case=False)], axis=1, inplace=True)

mergefile.to_csv('merge.csv')

#print(mergefile)