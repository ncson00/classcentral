import time
import argparse

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
        elif len(tag.contents) > 1:
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


def main(file_dir):

    html_doc = open(file_dir, mode='r')
    soup = BeautifulSoup(html_doc, 'lxml')

    tags = [tag.name for tag in soup.body.find_all()]
    tag_names = list(set(tags).difference(set(BLACKLIST)))

    for tag_name in tag_names:
        for tag in soup.body.find_all(tag_name):
            translate_tag(tag)

    with open(file_dir, 'w') as f:
        f.write(str(soup))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    # Adding optional argument
    parser.add_argument("-d", "--file_dir", help="HTML file directory")

    args = parser.parse_args()
    if not args.file_dir:
        raise IOError("File directory must be specify from arguments!!!")

    start = time.time()
    main(args.file_dir)
    print('INFO - Took {} secs'.format(time.time() - start))