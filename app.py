import os
from flask import Flask, request, redirect, url_for, render_template
import pandas as pd
from graphe import generate_graphs  # Importer la fonction generate_graphs

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads'))
app.config['ALLOWED_EXTENSIONS'] = {'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def ensure_upload_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        print(f"Dossier créé: {app.config['UPLOAD_FOLDER']}")
    else:
        print(f"Dossier existant: {app.config['UPLOAD_FOLDER']}")


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            ensure_upload_folder()
            filename = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_file.csv')
            file.save(filename)
            return redirect(url_for('analysis'))
    return render_template('index.html')


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        return redirect(url_for('analyze_file'))
    return render_template('analysis.html')


@app.route('/analyze', methods=['POST'])
def analyze_file():
    ensure_upload_folder()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_file.csv')

    # Vérifier si le fichier existe
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas.")
        return "File not found", 404

    print(f"Chargement du fichier: {file_path}")
    try:
        # Lire le fichier avec le délimiteur correct
        data_initial = pd.read_csv(file_path, delimiter=',', quotechar='"')
        print("Fichier chargé avec succès.")
        print("Colonnes disponibles:", data_initial.columns.tolist())
    except Exception as e:
        print(f"Erreur lors du chargement du fichier: {e}")
        return "Error loading file", 500

    try:
        # Définir les noms des colonnes si elles ne sont pas correctement lues
        if len(data_initial.columns) == 1:
            data_initial = pd.read_csv(file_path, delimiter=',', quotechar='"', names=[
                "txHash", "providerId", "hermesId", "channelAddress",
                "externalWalletAddress", "amount", "settledAt", "fees",
                "isWithdrawal", "blockExplorerUrl", "error"
            ], header=0)

        # Convertir la colonne 'settledAt' en datetime et extraire uniquement la date
        data_initial['settledAt'] = pd.to_datetime(data_initial['settledAt']).dt.date

        # Convertir 'amount' et 'fees' en numérique et conserver uniquement les 4 premières unités
        data_initial['amount'] = pd.to_numeric(data_initial['amount'], errors='coerce').astype(str).str[:4].astype(
            float)
        data_initial['fees'] = pd.to_numeric(data_initial['fees'], errors='coerce').astype(str).str[:4].astype(float)

        # Sélectionner les colonnes pertinentes
        data_transformed = data_initial[['settledAt', 'amount', 'fees']]

        print("Nettoyage des données réussi.")
    except Exception as e:
        print(f"Erreur lors du nettoyage des données: {e}")
        return "Error processing data", 500

    # Sauvegarder les données nettoyées dans un nouveau fichier CSV
    transformed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'settlement_transformed.csv')
    try:
        data_transformed.to_csv(transformed_file_path, index=False)
        print(f"Données nettoyées sauvegardées à {transformed_file_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données nettoyées: {e}")
        return "Error saving cleaned data", 500

    # Appeler la fonction generate_graphs pour créer les graphiques
    try:
        generate_graphs(transformed_file_path)
    except Exception as e:
        print(f"Erreur lors de la génération des graphiques: {e}")
        return "Error generating graphs", 500

    return render_template('analysis.html',
                           cumulative_graph=url_for('static', filename='uploads/cumulative_amount_over_time.png'),
                           daily_revenue_graph=url_for('static', filename='uploads/daily_revenue_over_time.png'),
                           average_revenue=data_transformed[
                               'amount'].mean() if 'amount' in data_transformed.columns else None,
                           median_revenue=data_transformed[
                               'amount'].median() if 'amount' in data_transformed.columns else None,
                           transaction_count=len(data_transformed))


if __name__ == '__main__':
    app.run(debug=True)
