import requests
import pandas as pd
from io import StringIO

def decode_secret_message(doc_url):
    try:
        # Fetch the content of the Google Doc
        response = requests.get(doc_url)
        response.raise_for_status()
        text = response.text

        # Parse table data from the HTML using pandas
        tables = pd.read_html(StringIO(text), header=0)  # Use the first row as headers
        if not tables:
            print("No tables found in the document.")
            return

        # Use the first table in the document
        df = tables[0]

        # Debug: Print the first few rows of the table
        print("First few rows of the table after parsing:")
        print(df.head())

        # Ensure required columns are present
        required_columns = {"x-coordinate", "Character", "y-coordinate"}
        if not required_columns.issubset(df.columns):
            print(f"Required columns are missing. Found columns: {df.columns}")
            return

        # Parse table into a list of characters and their coordinates
        data = [(row["Character"], int(row["x-coordinate"]), int(row["y-coordinate"])) for _, row in df.iterrows()]

        # Find the size of the grid
        max_x = max(item[1] for item in data)
        max_y = max(item[2] for item in data)

        # Initialize the grid with spaces
        grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

        # Fill the grid with characters
        for char, x, y in data:
            grid[y][x] = char

        # Print the grid
        print("\nDecoded Secret Message:")
        for row in grid:
            print("".join(row))

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
doc_url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
decode_secret_message(doc_url)