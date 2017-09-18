from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import argparse
 
class MyHTMLParser(HTMLParser):
 
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]
 
    def saveLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if 'text/html' in response.getheader('Content-Type'):
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]
 
def spyglass(url, word, maxPages):
    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False
    while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
        numberVisited = numberVisited + 1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            print("Site number", numberVisited, ":", url)
            parser = MyHTMLParser()
            data, links = parser.saveLinks(url)
            pagesToVisit = pagesToVisit + links
            if data.find(word)>-1:
                foundWord = True
                print("--Success--")
        except:
            print("--Exception--")
    if foundWord:
        print("Found the word", word, "at", url)
    else:
        print("Could not find the word")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--startsite', default="https://www.wowhead.com")
    parser.add_argument('-w', '--word', default="mythic")
    parser.add_argument('-m', '--max', default=10)
    args = parser.parse_args()
    spyglass(args.startsite, args.word, args.max)