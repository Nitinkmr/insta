import os
import cv2
import numpy as np
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager


class InstaPost:
    def __init__(self, account):
        try:
            self.username = account['username']
            self.password = account['password']
            self.cookies = account['cookies']

            from selenium.webdriver.chrome.options import Options
            mobile_emulation = {
               "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
               "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
            chrome_options = Options()
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            #chrome_options.addArguments("--incognito")
            self. driver = webdriver.Chrome(executable_path="/Users/nitinkumar/Downloads/chromedriver",chrome_options = chrome_options)


           # self.driver = webdriver.Chrome(executable_path="/Users/nitinkumar/Downloads/chromedriver", chrome_options=chrome_options)
        except  Exception as e:
            print(e)
            raise Exception('Can\'t fetch account details')

    # -----------------------------------------------------------------------------------------------------------------------

    def wait(self, wait_time):
        sleep(wait_time)

    # -----------------------------------------------------------------------------------------------------------------------

    def close_insta(self):
        try:
            self.driver.close()
            self.driver.quit()
            message = 'Selenium closed Successfully'
        except:
            message = 'Selenium already closed'
        finally:
            return {message}

    # -----------------------------------------------------------------------------------------------------------------------

    def click_element(self, element, text):
        sleep(3)
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, f'//{element}[contains(text(), "{text}")]'))).click()

    # -----------------------------------------------------------------------------------------------------------------------

    def log_out(self):
        # while self.driver.current_url != 'https://www.instagram.com/':
        #     sleep(5)
        # else:
        self.driver.get(f'https://www.instagram.com/{self.username}')
        options = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//button[@class="_2I5My"]'))).click()
        self.click_element('div', 'Log out')
        self.click_element('button', 'Log out')

    # -----------------------------------------------------------------------------------------------------------------------

    def log_in(self):
        self.driver.get('https://www.instagram.com/accounts/login')

        if len(self.cookies) > 0:
            for cookie in eval(self.cookies):
                self.driver.add_cookie(cookie)
        else:
            username_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Phone number, username or email address"]')))
            password_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Password"]')))
            submit = self.driver.find_element_by_xpath('//button[@type="submit"]')

            username_input.send_keys(self.username)
            password_input.send_keys(self.password)
            submit.click()

            find_list = [
                ('a', 'Not Now'),
                ('button', 'Save Info'),
                ('button', 'Cancel'),
                ('button', 'Not Now')
            ]

            for element, text in find_list:
                try:
                    self.click_element(element, text)
                except:
                    pass

            self.cookies = self.driver.get_cookies()

        self.driver.get(f'https://www.instagram.com/{self.username}')

        sleep(5)
        try:
            self.driver.find_element_by_xpath(f'//a[contains(@href, "/{self.username}/")]')
        except:
            self.cookies = []
            self.log_in()

        return {'Logged In'}


    def click_not_now(self):
        button=self.driver.find_elements_by_xpath("//*[contains(text(), 'Not now')]")
        print(len(button))
        if len(button) > 0:
            button[0].click()

    # -----------------------------------------------------------------------------------------------------------------------

    def apply_filter(self, img_path, scale_factor, back_color=None):
        img = cv2.imread(img_path)

        h, w = img.shape[:2]
        min_size = np.amin([h, w])
        max_size = np.amax([h, w])

        scale = (min_size/max_size) * scale_factor  # earlier 0.9

        overlay = cv2.resize(img, (None), fx=scale, fy=scale,
                             interpolation=cv2.INTER_AREA)

        if back_color == None:
            crop_img = img[int(h/2-min_size/2):int(h/2+min_size/2),
                           int(w/2-min_size/2):int(w/2+min_size/2)]

            back = cv2.blur(crop_img, (100, 100))

        else:
            thickness = -1
            back = cv2.rectangle(np.zeros((min_size, min_size, 3), np.uint8),
                                 (0, 0), (min_size, min_size), back_color[::-1], thickness)

        over_h, over_w, _ = overlay.shape
        back_h, back_w, _ = back.shape

        y_offset = round((back_h-over_h)/2)
        x_offset = round((back_w-over_w)/2)

        result = back.copy()
        result[y_offset:y_offset+over_h, x_offset:x_offset+over_w] = overlay

        cv2.imwrite(f'mod_{img_path}', result)
        return f'mod_{img_path}', result

    # -----------------------------------------------------------------------------------------------------------------------

    def load_img(self, post_data):
        img_path = post_data['url']
        color = post_data['color']
        caption = post_data['caption']

        self.driver.execute_script(
            "HTMLInputElement.prototype.click = function() {                     " +
            "  if(this.type !== 'file') HTMLElement.prototype.click.call(this);  " +
            "};                                                                  ")

        self.driver.find_element_by_xpath('//div[@data-testid="new-post-button"]').click()

        if color == None:
            back_color = (255, 255, 255)
            scale_factor = 1.0
        else:
            back_color = color
            scale_factor = 0.9

        # modified_img_path = os.path.abspath(self.apply_filter(img_path, scale_factor, back_color)[0])

        self.driver.find_elements_by_tag_name('input')[-1].send_keys(img_path)
        self.driver.execute_script("delete HTMLInputElement.prototype.click")

        self.click_element('button', 'Next')

        sleep(3)
        caption_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//textarea[@aria-label="Write a caption..."]')))
        caption_input.send_keys(caption)

        return {'Image Loaded and ready to publish'}

    # -----------------------------------------------------------------------------------------------------------------------

    def post_img(self):
        self.click_element('button', 'Share')
        while self.driver.current_url != 'https://www.instagram.com/':
            pass
        return {'Successfully Posted'}


account = {
    'username' : '<username>',
    'password' : '<password>',
    # 'cookies' : '<pickle cookies>', # to load without credentials
}

post_data = {
    'url' : '<img_path>',
    'color' : '<rgb_background_color_for_image>', # or leave it as None
    'caption' : '<caption>'
}

# ip = InstaPost(account)
# ip.log_in()

# ip.load_img(post_data)
# ip.post_img()

# # if don't want to use cookies
# ip.log_out()

# # else
# ip.close_insta()
