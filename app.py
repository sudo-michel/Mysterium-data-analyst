import os
from flask import Flask, request, redirect, url_for, render_template
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def ensure_upload_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

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
    # Load the uploaded CSV file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_file.csv')
    data = pd.read_csv(file_path)

    # Convert the 'settledAt' column to datetime
    data['settledAt'] = pd.to_datetime(data['settledAt'])

    # Calculate cumulative amount
    data['cumulative_amount'] = data['amount'].cumsum()

    # Generate cumulative amount graph
    plt.figure(figsize=(10, 6))
    plt.plot(data['settledAt'], data['cumulative_amount'], marker='o', linestyle='-', label='Cumulative Amount')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Amount')
    plt.title('Cumulative Amount Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    cumulative_graph_path = os.path.join(app.config['UPLOAD_FOLDER'], 'cumulative_amount_over_time.png')
    plt.savefig(cumulative_graph_path)
    print(f"Cumulative graph saved at {cumulative_graph_path}")
    plt.close()

    # Calculate daily revenue
    daily_revenue = data.groupby(data['settledAt'].dt.date)['amount'].sum().reset_index()
    daily_revenue.columns = ['Date', 'Daily Revenue']

    # Generate daily revenue graph
    plt.figure(figsize=(10, 6))
    plt.plot(daily_revenue['Date'], daily_revenue['Daily Revenue'], marker='o', linestyle='-', label='Daily Revenue')
    plt.xlabel('Date')
    plt.ylabel('Daily Revenue')
    plt.title('Daily Revenue Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    daily_revenue_graph_path = os.path.join(app.config['UPLOAD_FOLDER'], 'daily_revenue_over_time.png')
    plt.savefig(daily_revenue_graph_path)
    print(f"Daily revenue graph saved at {daily_revenue_graph_path}")
    plt.close()

    # Calculate statistics
    average_revenue = daily_revenue['Daily Revenue'].mean()
    median_revenue = daily_revenue['Daily Revenue'].median()
    transaction_count = len(data)

    return render_template('analysis.html',
                           cumulative_graph=url_for('static', filename='uploads/cumulative_amount_over_time.png'),
                           daily_revenue_graph=url_for('static', filename='uploads/daily_revenue_over_time.png'),
                           average_revenue=average_revenue,
                           median_revenue=median_revenue,
                           transaction_count=transaction_count)

if __name__ == '__main__':
    app.run(debug=True)
