import threading
import time
from MarksFetcherReq import Fetcher
from banners import *
import saver
import converter

from os import system

details = list()
results = list()
info = dict()


def validate_pin(start_pin_):
    try:
        len_ = len(start_pin_)
        if not ((len_ == 11) or (len_ == 12) or (len_ == 13)):
            raise AssertionError
        start_pin_ = start_pin_.split('-')
        if len(start_pin_) != 3:
            raise AssertionError
        assert start_pin_[0].isnumeric()
        branch = start_pin_[1]
        assert branch.isalpha()
        assert start_pin_[2].isdigit()
        return True
    except AssertionError or IndexError:
        raise


def get_details():
    valid_sems = '1 3 4 5 6 7'.split(' ')
    sp = input("Enter Start Pin: ")
    while not validate_pin(sp):
        print(red + "Enter Correct Start Pin!")
        sp = input(reset + cyan + "Enter Start Pin: ")
    details.append(sp)
    ep = input("Enter End Pin: ")
    while not validate_pin(ep):
        print(red + "Enter Correct End Pin!")
        ep = input(reset + cyan + "Enter End Pin: ")
    details.append(ep)
    sem_ = input("Enter Sem: ")
    if sem_ not in valid_sems:
        print(red + "Enter Correct sem!")
        sem_ = input(reset + "Enter Sem: ")
    details.append(sem_)
    subs_ = input("Enter Number of Subjects: ")
    while not subs_.isdigit():
        subs_ = input(reset + cyan + "Enter Number of Subjects Correctly: ")
    details.append(subs_)
    system("cls") if sys.platform == 'win32' else system("clear")
    con = input(
        green + f"Entered Details:\nStarting Pin: {sp}\nEnding Pin: {ep}\nSem: {sem_}\nSubjects: {subs_}\nPress Enter To Confirm!")
    if con != '':
        print("Abort! Re-Run The Script - Pmk")
        exit()
    system("cls") if sys.platform == 'win32' else system("clear")


def extract_pins(start_pin_, end_pin_, subs_):
    global info
    year = start_pin_[0:5]
    branch = start_pin_[6:8] if start_pin_[6:8].isalpha() else start_pin_[6:7]
    if start_pin_[6:9].isalpha():
        branch = start_pin_[6:9]
    start_pin_ = start_pin_[::-1][0:3][::-1]
    end_pin_ = end_pin_[::-1][0:3][::-1]
    info = {
        'year': year,
        'branch': branch.upper(),
        'start_pin': int(start_pin_),
        'end_pin': int(end_pin_),
        'subs': int(subs_)
    }


def fetch(start, end, year, branch, sem_, incoming_results, subs_):
    fetcher = Fetcher()
    for Pin in range(start, end):
        PIN = year + '-' + branch + '-' + '%03d' % Pin
        res = fetcher.fetch(PIN, sem_, subs_)
        if res != {}:
            print(green + "Result Fetch Successful For Pin %s!" % PIN)
            incoming_results.append(res)
        else:
            print(red + "Result Fetch UnSuccessful For Pin %s!" % PIN)


def run():
    start_banner()
    get_details()
    if sys.platform == 'darwin':
        processes_count = {
            'CM': 5,
            'EE': 5,
            'EC': 5,
            'MNG': 2,
            'C': 5,
            'M': 5
        }
    else:
        processes_count = {
            'CM': 15,
            'EE': 15,
            'EC': 15,
            'MNG': 10,
            'C': 15,
            'M': 15
        }
    print(reset)
    start_time = time.time()
    extract_pins(details[0], details[1], details[3])
    start_pin = bak = info['start_pin']
    end_pin = info['end_pin']
    year_ = info['year']
    branch_ = info['branch']
    subs = info['subs']
    sem = details[2]
    threads = []
    for pin in range(start_pin, end_pin + 1):
        if pin % processes_count[branch_] == 0:
            print(blue + f"NEW THREAD WITH PINS FROM {start_pin} TO {pin}!")
            t = threading.Thread(target=fetch,
                                 args=(start_pin, pin, year_, branch_, sem, results, subs))
            t.start()
            threads.append(t)
            start_pin = pin
    for t in threads:
        t.join()
    end_time = time.time()
    # system("cls") if sys.platform == 'win32' else system("clear")
    print(f"Took %.4f Time For Fetching {end_pin + 1 - bak} Results!" % (end_time - start_time))
    print(yellow + "Saving Results...")
    try:
        saver.save(f'static/{start_pin}', list(results))
    except PermissionError:
        print(red + "Saving the results failed due to Exception!\n"
                    "Please Check The Permissions!")
        end_banner()
        input("Press Enter To Exit!")
        exit(1)
    print(green + "Save Successful!")
    print(yellow + "Converting Results to Excel Format...")
    name = input(reset + "Enter Name for the Excel File: ")
    converter.Converter(results_path=f"static/{start_pin}", file_path=name + '.xlsx', branch=branch_,
                        sem=sem, subjects=subs).save_results()
    print(green + "Convert Success and saved as %s" % name + '.xlsx')
    input("Press Enter To Exit!")
    system("cls") if sys.platform == 'win32' else system("clear")
    end_banner()
    input()


if __name__ == '__main__':
    run()
