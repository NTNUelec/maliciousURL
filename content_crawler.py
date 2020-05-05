import csv, os
from urllib.request import urlopen
from urllib import error
from selenium import webdriver

def read_file(filename):
    file = open(filename, newline='')
    rows = csv.reader(file)
    return rows

def crawl_url(filename = "20200415-28.csv"):
    uuid_file = open('uuid.csv', 'w+', newline='')
    uuid_file = csv.writer(uuid_file)

    driver = webdriver.PhantomJS(
        executable_path=os.path.join('phantomjs-2.1.1-linux-x86_64', 'bin', 'phantomjs')
        )
    driver.set_page_load_timeout(10)

    based_url = "https://urlscan.io/result/"

    data = read_file(filename)
    for idx, row in enumerate(data):
        if idx == 0:    # first row if info
            continue
        
        ##########################
        # control
        ##########################
        if idx < 1516:
            continue
        if idx > 80000:
            break
        ##########################

        url = based_url + row[2] + "/dom/"

        try:
            driver.get(url)
            code = driver.find_element_by_tag_name('code')
            print('{} find code'.format(url))
        except:
            print('{} cannot find code'.format(url))
            continue

        # wait for dynamically loading html
        counter = 0
        flag = 0
        while not code.text:
            if counter > 100:
                flag = 1
                break
            counter += 1
        if flag:
            continue

        uuid_file.writerow([row[2]])
        output_file = open(os.path.join('html_files', row[2] + '.html'), 'w')
        output_file.write(code.text)    # cp950 error under windows OS
        output_file.close()

    uuid_file.close()
    return

def main():
    if 'html_files' not in os.listdir('.'):
        os.mkdir('html_files')
    crawl_url("20200415-28.csv")

if __name__ == '__main__':
    main()