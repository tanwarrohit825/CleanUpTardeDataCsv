import pandas as pd

def calculate_transaction_costs(trade_type, buy_price, sell_price, quantity, apply_dp):
    """Calculates transaction costs including DP charges only once per stock per day."""
    
    turnover = (buy_price + sell_price) * quantity
    brokerage = 0
    stt = 0
    exchange_transaction_charge = 0
    sebi_charges = 0
    stamp_duty = 0
    gst = 0
    dp_charges = 15.93 if apply_dp else 0  # DP charges applied only once per stock per day

    if trade_type == "DIRECT_EQUITY_INTRADAY":
        brokerage = min((buy_price * quantity * 0.0003) + (sell_price * quantity * 0.0003), 40)
        stt = round((sell_price * quantity) * 0.00025)
        exchange_transaction_charge = turnover * 0.0000345
        sebi_charges = turnover * 0.000001
        stamp_duty = round((buy_price * quantity) * 0.00003)
        gst = 0.18 * (brokerage + exchange_transaction_charge + sebi_charges)

    elif trade_type == "DIRECT_EQUITY_DELIVERY":
        stt = round(turnover * 0.001)
        exchange_transaction_charge = turnover * 0.0000345
        sebi_charges = turnover * 0.000001
        stamp_duty = round((buy_price * quantity) * 0.00015)
        gst = 0.18 * (exchange_transaction_charge + sebi_charges)

    total_transaction_costs = brokerage + stt + exchange_transaction_charge + sebi_charges + stamp_duty + gst + dp_charges
    return round(total_transaction_costs, 3)

def add_fee_data(file_path):
    """Adds tax information to a trade data CSV file with DP charges applied only once per stock per day."""
    
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()  # Clean column names

    if 'Taxes' not in data.columns:
        data['Taxes'] = 0.0  

    # Track which stocks have already had DP charges applied for the day
    dp_applied = set()

    for index, row in data.iterrows():
        trade_type = str(row['Type']).strip() if pd.notna(row['Type']) else ''
        buy_price = row['Value'] / row['Shares'] if row['Shares'] != 0 else 0
        sell_price = buy_price  # Assuming no separate sell price column, adjust if needed
        quantity = row['Shares']
        date = row['Date']
        stock = row['Name']

        # Apply DP charges only once per stock per day
        apply_dp = (trade_type == "Sell" and (date, stock) not in dp_applied)
        if apply_dp:
            dp_applied.add((date, stock))  # Mark this stock for DP charge on this date

        tax = calculate_transaction_costs(trade_type, buy_price, sell_price, quantity, apply_dp)
        data.at[index, 'Taxes'] = tax  

    data.to_csv(file_path, index=False)
    print("Updated CSV with Taxes.")

