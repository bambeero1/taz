import sqlite3
import pandas as pd
import os

if os.path.isfile('index.html'):
    os.remove('index.html')

# Connect to the SQLite database
conn = sqlite3.connect('dresses.db')

# Retrieve data from the "dresses" table
df = pd.read_sql_query('SELECT * FROM dresses', conn)

# Filter out rows with no sizes available
df = df[df['sizes'] != 'No sizes available']

# Sort the data by discount percentage
df = df.sort_values(by='percentage', ascending=False)

# Create a new column with clickable URLs
df['url_html'] = df['url'].apply(lambda x: '<a href="{0}">{0}</a>'.format(x))

# Save the data as an HTML table with clickable URLs and Bootstrap styling
with open('index.html', 'w') as f:
    f.write('<!DOCTYPE html>\n<html>\n<head>\n')
    f.write('<meta charset="UTF-8">\n')
    f.write('<title>Dresses</title>\n')
    f.write('<link rel="stylesheet" href="https://bootswatch.com/4/darkly/bootstrap.css">\n')
    f.write('<link rel="stylesheet" href="style.css">\n')
    f.write('</head>\n<body>\n')
    f.write('<div class="container">\n')
    f.write('<h1 class="text-center">Dresses</h1>\n')
    f.write(df.to_html(escape=False, index=False, classes='table table-hover table-dark'))
    f.write('\n</div>\n')
    f.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>\n')
    f.write('<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"></script>\n')
    f.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>\n')
    f.write('</body>\n</html>')
