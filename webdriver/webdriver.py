from selenium import webdriver
import platform

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")


class WebDriver:
    @staticmethod
    def get_driver(with_chrome_options=False, window_size=(1280, 1000)):
        global chrome_options
        operationalSystem = platform.system()
        PATH = 'Setup/Selenium/chromedriver.exe' if operationalSystem == 'Windows' else 'Setup/Selenium/chromedriver'
        driver = webdriver.Chrome(PATH, chrome_options=chrome_options if with_chrome_options else None)
        driver.set_window_size(*window_size)
        return driver