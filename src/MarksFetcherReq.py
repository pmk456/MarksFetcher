"""
File Name: MarksFetcherReq.py [ MuMa Parser ]
Author: Patan Musthakheem Khan
Date & Time: 22-07-2023 01:23 AM
"""
import requests

import bs4


# import subjects
class Fetcher:
    def __init__(self):
        self.req = requests.post
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) \
                             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
        self.valid_sems = '1 3 4 5 6 7'.split(' ')
        self.link = 'https://sbtet.ap.gov.in/APSBTET/gradeWiseResults.xls'

    def __request(self, payload):
        try:
            res = self.req(
                self.link,
                data=payload,
                headers=self.headers
            )
            return res
        except ConnectionError or ConnectionResetError or ConnectionAbortedError or ConnectionRefusedError or Exception:
            return self.__request(payload)

    def fetch(self, pin: str, sem_num: str, subjects) -> dict:
        pin = pin.upper()
        if sem_num not in self.valid_sems:
            return {}
        end = int(subjects)
        if sem_num == '1':
            end = 11
        sem = sem_num + 'SEM' if sem_num != '1' else '1YEAR'
        __PAYLOAD: dict = {
            'mode': 'getData',
            'grade1': '',
            'grade': '',
            'aadhar1': pin,
            'grade2': sem
        }
        res = self.__request(__PAYLOAD)
        if res.status_code == 404:
            return dict()
        try:
            soup = bs4.BeautifulSoup(res.content, 'html.parser')
            results = dict()
            raw_pin = soup.select('#altrowstable1 > tr:nth-child(3) > td:nth-child(2)')
            results["Pin"] = [k.text.split(' ')[0].strip() for k in raw_pin][0]
            for i in range(7, (end + 7)):
                raw_paper = soup.select(f'#altrowstable1 > tr:nth-child({i}) > th')
                paper = [k.text.split(' ')[0].strip() for k in raw_paper][0]
                ele = soup.select(
                    f'#altrowstable1 > tr:nth-child({i}) > td'
                )
                res = [k.text.split(' ')[0].strip() for k in ele]
                main_str = '-'.join(res)
                results[str(paper)] = main_str
            raw_total = soup.select(f'#altrowstable1 > tr:nth-child({end + 7}) > td')
            total = [k.text.split(' ')[0].strip() for k in raw_total][0]
            raw_result = soup.select(f'#altrowstable1 > tr:nth-child({end + 8}) > td')
            result = [k.text.split(' ')[0].strip() for k in raw_result][0]
            results['Total'] = int(total)
            results['Result'] = str(result)
            return results
        except Exception:
            return dict()
