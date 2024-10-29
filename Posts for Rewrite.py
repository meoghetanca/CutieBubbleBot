import pandas as pd
import random

# Load the CSV file
def load_links(csv_file):
    try:
        # Read the CSV file, skipping any bad lines
        df = pd.read_csv(csv_file, on_bad_lines='skip')
        
        # Check if 'links' column exists
        if 'links' not in df.columns:
            print("The CSV file does not contain a 'links' column.")
            return []

        # Return the list of links
        return df['links'].dropna().tolist()  # Drop any NaN values, if present
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return []

# Select and shuffle links
def select_and_shuffle_links(links, num_links=52):
    if len(links) < num_links:
        print(f"Not enough links available. Found {len(links)} links.")
        return []

    # Randomly select and shuffle 52 links
    selected_links = random.sample(links, num_links)
    random.shuffle(selected_links)
    return selected_links

# Main function
def main():
    csv_file = 'D:\PYTHON\Files\link.csv'  # Replace with your CSV file path
    links = load_links(csv_file)
    
    if not links:
        return  # Exit if no links were loaded
    
    shuffled_links = select_and_shuffle_links(links)
    
    if shuffled_links:
        print("Randomly selected and shuffled links:")
        for link in shuffled_links:
            print(link)

if __name__ == "__main__":
    main()