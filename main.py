from bs4 import BeautifulSoup
import pandas as pd

# Assuming you have an HTML file named 'farms.html' in your project directory
html_file_path = 'src.html'  # Adjust this path as needed

# Reading the HTML content from the file
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

data = []

# Iterate through each farm entry
for farm in soup.find_all("span", class_="farm"):
    # Extract the farm name
    farm_name = farm.find("a").text.strip() if farm.find("a") else ""

    # Initialize placeholders for phone and email
    phone = ""
    email = ""

    # Extract details text, assuming it follows the farm name
    details_text = farm.parent.get_text()

    # Extract the phone number
    if "Phone:" in details_text:
        phone_start = details_text.find("Phone:") + len("Phone:")
        phone_end = details_text.find(".", phone_start)
        phone = details_text[phone_start:phone_end].strip()

    # Extract the email
    email_tag = farm.parent.find("a", href=True)
    if email_tag and "mailto:" in email_tag['href']:
        email = email_tag['href'].split("mailto:")[1]

    # Extract the fruits listed
    fruits = details_text.split("-")[1].split(".")[0].strip() if "-" in details_text else ""

    # Extract the address, assuming it's before the "Phone:" text
    address = details_text.split("Phone:")[0].strip() if "Phone:" in details_text else details_text.strip()

    # Extract county name
    county_name = farm.find_previous("h3").text.strip() if farm.find_previous("h3") else ""

    data.append([county_name, farm_name, fruits, address, phone, email])

# Convert the data into a DataFrame
df = pd.DataFrame(data, columns=["County", "Farm Name", "Fruits", "Address", "Phone", "Email"])

# Specify the filename for the CSV
csv_filename = "farms_extracted.csv"

# Save the DataFrame to a CSV file
df.to_csv(csv_filename, index=False)

print("Data extraction completed and saved to CSV.")
