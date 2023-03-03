import time
import glob

from googletrans import Translator
from bs4 import BeautifulSoup, NavigableString, Comment

BLACKLIST = ["title", "script", "noscript", None]

translator = Translator(service_urls=['translate.googleapis.com'])

def translate_tag(tag):
    try:
        hindi = translator.translate(tag.text, src='en', dest='hindi')
        tag.string.replace_with(hindi.text)
    except:
        pass


def translate_nested_tag(tag):

    '''Recursion Function for translating nested tags'''

    if type(tag) == Comment or tag.name in BLACKLIST: pass
    else:
        if len(tag.contents) == 1: translate_tag(tag)
        elif (len(tag.contents) > 1) & (len(tag.contents) <= 9):
            for i in range(len(tag.contents)):
                element = tag.contents[i]
                if type(element) == NavigableString:
                    try:
                        hindi = translator.translate(element.text, src='en', dest='hindi')
                        element.replace_with(hindi.text)
                    except:
                        pass
                else:
                    translate_nested_tag(element)
        else: pass


def main():

    start = time.time()
    file_done = 0

    for file_dir in glob.glob("**/*.html", recursive=True):
    # file_dir = 'www.classcentral.com/login.html'
        html_doc = open(file_dir, mode='r')
        soup = BeautifulSoup(html_doc, 'lxml')

        tags = [tag.name for tag in soup.body.find_all()]
        tag_names = list(set(tags).difference(set(BLACKLIST)))

        for tag_name in tag_names:
            for tag in soup.body.find_all(tag_name):
                translate_nested_tag(tag)

        with open(file_dir, 'w') as f:
            f.write(soup)

        file_done += 1
        print('INFO - Took {} secs. Processed successfully {} file(s)'.format(time.time() - start, file_done))
        

if __name__ == '__main__':

    main()