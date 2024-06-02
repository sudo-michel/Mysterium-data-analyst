# Mysterium Data Analyst

A project to clean and transform settlement data from a CSV file for analysis and visualization.

## Features

- **Data Cleaning**: Extracts and cleans transaction data, retaining only the necessary columns.
- **Date Formatting**: Converts transaction timestamps to date format, removing unnecessary time information.
- **Amount and Fees Processing**: Limits transaction amounts and fees to the first four digits for simplicity.
- **CSV Export**: Saves the cleaned data into a new CSV file for further analysis.
- **Graphical Analysis**: Generates graphical representations of the data, including:
  - Time series plots showing transaction amounts over time.
  - Cumulative transaction amounts.
  - Daily revenue and fees.

## Installation

### Local Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/sudo-michel/Mysterium-data-analyst.git
    cd Mysterium-data-analyst
    ```

2. **Create a virtual environment and activate it**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the Flask application**:
    ```sh
    python app.py
    ```

5. **Open your web browser and navigate to `http://127.0.0.1:5000`**.

### Deployment on PythonAnywhere

1. **Create an account**: If you don't have an account, sign up on [PythonAnywhere](https://www.pythonanywhere.com/).

2. **Create a new web app**:
    - Go to the "Web" tab.
    - Click "Add a new web app".
    - Choose "Manual configuration" and select "Python 3.x".

3. **Upload your project files**:
    - Go to the "Files" tab.
    - Upload your project files to your PythonAnywhere account.

4. **Set up a virtual environment**:
    - In the "Consoles" tab, start a Bash console.
    - Navigate to your project directory:
        ```sh
        cd ~/Mysterium-data-analyst
        ```
    - Create and activate a virtual environment:
        ```sh
        python -m venv venv
        source venv/bin/activate
        ```
    - Install the dependencies:
        ```sh
        pip install -r requirements.txt
        ```

5. **Configure the web app**:
    - Go to the "Web" tab and select your web app.
    - Set the "Working directory" to your project directory.
    - Under "Virtualenv", set the path to your virtual environment, e.g., `/home/yourusername/Mysterium-data-analyst/venv`.
    - Edit the WSGI configuration file to point to your Flask app:
        ```python
        import sys
        import os

        # Add your project directory to the sys.path
        project_home = u'/home/yourusername/Mysterium-data-analyst'
        if project_home not in sys.path:
            sys.path = [project_home] + sys.path

        # Set the 'PYTHONPATH' environment variable
        os.environ['PYTHONPATH'] = project_home

        # Activate your virtual env
        activate_this = os.path.expanduser(project_home + "/venv/bin/activate_this.py")
        exec(compile(open(activate_this).read(), activate_this, 'exec'), dict(__file__=activate_this))

        # Import Flask app
        from app import app as application
        ```

6. **Reload the web app**:
    - Go to the "Web" tab and click "Reload".

## Usage

1. **Upload your raw CSV file** on the homepage of your deployed app.
2. **Analyze** the uploaded file to generate graphs and statistics.

## Contribution

Feel free to fork the repository, make improvements, and submit pull requests. Your contributions are welcome!

## License

This project is licensed under the MIT License.
