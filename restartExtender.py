from time import sleep
from selenium import webdriver
from pythonping import ping
import datetime

url = 'http://192.168.1.251'


def ping_p(host, fail_count) -> int:
    ping_results = ping(host, size=40, count=10)

    if ping_results.rtt_avg_ms > 1000:
        fail_count = fail_count + 1
    else:
        fail_count = 0

#    print(host + "\tRTT avg:\t" + str(ping_results.rtt_avg_ms) + "ms\t" + "fail_count:" + str(fail_count))

    return fail_count


camera_1 = 0
camera_2 = 0
camera_3 = 0
camera_4 = 0
camera_max_fail_count = 6

while 1:
    camera_1 = ping_p('192.168.1.22', camera_1)
    camera_2 = ping_p('192.168.1.26', camera_2)
    camera_3 = ping_p('192.168.1.27', camera_3)
    camera_4 = ping_p('192.168.1.28', camera_4)

    if camera_1 > camera_max_fail_count or \
       camera_2 > camera_max_fail_count or \
       camera_3 > camera_max_fail_count or \
       camera_4 > camera_max_fail_count:

        now = datetime.datetime.now()

        print(now.strftime("%Y-%m-%d %H:%M:%S") + " camera offline - restarting")
        # Start Chrome browser
        loptions = webdriver.ChromeOptions()
        loptions.add_argument('headless')
        loptions.add_argument('disable-gpu')

        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=loptions)
        driver.get(url + '/BAK_restart.htm')
        button = driver.find_element_by_name('ROMRestart')
        button.click()

        camera_1 = 0
        camera_2 = 0
        camera_3 = 0
        camera_4 = 0
        sleep(120)
        print("Done!")

    sleep(10)
