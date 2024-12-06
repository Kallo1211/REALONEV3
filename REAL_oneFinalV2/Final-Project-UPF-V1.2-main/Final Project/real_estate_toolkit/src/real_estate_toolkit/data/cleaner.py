from dataclasses import dataclass
from typing import Dict, List, Any
import re

@dataclass
class Cleaner:
    """Class for cleaning real estate data."""
    data: List[Dict[str, Any]]

    def rename_with_best_practices(self) -> None:
        """
        Rename the columns with best practices (e.g., snake_case, descriptive names).

        Modifies the data in place by transforming all keys in each row to snake_case.
        """
        if not self.data:
            return  # Exit early if data is empty

        # Extract all column names from the first row
        original_columns = list(self.data[0].keys())

        for row in self.data:
            new_row = {}
            for column in original_columns:
                # Convert column name to snake_case
                new_column = re.sub(r'([A-Z])', r'_\1', column)  # Add underscores before capital letters
                new_column = re.sub(r'[^a-zA-Z0-9]', '_', new_column)  # Replace non-alphanumeric characters
                new_column = new_column.lower().strip('_')  # Convert to lowercase and strip leading/trailing underscores
                new_row[new_column] = row[column]

            # Update the row with the new column names
            row.clear()
            row.update(new_row)

    def na_to_none(self) -> None:
        """
        Replace 'NA' with None in all values in the dataset.

        Modifies the data in place and replaces 'NA' with None in all columns.
        """
        for row in self.data:
            if not row or not isinstance(row, dict):  # Skip rows that are None or not dictionaries
                continue
            for column in row.keys():  # Safely iterate over keys
                if row[column] == "NA":  # Replace "NA" with None
                    row[column] = None
                    
    def na_to_none(self) -> None:
        """
        Replace 'NA' with None in all values in the dataset.

        Modifies the data in place and replaces 'NA' with None in all columns.
        """
        for index, row in enumerate(self.data):
            if not row or not isinstance(row, dict):  # Skip rows that are None or not dictionaries
                print(f"Skipping invalid row at index {index}: {row}")  # Debugging
                continue

            for column in row.keys():
                try:
                    if row[column] == "NA":  # Replace "NA" with None
                        row[column] = None
                except Exception as e:
                    # Debugging output to pinpoint the issue
                    print(f"Error processing row {index}, column '{column}': {e}")
                    raise
