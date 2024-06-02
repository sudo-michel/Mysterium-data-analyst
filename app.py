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
            return redirect(url_for('analyze_file'))
    return render_template('index.html')


@app.route('/analyze')
def analyze_file():
    ensure_upload_folder()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_file.csv')

    # Vérifier si le fichier existe
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas.")
        return "File not found", 404

    print(f"Chargement du fichier: {file_path}")
    try:
        data = pd.read_csv(file_path)
        print("Fichier chargé avec succès.")
    except Exception as e:
        print(f"Erreur lors du chargement du fichier: {e}")
        return "Error loading file", 500

    try:
        data['settledAt'] = pd.to_datetime(data['settledAt'])
        print("Conversion de la colonne 'settledAt' en datetime réussie.")
    except Exception as e:
        print(f"Erreur lors de la conversion de 'settledAt' en datetime: {e}")
        return "Error processing dates", 500

    # Afficher les premières lignes des données pour débogage
    print("Premières lignes des données:")
    print(data.head())

    # Sauvegarder les données transformées dans un nouveau fichier CSV
    transformed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'settlement_transformed.csv')
    try:
        data[['settledAt', 'amount']].to_csv(transformed_file_path, index=False)
        print(f"Données transformées sauvegardées à {transformed_file_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données transformées: {e}")
        return "Error saving transformed data", 500

    # Appeler la fonction generate_graphs pour créer les graphiques
    try:
        generate_graphs(transformed_file_path)
    except Exception as e:
        print(f"Erreur lors de la génération des graphiques: {e}")
        return "Error generating graphs", 500

    return render_template('analysis.html',
                           cumulative_graph=url_for('static', filename='uploads/cumulative_amount_over_time.png'),
                           daily_revenue_graph=url_for('static', filename='uploads/daily_revenue_over_time.png'),
                           average_revenue=data['amount'].mean(),
                           median_revenue=data['amount'].median(),
                           transaction_count=len(data))


if __name__ == '__main__':
    app.run(debug=True)
