import requests,re,json
from multiprocessing import Pool
from requests.exceptions import RequestException

def get_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
def re_match(html):
    match1 = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?alt="(.*?)".*?"star">(.*?)</p>.*?releasetime">(.*?)</p>.*?"integer">(.*?)</i>.*?"fraction">(.*?)</i></p>',re.S)
    result = re.findall(match1,html)
    for i in result:
        yield {
            'index':i[0],
            'url':i[1],
            'name':i[2],
            'actor':i[3].strip()[3:],
            'Release_time':i[4].strip()[5:],
            'score':i[5]+i[6]
        }

def main(page):
    url = "https://maoyan.com/board/4?offset=" + str(page)
    html = get_page(url)
    Gl = re_match(html)
    with open('film_record.txt','a') as f:
        for i in Gl:
          f.write(json.dumps(i,ensure_ascii=False)+'\n' )


if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])
