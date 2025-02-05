# import required libraries
from seleniumbase import Driver
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from environment variables
EMAIL = os.getenv('DEEPSEEK_EMAIL')
PASSWORD = os.getenv('DEEPSEEK_PASSWORD')

# initialize driver with UC mode enabled in GUI mode
driver = Driver(uc=True, headless=False, proxy=None)

# set target URL
url = "https://chat.deepseek.com/sign-in"

# open URL using UC mode with 6 second reconnect time to bypass initial detection
driver.uc_open_with_reconnect(url, reconnect_time=6)

# Wait for page to load and handle any initial challenges
driver.sleep(5)

# attempt to bypass CAPTCHA if present using UC mode's built-in method
driver.uc_gui_click_captcha()

# Wait for login form to be visible
email_input = 'input[placeholder*="Phone number / email"]'
driver.wait_for_element_visible(email_input)

# Input email and password
driver.type(email_input, EMAIL)
driver.type('input[type="password"]', PASSWORD)

# Wait for and click the terms checkbox by finding the container with the terms text
driver.wait_for_element_visible('div:contains("Terms of Use")')
driver.click('div.ds-checkbox-wrapper div[tabindex="0"]')

# Click the login button by finding the button with role and text
driver.click('div[role="button"]:contains("Log in")')

# Wait for login to complete
driver.sleep(5)

# take a screenshot of the current page
driver.save_screenshot("login-result.png")

# close the browser and end the session
driver.quit()
