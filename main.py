"""Creating a playlist."""

import requests
from bs4 import BeautifulSoup

print('Which music year do you want to create a playlist from?')

# Get the date
date = input('Type in this format YYYY-MM-DD: ')
print(date)
