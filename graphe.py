import pandas as pd
import matplotlib.pyplot as plt
import os

# Charger les données nettoyées
file_path = 'settlement_transformed.csv'
data = pd.read_csv(file_path)

# Convertir la colonne 'settledAt' en datetime
data['settledAt'] = pd.to_datetime(data['settledAt'])

# Calculer la somme cumulative des montants
data['cumulative_amount'] = data['amount'].cumsum()

# Créer un graphique linéaire pour le montant cumulé
plt.figure(figsize=(10, 6))
plt.plot(data['settledAt'], data['cumulative_amount'], marker='o', linestyle='-', label='Cumulative Amount')
plt.xlabel('Date')
plt.ylabel('Cumulative Amount')
plt.title('Cumulative Amount Over Time')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Enregistrer le graphique du montant cumulé
output_graph_path = os.path.abspath('cumulative_amount_over_time.png')
plt.savefig(output_graph_path)
print(f"Le graphique a été sauvegardé dans {output_graph_path}")

# Calculer le revenu journalier
daily_revenue = data.groupby(data['settledAt'].dt.date)['amount'].sum().reset_index()
daily_revenue.columns = ['Date', 'Daily Revenue']

# Créer un graphique pour le revenu journalier
plt.figure(figsize=(10, 6))
plt.plot(daily_revenue['Date'], daily_revenue['Daily Revenue'], marker='o', linestyle='-', label='Daily Revenue')
plt.xlabel('Date')
plt.ylabel('Daily Revenue')
plt.title('Daily Revenue Over Time')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Enregistrer le graphique du revenu journalier
output_graph_daily_path = os.path.abspath('daily_revenue_over_time.png')
plt.savefig(output_graph_daily_path)
print(f"Le graphique a été sauvegardé dans {output_graph_daily_path}")

# Afficher les graphiques
plt.show()
