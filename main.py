import pandas as pd

# Charger les données à partir du fichier CSV initial
file_path_initial = 'settlement_history_1717251645585.csv'
data_initial = pd.read_csv(file_path_initial, delimiter=',', quotechar='"')

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

# Sélectionner les colonnes pertinentes
data_transformed = data_initial[['settledAt', 'amount', 'fees']]

# Afficher les premières lignes des données transformées
print(data_transformed.head())


# Sauvegarder les données transformées dans un nouveau fichier CSV
output_file_path = 'settlement_transformed.csv'
data_transformed.to_csv(output_file_path, index=False)