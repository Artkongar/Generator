from sympy import *
import re
import os
import string
import requests
from bs4 import BeautifulSoup

path = "../tex/Q1/t3_4.tex"
f = open(path)
text = f.read()
f.close()

lst = re.findall(r'<([\w]*?)>', text)

print(lst)