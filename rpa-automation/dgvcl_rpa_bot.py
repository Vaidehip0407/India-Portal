#!/usr/bin/env python3
"""
DGVCL RPA Bot - Complete Automation Solution
Automates the entire DGVCL name change process without browser extensions
"""

import time
import json
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DGVCLRPABot:
    def __init__(self, headless=False):
        """Initialize the RPA bot with Chrome driver"""
        self.driver = None
        self.headless = headless
        self.status_callback = None
        
    def setup_driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        try:
            # Try system ChromeDriver first
            try:
                service = Service('/usr/local/bin/chromedriver')
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("✅ Chrome driver initialized with system ChromeDriver")
            except Exception as e:
                logger.warning(f"System ChromeDriver failed: {e}")
                # Fallback to WebDriver Manager
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("✅ Chrome driver initialized with WebDriver Manager")
            
            # Set longer timeouts
            self.driver.implicitly_wait(15)
            self.driver.set_page_load_timeout(60)
            self.driver.set_script_timeout(30)
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize Chrome driver: {e}")
            return False
    
    def update_status(self, step, message, status="processing"):
        """Update status for real-time monitoring"""
        status_data = {
            "step": step,
            "message": message,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        logger.info(f"🔄 {step}: {message}")
        
        if self.status_callback:
            self.status_callback(status_data)
    
    def step1_login(self, mobile, discom="DGVCL"):
        """Step 1: Login page - Auto-fill mobile and discom"""
        try:
            self.update_status("STEP 1", "Opening DGVCL login page...")
            
            # Navigate to login page with parameters
            login_url = f"https://portal.guvnl.in/login.php?mobile={mobile}&discom={discom}"
            logger.info(f"Navigating to: {login_url}")
            
            # Use get with retry mechanism
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    self.driver.get(login_url)
                    break
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(5)
            
            # Wait for page to load with explicit wait
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                self.update_status("STEP 1", "✅ Page loaded successfully")
            except TimeoutException:
                self.update_status("STEP 1", "⚠️ Page load timeout, continuing...")
            
            # Wait a bit more for dynamic content
            time.sleep(3)
            
            # Fill mobile number with multiple selectors
            mobile_selectors = [
                "//input[@placeholder='Mobile No']",
                "//input[contains(@placeholder, 'Mobile')]",
                "//input[@name='mobile']",
                "//input[@id='mobile']"
            ]
            
            mobile_input = None
            for selector in mobile_selectors:
                try:
                    mobile_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if mobile_input:
                mobile_input.clear()
                mobile_input.send_keys(mobile)
                self.update_status("STEP 1", f"✅ Mobile number filled: {mobile}")
            else:
                self.update_status("STEP 1", "⚠️ Mobile field not found")
            
            # Select DISCOM with multiple attempts
            try:
                discom_select = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "select"))
                )
                select_obj = Select(discom_select)
                
                # Try to select by text
                for option in select_obj.options:
                    if discom.upper() in option.text.upper():
                        select_obj.select_by_visible_text(option.text)
                        self.update_status("STEP 1", f"✅ DISCOM selected: {discom}")
                        break
            except TimeoutException:
                self.update_status("STEP 1", "⚠️ DISCOM dropdown not found")
            
            # Wait for manual captcha entry
            self.update_status("STEP 1", "⏳ Waiting for manual captcha entry...", "waiting")
            
            # Look for captcha field
            captcha_selectors = [
                "//input[contains(@placeholder, 'Captcha')]",
                "//input[contains(@placeholder, 'captcha')]",
                "//input[@name='captcha']",
                "//input[@id='captcha']"
            ]
            
            captcha_input = None
            for selector in captcha_selectors:
                try:
                    captcha_input = self.driver.find_element(By.XPATH, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if captcha_input:
                # Monitor captcha field and auto-click login when filled
                self.update_status("STEP 1", "✅ Captcha field found, monitoring for input...")
                
                # Wait for captcha to be entered (polling with timeout)
                captcha_timeout = 300  # 5 minutes
                start_time = time.time()
                
                while time.time() - start_time < captcha_timeout:
                    try:
                        current_value = captcha_input.get_attribute('value')
                        if current_value and len(current_value) >= 4:
                            break
                        time.sleep(2)
                    except Exception as e:
                        logger.warning(f"Error checking captcha: {e}")
                        time.sleep(2)
                
                if time.time() - start_time >= captcha_timeout:
                    self.update_status("STEP 1", "❌ Captcha timeout - no input detected", "error")
                    return False
                
                self.update_status("STEP 1", "✅ Captcha entered, clicking Login...")
                
                # Click login button
                login_selectors = [
                    "//input[@value='Login']",
                    "//button[@type='submit']",
                    "//input[@type='submit']",
                    "//button[contains(text(), 'Login')]"
                ]
                
                login_btn = None
                for selector in login_selectors:
                    try:
                        login_btn = self.driver.find_element(By.XPATH, selector)
                        break
                    except NoSuchElementException:
                        continue
                
                if login_btn:
                    login_btn.click()
                    self.update_status("STEP 1", "✅ Login button clicked, proceeding to OTP...")
                    return True
                else:
                    self.update_status("STEP 1", "❌ Login button not found", "error")
                    return False
            else:
                self.update_status("STEP 1", "❌ Captcha field not found", "error")
                return False
            
        except Exception as e:
            self.update_status("STEP 1", f"❌ Login failed: {str(e)}", "error")
            logger.error(f"Login step failed: {e}")
            return False
    
    def step2_otp(self):
        """Step 2: OTP page - Wait for manual OTP entry and auto-submit"""
        try:
            self.update_status("STEP 2", "Waiting for OTP page to load...")
            
            # Wait for OTP page
            WebDriverWait(self.driver, 15).until(
                EC.url_contains("checkOtp.php")
            )
            
            self.update_status("STEP 2", "⏳ Waiting for manual OTP entry...", "waiting")
            
            # Find OTP input field
            otp_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'OTP') or @type='text']"))
            )
            
            # Wait for OTP to be entered (polling)
            while len(otp_input.get_attribute('value')) < 4:
                time.sleep(1)
            
            self.update_status("STEP 2", "✅ OTP entered, submitting...")
            
            # Click submit button
            submit_btn = self.driver.find_element(By.XPATH, "//input[@value='Submit Otp'] | //button[@type='submit']")
            submit_btn.click()
            
            self.update_status("STEP 2", "✅ OTP submitted, proceeding...")
            return True
            
        except Exception as e:
            self.update_status("STEP 2", f"❌ OTP step failed: {str(e)}", "error")
            return False
    
    def step3_select_user(self):
        """Step 3: Select user page - Auto-submit"""
        try:
            self.update_status("STEP 3", "Auto-submitting user selection...")
            
            # Wait for select user page
            WebDriverWait(self.driver, 15).until(
                EC.url_contains("Submit_Otp.php")
            )
            
            # Auto-click submit
            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='Submit'] | //button[@type='submit']"))
            )
            submit_btn.click()
            
            self.update_status("STEP 3", "✅ User selection submitted")
            return True
            
        except Exception as e:
            self.update_status("STEP 3", f"❌ User selection failed: {str(e)}", "error")
            return False
    
    def step4_dashboard(self):
        """Step 4: Dashboard - Auto-click LT Name Change"""
        try:
            self.update_status("STEP 4", "Navigating to dashboard...")
            
            # Wait for dashboard page
            WebDriverWait(self.driver, 15).until(
                EC.url_contains("prtlDashboard.php")
            )
            
            self.update_status("STEP 4", "🔍 Looking for LT Name Change link...")
            
            # Try multiple ways to find LT Name Change link
            name_change_selectors = [
                "//a[contains(@href, 'ltNameChange')]",
                "//a[contains(@href, 'namechange')]",
                "//a[contains(text(), 'Name Change')]",
                "//a[contains(text(), 'LT Name Change')]",
                "//*[contains(text(), 'Name Change')]//ancestor::a",
                "//img[@alt='Name Change']//parent::a"
            ]
            
            name_change_link = None
            for selector in name_change_selectors:
                try:
                    name_change_link = self.driver.find_element(By.XPATH, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if name_change_link:
                self.update_status("STEP 4", "✅ Found LT Name Change link, clicking...")
                name_change_link.click()
            else:
                self.update_status("STEP 4", "❌ LT Name Change link not found", "error")
                return False
            
            self.update_status("STEP 4", "✅ Navigated to Name Change form")
            return True
            
        except Exception as e:
            self.update_status("STEP 4", f"❌ Dashboard navigation failed: {str(e)}", "error")
            return False
    
    def step5_name_change_form(self, form_data):
        """Step 5: Name Change form - Auto-fill and submit"""
        try:
            self.update_status("STEP 5", "Filling Name Change form...")
            
            # Wait for name change form page
            WebDriverWait(self.driver, 15).until(
                EC.url_contains("ltNameChange.php")
            )
            
            filled_fields = 0
            
            # Fill New Name
            if form_data.get('new_name'):
                try:
                    name_input = self.driver.find_element(By.XPATH, "//input[contains(@name, 'name') or contains(@placeholder, 'name')]")
                    name_input.clear()
                    name_input.send_keys(form_data['new_name'])
                    filled_fields += 1
                    self.update_status("STEP 5", f"✅ New name filled: {form_data['new_name']}")
                except NoSuchElementException:
                    logger.warning("New name field not found")
            
            # Fill Reason dropdown
            if form_data.get('reason'):
                try:
                    reason_select = Select(self.driver.find_element(By.XPATH, "//select[contains(@name, 'reason')]"))
                    reason_select.select_by_visible_text(form_data['reason'])
                    filled_fields += 1
                    self.update_status("STEP 5", f"✅ Reason selected: {form_data['reason']}")
                except NoSuchElementException:
                    logger.warning("Reason dropdown not found")
            
            # Handle Security Deposit radio buttons
            if form_data.get('security_deposit_option'):
                try:
                    radio_buttons = self.driver.find_elements(By.XPATH, "//input[@type='radio']")
                    for radio in radio_buttons:
                        if form_data['security_deposit_option'].lower() in radio.get_attribute('value').lower():
                            radio.click()
                            filled_fields += 1
                            self.update_status("STEP 5", f"✅ Security deposit option selected: {form_data['security_deposit_option']}")
                            break
                except NoSuchElementException:
                    logger.warning("Security deposit radio buttons not found")
            
            # Fill Old Security Deposit Amount
            if form_data.get('old_security_deposit'):
                try:
                    deposit_input = self.driver.find_element(By.XPATH, "//input[contains(@name, 'deposit') or contains(@name, 'amount')]")
                    deposit_input.clear()
                    deposit_input.send_keys(form_data['old_security_deposit'])
                    filled_fields += 1
                    self.update_status("STEP 5", f"✅ Old security deposit filled: {form_data['old_security_deposit']}")
                except NoSuchElementException:
                    logger.warning("Security deposit amount field not found")
            
            self.update_status("STEP 5", f"✅ Filled {filled_fields} fields, submitting form...")
            
            # Submit form
            submit_btn = self.driver.find_element(By.XPATH, "//input[@value='Submit'] | //button[@type='submit']")
            submit_btn.click()
            
            self.update_status("STEP 5", "✅ Name Change form submitted successfully!", "success")
            return True
            
        except Exception as e:
            self.update_status("STEP 5", f"❌ Form submission failed: {str(e)}", "error")
            return False
    
    def run_complete_automation(self, form_data, status_callback=None):
        """Run the complete DGVCL automation process"""
        self.status_callback = status_callback
        
        try:
            # Setup driver
            if not self.setup_driver():
                return {"success": False, "error": "Failed to setup browser driver"}
            
            # Extract data
            mobile = form_data.get('mobile')
            discom = form_data.get('provider', 'DGVCL')
            
            # Run all steps
            steps = [
                (self.step1_login, [mobile, discom]),
                (self.step2_otp, []),
                (self.step3_select_user, []),
                (self.step4_dashboard, []),
                (self.step5_name_change_form, [form_data])
            ]
            
            for step_func, args in steps:
                if not step_func(*args):
                    return {"success": False, "error": f"Failed at {step_func.__name__}"}
                time.sleep(2)  # Brief pause between steps
            
            # Success
            self.update_status("COMPLETE", "🎉 DGVCL Name Change automation completed successfully!", "success")
            return {"success": True, "message": "Automation completed successfully"}
            
        except Exception as e:
            error_msg = f"Automation failed: {str(e)}"
            self.update_status("ERROR", error_msg, "error")
            return {"success": False, "error": error_msg}
            
        finally:
            # Cleanup
            if self.driver:
                time.sleep(5)  # Keep browser open for 5 seconds to see result
                self.driver.quit()
                logger.info("🔄 Browser closed")

# Test function
def test_dgvcl_automation():
    """Test the DGVCL automation with sample data"""
    test_data = {
        "mobile": "9870083162",
        "provider": "DGVCL",
        "new_name": "Test Name Change",
        "reason": "Marriage",
        "security_deposit_option": "entire",
        "old_security_deposit": "1000",
        "applicant_name": "Test User",
        "email": "test@example.com"
    }
    
    def status_update(status):
        print(f"Status Update: {status}")
    
    bot = DGVCLRPABot(headless=False)  # Set to True for headless mode
    result = bot.run_complete_automation(test_data, status_update)
    print(f"Final Result: {result}")

if __name__ == "__main__":
    test_dgvcl_automation()