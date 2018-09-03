from datetime import date, timedelta
from time import sleep
from random import randint
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui, expected_conditions as EC
from celery import group

from airbnb import app
from conf import chrome_driver_path

search_filter_collapsed_xpath = "//div[contains(@class, 'is-collapsed') and contains(@class, 'SidebarFilterModule')]"
quality_filter_xpath = "//div[@data-filter-type='quality']/select/option[@data-nav='search_filter_quality_off']"

TWITTER_ROOT_URL = 'https://twitter.com'
PAGE_TWITTER_SEARCH = f'{TWITTER_ROOT_URL}/search-advanced'
SCROLL_PAUSE_TIME = 3
RANDINT_SCROLL = randint(0, 30)


def make_driver():

    f_options = FirefoxOptions()
    f_options.set_headless(headless=True)

    c_options = ChromeOptions()
    c_options.add_argument("--headless")
    c_options.add_argument("start-maximized")
    c_options.add_argument("disable-infobars")
    c_options.add_argument("--disable-extensions")

    # driver = webdriver.Firefox(firefox_options=options, executable_path='/home/shihhao/testing/geckodriver')
    driver = webdriver.Chrome(chrome_options=c_options,
                              executable_path=chrome_driver_path)
    driver.implicitly_wait(20)
    driver.maximize_window()

    return driver


def process_dates():
    response = group(print_date.s(i) for i in dates_list())()
    # 直接使用 response.get() 會凍結，找不出原因

    with open("test.txt", 'a') as f:
        for result in response.results:
            print(result.get())
            f.write(result.get() + '\n')


@app.task(bind=True, max_retries=3, default_retry_delay=30 * 60)
def crawl_twitter(self, form_data):
    print(form_data)
    driver = make_driver()
    driver.get(PAGE_TWITTER_SEARCH)
    try:

        submit_twitter_advance_search(driver, **form_data)
        off_quality_filter(driver)

        for i in scroll_down(driver=driver):
            sleep(randint(1,3))

        result = driver.find_element_by_id("timeline").get_attribute("outerHTML")
        return result

    except Exception as exc:
        print(exc)
        raise self.retry(exc=exc)


    finally:
        driver.close()


def submit_twitter_advance_search(driver, **kwargs):
    button_xpath = "//div[@class='main']//form//button[@type='submit']"

    for key, value in kwargs.items():
        key = driver.find_element_by_xpath(key)
        key.clear()
        key.send_keys(value)
        sleep(1)


    ele = driver.find_element_by_xpath(button_xpath)
    actionChains = ActionChains(driver)
    actionChains.double_click(ele).perform()

    ui.WebDriverWait(driver, 10, 0.5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "SearchNavigation"))
    )


def off_quality_filter(driver):
    current_url = driver.current_url
    print(current_url)
    url = current_url + '&qf=off'  # quality_filter_off
    driver.get(url)
    ui.WebDriverWait(driver, 10, 0.5).until(
        (lambda driver: '&qf=off' in driver.current_url)
    )


def scroll_down(driver, retry_times=3):
    """ Scroll down to bottom, then calculate new scroll height and compare
    with last scroll height
    """

    last_height = driver.execute_script("return document.body.scrollHeight")
    new_height = 0
    times = 0
    retried = 0

    while (last_height != new_height) and retried < retry_times:
        times += 1
        last_height = new_height
        driver.execute_script(f"window.scrollTo(0, (document.body.scrollHeight));")
        new_height = driver.execute_script("return document.body.scrollHeight")

        if last_height == new_height:
            retried += 1
        else:
            retried = 0
        yield

    else:
        print(f"scroll_times = {times}")
        print("No more content")
        return


def dates_list():
    since = date(2016, 1, 1)

    ls = []
    day_range = 10

    while since <= date.today():
        since_1 = since + timedelta(days=day_range)
        ls.append((since, since_1))
        since += timedelta(days=day_range)

    ls.append((since-timedelta(days=day_range), date.today()))

    return ls
