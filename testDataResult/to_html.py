import pandas as pd

# Read the CSV file
data = pd.read_csv("test_predicted.csv")

# Convert the data to HTML table
html_table = data.to_html(index=False)

# Print or save the HTML table
print(html_table)

# If you want to save it to an HTML file
with open("pred_table.html", "w") as file:
    file.write(html_table)
