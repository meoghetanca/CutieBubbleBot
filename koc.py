import pandas as pd
import re

# Function to clean phone numbers
def clean_phone_number(phone):
    if isinstance(phone, str):  # Check if the phone number is a string
        # Remove unwanted characters
        cleaned_phone = re.sub(r'[^\d]', '', phone)  # Keep only digits

        # Optional: Format the phone number (e.g., add a country code if necessary)
        if len(cleaned_phone) == 10:  # Example for a 10-digit number
            cleaned_phone = f'+84 {cleaned_phone}'  # Add country code

        return cleaned_phone
    else:
        return None  # Return None for non-string entries (e.g., NaN)

# Load the CSV file into a DataFrame
df = pd.read_csv('D:\Python\Files\KOC.csv', sep=';', encoding='utf-8')

# Display the original DataFrame (for verification)
print("Original DataFrame:")
print(df)

# Clean the 'Email/Contact inf' column
df['Cleaned Contact'] = df['Email/Contact inf'].apply(clean_phone_number)

# Display the cleaned DataFrame
print("\nCleaned DataFrame:")
print(df[['Email/Contact inf', 'Cleaned Contact']])

# Save the cleaned DataFrame to a new CSV file
df.to_csv('cleaned_contacts.csv', sep=';', index=False, encoding='utf-8')
