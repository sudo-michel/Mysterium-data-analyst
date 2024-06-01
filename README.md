# Settlement Data Transformer

This project is designed to clean and transform settlement data from a CSV file. It focuses on extracting and converting relevant transaction data to a more manageable format, while allowing for future graphical analysis and visualization.

## Features

- **Data Cleaning**: Extracts and cleans transaction data, retaining only the necessary columns.
- **Date Formatting**: Converts transaction timestamps to date format, removing unnecessary time information.
- **Amount and Fees Processing**: Limits transaction amounts and fees to the first four digits for simplicity.
- **CSV Export**: Saves the cleaned data into a new CSV file for further analysis.

## Future Enhancements

- **Graphical Analysis**: The project will be extended to include graphical representations of the data. This may include:
  - Time series plots showing transaction amounts over time.
  - Cumulative transaction amounts.
  - Histograms and other statistical visualizations.

## Usage

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/settlement-data-transformer.git
    cd settlement-data-transformer
    ```

2. **Install dependencies**:
    Ensure you have `pandas` and other necessary libraries installed.
    ```sh
    pip install pandas matplotlib
    ```

3. **Run the script**:
    Update the file paths in the script to point to your data files and run it using Python.
    ```sh
    python main.py
    ```

## Contribution

Feel free to fork the repository, make improvements, and submit pull requests. Your contributions are welcome!

## License

This project is licensed under the MIT License.
