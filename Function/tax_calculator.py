import pandas as pd

def calculate_transaction_costs(trade_type, buy_price, sell_price, quantity, apply_dp):
    """Calculates transaction costs including DP charges only once per stock per day."""
    
    turnover = (buy_price + sell_price) * quantity
    brokerage = 0
    stt = 0
    exchange_transaction_charge = 0
    sebi_charges = 0
    ipft_charges = 0
    stamp_duty = 0
    gst = 0
    dp_charges = 14.75 if apply_dp else 0  # DP charges applied only once per stock per day

    if trade_type == "BUY":
        turnover = buy_price * quantity
        brokerage = 0  # No brokerage for buy
        stt = round(turnover * 0.001, 2)  # STT at 0.1%
        exchange_transaction_charge = round(turnover * 0.0000345, 2)  # 0.00345%
        sebi_charges = round(turnover * 0.000001, 2)  # SEBI charges
        ipft_charges = round(turnover * 0.000001, 2)  # IPFT
        stamp_duty = round(turnover * 0.00015, 2)  # Stamp Duty
        gst = round(0.18 * (exchange_transaction_charge + sebi_charges), 2)  # GST

        total_transaction_costs = brokerage + stt + exchange_transaction_charge + sebi_charges + ipft_charges + stamp_duty + gst

    elif trade_type == "SELL":
        turnover = sell_price * quantity  # Sell turnover only
        stt = round(turnover * 0.001, 2)  # STT at 0.1%
        exchange_transaction_charge = round(turnover * 0.0000345, 2)  # 0.00345%
        sebi_charges = round(turnover * 0.000001, 2)  # SEBI charges
        ipft_charges = round(turnover * 0.000001, 2)  # IPFT
        stamp_duty = 0  # No stamp duty on sell transactions
        gst = 0  # GST not applied on sell
       
        total_transaction_costs = stt + exchange_transaction_charge + sebi_charges + ipft_charges + dp_charges

    return round(total_transaction_costs, 4)

def add_fee_data(file_path):
    """Adds tax information to a trade data CSV file with DP charges applied only once per stock per day."""
    
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()  # Clean column names

    if 'Taxes' not in data.columns:
        data['Taxes'] = 0.0  

    # Track which stocks have already had DP charges applied for the day
    dp_applied = set()

    for index, row in data.iterrows():
        trade_type = str(row['Type']).strip().upper() if pd.notna(row['Type']) else ''
        buy_price = row['Value'] / row['Shares'] if row['Shares'] != 0 else 0
        sell_price = buy_price  # Assuming no separate sell price column, adjust if needed
        quantity = row['Shares']
        date = str(row['Date']).strip()  # Convert to string to avoid datetime issues
        stock = str(row['Name']).strip()

        # Apply DP charges only once per stock per day for Sell transactions
        apply_dp = (trade_type == "SELL" and (date, stock) not in dp_applied)
        if apply_dp:
            dp_applied.add((date, stock))  # Mark this stock for DP charge on this date

        tax = calculate_transaction_costs(trade_type, buy_price, sell_price, quantity, apply_dp)
        data.at[index, 'Taxes'] = tax  

    data.to_csv(file_path, index=False)
    print("Updated CSV with Taxes.")
