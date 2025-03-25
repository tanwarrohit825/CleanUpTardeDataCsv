#pip install -U -r requirements.txt

# import os
# os._exit(00)  # Force restart the kernel

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


def match_name(name, name_dict, threshold=99.5):
    # Check for the special case
    if name == "ICICI Pru Bank Nifty ETF":
        return "rohitBank"
    elif name == "ICICI Prudential IT ETF":
        return "ICICITECH.NS"
    elif name == "ICICI Pru Nifty 50 ETF":
        return "ICICINIFTY.NS"
    elif name == "Nippon India Nifty 50 ETF":
        return "NIFTYBEES.NS"
    elif name == "Nippon India Gold ETF":
        return "GOLDBEES.NS"
    elif name == "Nippon Gold ETF (GOLDBEES)":
        return "GOLDBEES.NS"
    elif name == "Nippon Nifty 50 ETF (NIFTYBEES)":
        return "NIFTYBEES.NS"
    elif name == "Nippon Nifty Next 50 ETF (JUNIORBEES)":
        return "JUNIORBEES.NS"
    elif name == "Mirae Asset Nifty Midcap 150 ETF":
        return "MAM150ETF.NS"
    elif name == "Kotak Nifty Alpha 50 ETF":
        return "ALPHA.NS"
    elif name == "HDFC Nifty Small Cap 250 ETF":
        return "HDFCSML250.NS"
    elif name == "Nippon Pharma ETF (PHARMABEES)":
        return "PHARMABEES.NS"
    elif name == "Nippon Nifty Liquid ETF (LIQUIDBEES)":
        return "LIQUIDBEES.NS"
    
    # Perform the usual matching process
    match, score = process.extractOne(name, name_dict.keys(), scorer=fuzz.token_set_ratio)
    if score >= threshold:
        return name_dict[match]
    else:
        return 'NA'
# add Fee in Software
def AddFeeDataInSoftware(file_path):
    
    dataFormBrocker = pd.read_csv(file_path)

    # Clean column names by stripping any extra spaces
    dataFormBrocker.columns = dataFormBrocker.columns.str.strip()

     # Ensure the 'Taxes' column exists; if not, create it
    if 'Taxes' not in dataFormBrocker.columns:
        dataFormBrocker['Taxes'] = 0.0  # Initialize with 0.0 or NaN
   
    # loop through the rows using iterrows()
    for index, row in dataFormBrocker.iterrows():
        Type = row['Type'].strip() #Type BUY
        Value = row['Value'] #190.38
        # Value = float(row['Value'].replace(',', '')) #'1,692.45'
        Shares = row['Shares'] #'1'
        STT = 0.001
        DP = 15

        if(Type == 'BUY'):
            Averageprice = Value / Shares
            BuyTaxes = round(Shares*Averageprice*STT,3)
            dataFormBrocker.at[index, 'Taxes'] = BuyTaxes  # Update the Taxes for the current row

        # if(Type == 'SELL'):
        #     Averageprice = Value / Shares
        #     SellTaxes = round(Shares*Averageprice*STT,3)+ DP
        #     dataFormBrocker.at[index, 'Taxes'] = SellTaxes  # Update the Taxes for the current row

 # Save the updated DataFrame back to the CSV file
    dataFormBrocker.to_csv(file_path, index=False)
    print("Updated CSV with Taxes.")
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

AddFeeDataInSoftware(file_path)

#print(mergefile)