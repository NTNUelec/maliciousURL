import csv, os
from urllib.request import urlopen
from urllib import error
from selenium import webdriver
from selenium import common
import time

def read_file(filename):
    file = open(filename, newline='')
    rows = csv.reader(file)
    return rows

def crawl_url():
    uuid_file = open('uuid.csv', 'w+', newline='')
    uuid_file = csv.writer(uuid_file)

    driver = webdriver.PhantomJS(
        executable_path=os.path.join('phantomjs-2.1.1-linux-x86_64', 'bin', 'phantomjs')
        )
    driver.set_page_load_timeout(10)

    based_url = "https://urlscan.io/result/"

    data = read_file("old_data.csv")
    for idx, row in enumerate(data):
        if idx == 0:    # first row if info
            continue
        
        #####################
        # control
        #####################
        if idx <= 100000:
            continue
        if idx > 200000:
            break
        #####################

        url = based_url + row[2] + "/dom/"

        try:
            driver.get(url)
            code = driver.find_element_by_tag_name('code')
        except common.exceptions.TimeoutException:
            print('{} Timeout'.format(url))
            continue
        except common.exceptions.NoSuchElementException:
            print('{} cannot find code'.format(url))
            continue

        ####################################
        # wait for dynamically loading html
        ####################################
        tic = time.clock()
        flag = 0
        while not code.text:
            toc = time.clock()
            if toc - tic > 10:
                flag = 1
                break
        if flag:
            print('{} js loading fail'.format(url))
            continue
        ####################################

        uuid_file.writerow([row[2]])
        output_file = open(os.path.join('html_files', row[2] + '.html'), 'w')
        output_file.write(code.text)    # cp950 error under windows OS
        output_file.close()
        print('{} find code'.format(url))

    uuid_file.close()
    return

def main():
    if 'html_files' not in os.listdir('.'):
        os.mkdir('html_files')
    crawl_url()

if __name__ == '__main__':
    main()