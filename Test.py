import requests
from bs4 import BeautifulSoup
import numpy as np
class Analyse_Name():
    result_url = "https://www.google.com/search?q="
    origin_url = "https://www.behindthename.com/name/"

    names_array =  'james,john,robert,michael,william,david,richard,charles,joseph,thomas,christopher,daniel,paul,mark,donald,\
george,kenneth,steven,edward,brian,ronald,anthony,kevin,jason,matthew,gary,timothy,jose,larry,jeffrey,frank,scott,\
eric,stephen,andrew,raymond,gregory,joshua,jerry,dennis,walter,patrick,peter,harold,douglas,henry,\
carl,arthur,ryan,roger,joe,juan,jack,albert,jonathan,justin,terry,gerald,keith,samuel,willie,ralph,lawrence,nicholas'.split(',')

    def __init__(self):
        self.resultCount = []
        self.nameOriginCount = []

    @classmethod
    def crawlingResultData(cls,name):
        link = Analyse_Name.result_url + name
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103\
            Safari / 537.36'}
        source = requests.get(link, headers=headers).text
        print(link)
        html_soup = BeautifulSoup(source, "html.parser")
        return html_soup

    @classmethod
    def crawlingOriginData(cls,name):
        link = Analyse_Name.origin_url + name
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103\
            Safari / 537.36'}
        source = requests.get(link, headers=headers).text
        print(link)
        html_soup = BeautifulSoup(source, "html.parser")
        return html_soup

    @classmethod
    def parseOriginResultCountData(cls,html_soup):

        origin_array = []
        data = html_soup.select('body > div.body-wrapper > div > div > div:nth-child(3) > article > div.infogroup > div:nth-child(2) > span.infoname-info >a')
        #res = html_soup.find('span', {'class': 'infoname-info'})
        for item in data:
            #print(item.get_text())
            origin_array.append(item.get_text())
        return ','.join(origin_array),len(data)
        #print(data)

    @classmethod
    def parseNameReslutCountData(clas,html_soup):
        res = html_soup.find('div', {'id': 'resultStats'})
        return int(res.text.replace(",", "").split()[1])

    def generateNameResultCountData(self):
        count_array = []
        html_array  = map(self.crawlingResultData, Analyse_Name.names_array)
        for html in html_array:
            count_array.append(int(self.parseNameReslutCountData(html)))
        dic_data = dict(zip(Analyse_Name.names_array, count_array))
        np_array = np.array(sorted(dic_data.items(), key=lambda x: x[1]))
        np.savetxt('./resultStatistics.csv', np_array, delimiter=',', fmt="%s")


    def generateNameOriginCountData(self):
        origin_array = []
        count_array = []
        html_array  = map(self.crawlingOriginData, Analyse_Name.names_array)
        for html in html_array:
            origin_array.append(self.parseOriginResultCountData(html)[0])
            count_array.append(int(self.parseOriginResultCountData(html)[1]))
        self.resultCount.append(Analyse_Name.names_array)
        self.resultCount.append(origin_array)
        self.resultCount.append(count_array)
        np_array_list = np.array(self.resultCount).T.tolist()
        sorted_list = sorted(np_array_list, key=lambda x: int(x[2]))
        np.savetxt('./origin.csv', np.array(sorted_list), delimiter=',', fmt="%s")


def main():
    analyse_Name = Analyse_Name()
    analyse_Name.generateNameResultCountData()
    analyse_Name.generateNameOriginCountData()


if __name__ == '__main__':
    main()
