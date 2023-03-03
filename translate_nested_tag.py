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


def main(file_dir, nested_tags):

    html_doc = open(file_dir, mode='r')
    soup = BeautifulSoup(html_doc, 'lxml')

    for nested_tag in nested_tags:
        for tag in soup.body.find_all(nested_tag):
            translate_nested_tag(tag)

    with open(file_dir, 'w') as f:
        f.write(str(soup))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    # Adding optional argument
    parser.add_argument('-d', '--file_dir', help='HTML file directory')
    parser.add_argument('-n', '--nested_tags', nargs='+', help='List of nested tag names', required=True)

    args = parser.parse_args()
    if not args.file_dir:
        raise IOError("File directory must be specify from arguments!!!")
    if not args.nested_tags:
        raise IOError("List of nested tags must be specify from arguments!!!")

    start = time.time()
    main(args.file_dir, args.nested_tags)
    print('INFO - Took {} secs'.format(time.time() - start))