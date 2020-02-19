import os
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

class WebDriver:
    DOWNLOAD_DIR = '/tmp'

    def __init__(self, headless=True):
        self.options = webdriver.ChromeOptions()

        self.options.add_argument('--disable-extensions')
        if headless:
            #self.options.add_argument('--headless')
            self.options.add_argument('--disable-gpu')
            self.options.add_argument('--no-sandbox')

        self.options.add_experimental_option(
            'prefs', {
                'download.default_directory': self.DOWNLOAD_DIR,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True
            }
        )

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def open(self):
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver.implicitly_wait(10)

    def close(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.get('https://thomsonreuters.condecosoftware.com')
        print(self.driver.current_url)
        username_field = self.driver.find_element_by_id('userNameInput')
        username_field.clear()
        username_field.send_keys(username)

        password_field = self.driver.find_element_by_id('passwordInput')
        password_field.clear()
        password_field.send_keys(password)
        sleep(1)

        submit = self.driver.find_element_by_id('submitButton')
        submit.click()

        print(self.driver.current_url)
        sleep(5)

        print(self.driver.current_url)

        # Close today page
        self.driver.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li/a').click()
        sleep(1)
        print(self.driver.current_url)

    def load_desk_booking_page(self):
        self.driver.switch_to_frame('leftNavigation')
        self.driver.find_element_by_id('DeskBookingHeader').click()
        sleep(5)
        self.driver.find_element_by_id('li_findADesk').click()
        sleep(5)
        self.driver.switch_to_default_content()
        print(self.driver.current_url)

    def book_desk_for_next_week(self, desk_ID):
        self.driver.switch_to_frame('mainDisplayFrame')
        for x in range(7, 12):
            am_box = 'incAM_{}'.format(x)
            self.driver.find_element_by_id(am_box).click()
            pm_box = 'incPM_{}'.format(x)
            self.driver.find_element_by_id(pm_box).click()
        self.driver.find_element_by_id('btnSearch').click()
        sleep(5)
        print(self.driver.current_url)

        # hardcoded to DEP/CDO result button
        self.driver.find_element_by_id('deskSearchResultsGrid_ctl02_floorPlanButton').click()
        sleep(5)
        self.driver.switch_to_default_content()
        self.driver.switch_to_frame('mainDisplayFrame')
        self.driver.switch_to_frame('iframeFloorPlan')
        self.driver.find_element_by_id(desk_ID).click()

        # Deal with popup Window
        condeco_window = self.driver.window_handles[0]
        print(condeco_window)
        booking_window = self.driver.window_handles[1]
        print(booking_window)
        self.driver.switch_to_window(booking_window)
        self.driver.find_element_by_id('submitButton').click()


if __name__ == '__main__':
    with WebDriver() as driver:
        driver.login(os.environ['CONDECO_USER'], os.environ['CONDECO_PASS'])
        driver.load_desk_booking_page()
        # export CONDECO_DESK=item2722 for 19-N-03
        driver.book_desk_for_next_week(os.environ['CONDECO_DESK'])
        driver.close()
