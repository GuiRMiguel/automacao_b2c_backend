import time
from ..interface import HGUModelInterface
from selenium.webdriver.common.action_chains import ActionChains 


class HGU_MItraStarECNT(HGUModelInterface):

    def login_support(self):
        time.sleep(2)
        user_input = self._driver.find_element_by_id('Loginuser')
        user_input.send_keys(self._username)
        time.sleep(1)
        pass_input = self._driver.find_element_by_id('LoginPassword')
        pass_input.send_keys(self._password)
        time.sleep(1)
        login_button = self._driver.find_element_by_id('Login_ID')
        login_button.click()
        time.sleep(1)
    
    def login_admin(self):
        time.sleep(2)
        user_input = self._driver.find_element_by_id('Loginuser')
        user_input.send_keys(self._username)
        time.sleep(1)
        pass_input = self._driver.find_element_by_id('LoginPassword')
        pass_input.send_keys(self._password)
        time.sleep(1)
        login_button = self._driver.find_element_by_id('Login_ID')
        login_button.click()
        time.sleep(1)

    def open_change_password_mitraStar(self):
        time.sleep(10)
        self._driver.switch_to.frame("menufrm")
        link = self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Management"]')
        link.click()
        time.sleep(1)
        link = self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Account_Settings"]')
        link.click()
        time.sleep(1)

    def admin_authentication_mitraStat(self):
        self._driver.switch_to.default_content()
        time.sleep(1)
        self._driver.switch_to.frame("basefrm")
        user_input = self._driver.find_element_by_xpath('//*[@id="Loginuser"]')
        user_input.send_keys("admin")
        pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
        pass_input.send_keys(self._password)
        login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
        time.sleep(1)
        login_button.click()
        time.sleep(1)

