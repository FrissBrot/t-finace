import functions as fn
import pandas as pd
from datetime import datetime, timedelta

transaction_raw = fn.get_transactions(3)
current_amount = 1000

columns = ["date", "type", "category", "amount", "description"]
df_raw = pd.DataFrame(transaction_raw, columns=columns)

transactions = []

for transaction in transaction_raw:
    new_entry = {'date': transaction[0], 'amount': transaction[3]}
    transactions.append(new_entry)

# Umwandlung der Daten in das richtige Format
for transaction in transactions:
    transaction['amount'] = float(transaction['amount'])

# Erstelle ein DataFrame für die letzten 30 Tage
end_date = datetime.today().date()
start_date = end_date - timedelta(days=29)

# Liste der Daten für die letzten 30 Tage
date_range = [start_date + timedelta(days=x) for x in range(30)]

# DataFrame initialisieren
df = pd.DataFrame(columns=['date', 'balance'])
balance = current_amount

# Iteriere durch jeden Tag in den letzten 30 Tagen
for day in date_range:
    # Aktualisiere den Kontostand basierend auf den Transaktionen bis zu diesem Tag
    for transaction in transactions:
        if transaction['date'] <= day:
            balance += transaction['amount']
    
    # Speichere den Kontostand für diesen Tag im DataFrame
    new_row = pd.DataFrame({'date': [day], 'balance': [balance]})
    df = pd.concat([df, new_row], ignore_index=True)

# Sortiere das DataFrame nach Datum (optional)
df = df.sort_values(by='date').reset_index(drop=True)

# Ausgabe des Ergebnis-DataFrames
print(df)
