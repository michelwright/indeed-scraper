import requests
from bs4 import BeautifulSoup
import re
import json



class Indeed:
    def __init__(self, query = '', location = ''):
        self.query = query
        self.location = location
        #safari_mac as default header
        self.header = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
        self.results = []

    def search(self, query = '', location = '', header = ''):
        if query == '':
            print('No query specified')
            return
        self.query = query
        if location == '':
            print('Location not set. Searching all.')
        self.location = location
        if header == '':
            header = self.header
        self.url = 'https://www.indeed.com/jobs?q='+self.query+'&l='+self.location+'&sort=date'
        try:
            r = requests.get(self.url, header)
        except (requests.ConnectionError):
            print('Error: Problem Connecting')
            pass
        try:
            self.soup = BeautifulSoup(r.text, 'html.parser')
        except:
            print('Error Parsing')
            pass

        self.scripts = self.soup.body.find_all('script', text=re.compile('jobmap'))
        self.scripts = re.findall(r'({jk.*});', str(self.scripts[0]))
        self.results = []
        #Perform Data Cleansing
        for s in self.scripts:
            s = re.sub(r'\s*', '', s)
            s = s.replace("'", '"')
            s = re.sub(':"|":', '":"', s)
            s = re.sub('",', '","', s)
            s = re.sub('{["]*', '{"', s)
            s = re.sub('["]*}', '"}', s)
            jObj = json.loads(s)
            self.results.append(jObj)

        print('Found ' + str(len(self.results)) + ' results')
