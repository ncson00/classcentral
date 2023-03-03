import glob
from googletrans import Translator
from bs4 import BeautifulSoup, NavigableString, Comment
from translate_nested_tag import translate_tag

BLACKLIST = ["title", "script", "noscript", None]

translator = Translator(service_urls=['translate.googleapis.com'])

file_dir = 'www.classcentral.com/login.html'
html_doc = open(file_dir, mode='r')
soup = BeautifulSoup(html_doc, 'lxml')


tags = [tag.name for tag in soup.body.find_all()]
tags = list(set(tags))
print(tags)
# tag = soup.body.find_all('button', class_="hidden weight-semi large-up-block text-1 color-charcoal padding-right-small")[0]
# print(tag)
# print('----------------')

# translate_tag(tag)
# print(tag)

# f = open("file_dir.txt", "r")
# print(f[0])