import requests
from bs4 import BeautifulSoup
import time
from multiprocessing import Process, Manager
headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
def fetch(start, end, lst):

    for pin in range(start, end):
        r = requests.post('https://sbtet.ap.gov.in/APSBTET/results.do'
                    , data={
                        'mode': 'getData',
                        'grade1': '',
                        'grade': '',
                        'aadhar1': '21029-EC-%03d' % pin,
                        'grade2': '4SEM'
                    }, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        res = soup.select('#altrowstable1 > tr:nth-child(16) > td')
        results = [k.text.split(' ')[0].strip() for k in res]
        lst.append(results[0] if results != [] else None)
        print(results)
        # #altrowstable1 > tbody > tr:nth-child(14) > td
        # #altrowstable1 > tbody > tr:nth-child(14) > td
if __name__ == '__main__':
    start = time.time()
    start_pin = 1
    processes = []
    manager = Manager()
    lst = manager.list()
    for i in range(1, 181):
        if i % 3 == 0:
            p = Process(
                target=fetch,
                args=(start_pin, i, lst)
            )
            p.start()
            processes.append(p)
            start_pin = i
    for p in processes:
        p.join()
    print(len(lst))
    print(lst)
    end = time.time()
    print(end-start)
import MarksFetcherReq
f = MarksFetcherReq.Fetcher()
f.fetch("21029-CM-090", "4")
