import time
from ..interface import HGUModelInterface
from selenium.webdriver.common.action_chains import ActionChains 


class HGU_MItraStarBROADCOM(HGUModelInterface):

    def login_support(self):
        # Entering on Advanced Interface
        self._driver.get('http://' + self._address_ip + '/padrao')
        time.sleep(3)
        frame = self._driver.find_element_by_xpath('/html/frameset/frame')
        self._driver.switch_to.frame(frame)
        time.sleep(3)
        self._driver.find_element_by_xpath('//*[@id="user"]').send_keys("support")
        self._driver.implicitly_wait(10)
        self._driver.find_element_by_xpath('//*[@id="pass"]').send_keys(self._password)
        time.sleep(1)
        self._driver.find_element_by_xpath('//*[@id="acceptLogin"]').click()
        time.sleep(3)

    # def open_change_password_mitraStar(self):
    #     time.sleep(10)
    #     self._driver.switch_to.frame("menufrm")
    #     link = self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Management"]')
    #     link.click()
    #     time.sleep(1)
    #     link = self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Account_Settings"]')
    #     link.click()
    #     time.sleep(1)

    def admin_authentication_mitraStat(self):
        time.sleep(5)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame("basefrm")
        time.sleep(1)
        user_input = self._driver.find_element_by_xpath('//*[@id="user"]')
        user_input.send_keys(self._username)
        pass_input = self._driver.find_element_by_xpath('//*[@id="pass"]')
        pass_input.send_keys(self._password)
        login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]/span')
        time.sleep(1)
        login_button.click()
        time.sleep(1)

