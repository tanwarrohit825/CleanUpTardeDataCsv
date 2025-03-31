from fuzzywuzzy import process, fuzz

# Dictionary for special cases
SPECIAL_CASES = {
    "ICICI Pru Bank Nifty ETF": "rohitBank",
    "ICICI Prudential IT ETF": "ICICITECH.NS",
    "ICICI Pru Nifty 50 ETF": "NIFTYIETF.NS",
    "Nippon India Nifty 50 ETF": "NIFTYBEES.NS",
    "Nippon India Gold ETF": "GOLDBEES.NS",
    "Nippon Gold ETF (GOLDBEES)": "GOLDBEES.NS",
    "Nippon Nifty 50 ETF (NIFTYBEES)": "NIFTYBEES.NS",
    "Nippon Nifty Next 50 ETF (JUNIORBEES)": "JUNIORBEES.NS",
    "Mirae Asset Nifty Midcap 150 ETF": "MAM150ETF.NS",
    "Kotak Nifty Alpha 50 ETF": "ALPHA.NS",
    "HDFC Nifty Small Cap 250 ETF": "HDFCSML250.NS",
    "Nippon Pharma ETF (PHARMABEES)": "PHARMABEES.NS",
    "Nippon Nifty Liquid ETF (LIQUIDBEES)": "LIQUIDBEES.NS",
    "Nippon Nifty Bank ETF (BANKBEES)": "BANKBEES.NS"
}

def match_name(name, name_dict, threshold=99.5):
    """ Matches a name using fuzzy logic or returns a predefined value. """
    if name in SPECIAL_CASES:
        return SPECIAL_CASES[name]
    
    match, score = process.extractOne(name, name_dict.keys(), scorer=fuzz.token_set_ratio)
    return name_dict[match] if score >= threshold else 'NA'
