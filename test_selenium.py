from time import sleep
from random import randint

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui, expected_conditions as EC


TWITTER_ROOT_URL = 'https://twitter.com'
PAGE_TWITTER_SEARCH = f'{TWITTER_ROOT_URL}/search-advanced'

f_options = FirefoxOptions()
f_options.set_headless(headless=True)

c_options = ChromeOptions()
# c_options.add_argument("--headless")
c_options.add_argument("start-maximized")
c_options.add_argument("disable-infobars")
c_options.add_argument("--disable-extensions")


'''
Advance Search Page
'''

# Search Form
ands_xpath = "//input[@name='ands']"
phrase_xpath = "//input[@name='phrase']"
ors_xpath = "//input[@name='ors']"
nots_xpath = "//input[@name='nots']"
tag_xpath = "//input[@name='tag']"
from_xpath = "//input[@name='from']"
to_xpath = "//input[@name='to']"
ref_xpath = "//input[@name='ref']"
near_xpath = "//input[@name='near']"
button_xpath = "//div[@class='main']//form//button[@type='submit']"
lang_xpath = "//select[@id='lang']"

# time format yyyy-mm-dd
since_xpath = "//input[@id='since']"
until_xpath = "//input[@id='until']"


# driver = webdriver.Firefox(firefox_options=options, executable_path='/home/shihhao/testing/geckodriver')
driver = webdriver.Chrome(chrome_options=c_options, executable_path='/home/shihhao/testing/chromedriver')
print("start browser")
driver.implicitly_wait(20)
driver.maximize_window()

driver.get(PAGE_TWITTER_SEARCH)

driver.find_element_by_xpath(ands_xpath).clear()
driver.find_element_by_xpath(ands_xpath).send_keys("airbnb")

driver.find_element_by_xpath(lang_xpath).send_keys("en")
ele = driver.find_element_by_xpath(button_xpath)

driver.find_element_by_xpath(since_xpath).clear()
driver.find_element_by_xpath(since_xpath).send_keys("2016/1/1")
driver.find_element_by_xpath(until_xpath).clear()
driver.find_element_by_xpath(until_xpath).send_keys("2016/1/2")

actionChains = ActionChains(driver)
actionChains.double_click(ele).perform()

ui.WebDriverWait(driver, 10, 0.5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "SearchNavigation"))
)

'''
Searched Page

class = SearchNavigation

https://twitter.com/search?l=en&q=airbnb&src=typd
https://twitter.com/search?vertical=default&q=airbnb&l=en&src=typd&qf=off
'''
search_filter_collapsed_xpath = "//div[contains(@class, 'is-collapsed') and contains(@class, 'SidebarFilterModule')]"
quality_filter_xpath = "//div[@data-filter-type='quality']/select/option[@data-nav='search_filter_quality_off']"
# driver.find_element_by_xpath(quality_filter_xpath).click()


current_url = driver.current_url
print(current_url)
url = current_url + '&qf=off'  # quality_filter_off
driver.get(url)
ui.WebDriverWait(driver, 10, 0.5).until(
    (lambda driver: '&qf=off' in driver.current_url)
)


SCROLL_PAUSE_TIME = 3
RANDINT_SCROLL = randint(0, 30)

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
print(last_height)


def scroll_down(driver):
    """ Scroll down to bottom, then calculate new scroll height and compare
    with last scroll height
    """

    last_height = driver.execute_script("return document.body.scrollHeight")
    new_height = 0
    times = 0
    limit = 1000
    retry = 0

    while (last_height != new_height) and times <= limit or retry <= 3:
        times += 1
        last_height = new_height
        driver.execute_script(f"window.scrollTo(0, (document.body.scrollHeight));")
        new_height = driver.execute_script("return document.body.scrollHeight")

        if last_height == new_height:
            retry += 1
        else:
            retry = 0
        yield

    else:
        print(f"times = {times}")
        print(f"retry = {retry}")
        print("No more content")
        return


for i in scroll_down(driver=driver):
    sleep(3)


page_source = driver.find_element_by_id("timeline").get_attribute("outerHTML")
with open("test_headless.html", "w") as f:
    f.write(page_source)


driver.close()
