import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_graphs(file_path):
    # Charger les données nettoyées
    data = pd.read_csv(file_path)

    # Convertir la colonne 'settledAt' en datetime
    data['settledAt'] = pd.to_datetime(data['settledAt'])

    # Calculer la somme cumulative des montants
    data = data.sort_values('settledAt')  # Assurez-vous que les données sont triées par date
    data['cumulative_amount'] = data['amount'].cumsum()

    # Créer un graphique en barres pour le montant cumulé
    plt.figure(figsize=(10, 6))
    plt.bar(data['settledAt'], data['cumulative_amount'], label='Cumulative Amount')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Amount')
    plt.title('Cumulative Amount Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Enregistrer le graphique du montant cumulé
    output_graph_path = os.path.abspath('static/uploads/cumulative_amount_over_time.png')
    plt.savefig(output_graph_path)
    print(f"Le graphique a été sauvegardé dans {output_graph_path}")
    plt.close()

    # Calculer le revenu journalier et les frais journaliers
    daily_revenue = data.groupby(data['settledAt']).agg({'amount': 'sum', 'fees': 'sum'}).reset_index()
    daily_revenue.columns = ['Date', 'Daily Revenue', 'Daily Fees']

    # Créer un graphique pour le revenu journalier et les frais journaliers
    plt.figure(figsize=(10, 6))
    plt.plot(daily_revenue['Date'], daily_revenue['Daily Revenue'], marker='o', linestyle='-', label='Daily Revenue')
    plt.plot(daily_revenue['Date'], daily_revenue['Daily Fees'], marker='o', linestyle='-', label='Daily Fees', color='orange')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Daily Revenue and Fees Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Enregistrer le graphique du revenu journalier
    output_graph_daily_path = os.path.abspath('static/uploads/daily_revenue_over_time.png')
    plt.savefig(output_graph_daily_path)
    print(f"Le graphique a été sauvegardé dans {output_graph_daily_path}")
    plt.close()

# Exemple d'appel de la fonction
if __name__ == '__main__':
    generate_graphs('settlement_transformed.csv')
