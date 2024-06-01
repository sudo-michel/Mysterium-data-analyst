import pandas as pd
import os

# Charger les données à partir du fichier CSV initial
file_path_initial = 'settlement_history_1717251645585.csv'
data_initial = pd.read_csv(file_path_initial, delimiter=',', quotechar='"')

# Vérifier si le DataFrame a été chargé correctement
print(data_initial.head())

# Définir les noms des colonnes si elles ne sont pas correctement lues
if len(data_initial.columns) == 1:
    # Supposons que les colonnes ne sont pas correctement lues, nous réessayons avec une autre méthode
    data_initial = pd.read_csv(file_path_initial, delimiter=',', quotechar='"', names=[
        "txHash", "providerId", "hermesId", "channelAddress",
        "externalWalletAddress", "amount", "settledAt", "fees",
        "isWithdrawal", "blockExplorerUrl", "error"
    ], header=0)

# Convertir la colonne 'settledAt' en datetime et extraire uniquement la date
data_initial['settledAt'] = pd.to_datetime(data_initial['settledAt']).dt.date

# Convertir 'amount' et 'fees' en numérique et conserver uniquement les 4 premières unités
data_initial['amount'] = pd.to_numeric(data_initial['amount'], errors='coerce').astype(str).str[:4].astype(float)
data_initial['fees'] = pd.to_numeric(data_initial['fees'], errors='coerce').astype(str).str[:4].astype(float)

# Vérifier les valeurs négatives ou incorrectes
data_initial['amount'] = data_initial['amount'].abs()
data_initial['fees'] = data_initial['fees'].abs()

# Sélectionner les colonnes pertinentes
data_transformed = data_initial[['settledAt', 'amount', 'fees']]

# Trier par date pour un calcul cumulé correct
data_transformed = data_transformed.sort_values(by='settledAt')

# Afficher les premières lignes des données transformées
print(data_transformed.head())

# Définir le chemin absolu pour le fichier de sortie
output_file_path = os.path.abspath('settlement_transformed.csv')

# Sauvegarder les données transformées dans un nouveau fichier CSV
data_transformed.to_csv(output_file_path, index=False)

print(f"Les données nettoyées ont été sauvegardées dans {output_file_path}")
