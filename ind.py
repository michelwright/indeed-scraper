from bs4 import BeautifulSoup
import requests
import re
import json
import csv


"""
----
ToDo
----
    1. Compare soup.div to object found in RegEx
        - Which has the most complete and reliable data?
    2. Finish the csv data function to save results
"""

class Indeed:

    def __init__(self, query = '', location = ''):
        self.titleElement = {'class':'jobtitle turnstileLink'}
        self.companyElement = {'class':'company'}
        self.dateElement = {'class':'date'}
        self.salaryElement = {'class':'salaryText'}
        self.locationElement = {'class':'location accessible-contrast-color-location'}

        if query != '':
            self.query = re.sub(r'\s', '+', query)
        self.query = query
        self.location = location
        #safari_mac as default header
        self.header = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
        self.results = []

    def search(self, query = '', location = '', header = ''):
        if query == '':
            print('No query specified')
            return
        self.query = re.sub(r'\s', '+', query)
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
            soup = BeautifulSoup(r.text, 'html.parser')
            self.results = soup.body.find_all('div', {'class':'jobsearch-SerpJobCard unifiedRow row result'})
        except:
            print('Error Parsing')
            pass


        self.scripts = soup.body.find_all('script', text=re.compile('jobmap'))
        self.scripts = re.findall(r'({jk.*});', str(self.scripts[0]))
        resultsObj = []

        #Data Cleansing
        for s in self.scripts:
            s = re.sub(r'\s*', '', s)
            s = s.replace("'", '"')
            s = re.sub(':"|":', '":"', s)
            s = re.sub('",', '","', s)
            s = re.sub('{["]*', '{"', s)
            s = re.sub('["]*}', '"}', s)
            jObj = json.loads(s)
            jObj['link'] = 'https://www.indeed.com/viewjob?jk='+jObj['jk']
            resultsObj.append(jObj)

        try:
            for i in range(len(self.results)):
                #Title
                if self.results[i].find('a', self.titleElement):
                    resultsObj[i]['title'] = self.results[i].find('a',{'class':'jobtitle turnstileLink'}).get_text()
                #Date Posted
                if self.results[i].find('span',self.dateElement):
                    resultsObj[i]['date'] = self.results[i].find('span',self.dateElement).get_text()
                #Salary
                if self.results[i].find('span',self.salaryElement): 
                    resultsObj[i]['salary'] = self.results[i].find('span',self.salaryElement).get_text()
                else:
                    resultsObj[i]['salary'] = '' 
        except:
            print('Error scraping data')
            pass
        
        del(self.results)
        self.results = resultsObj 
        print('Found ' + str(len(self.results)) + ' results')

    #Code - mockup
    def saveCSV(self):
        with open('data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Column1', 'Column2', 'Column3'])
                




