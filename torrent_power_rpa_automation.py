#!/usr/bin/env python3
"""
Torrent Power RPA Automation
Automates name change process on Torrent Power portal
"""
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

class TorrentPowerRPA:
    def __init__(self, headless=True):
        self.setup_driver(headless)
        self.wait = WebDriverWait(self.driver, 20)
        
    def setup_driver(self, headless=True):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def login(self, username, password):
        """Login to Torrent Power portal"""
        try:
            print("🔐 Logging into Torrent Power portal...")
            
            # Navigate to login page
            self.driver.get("https://connect.torrentpower.com/tplcp/session/signin")
            time.sleep(3)
            
            # Find and fill username
            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.clear()
            username_field.send_keys(username)
            
            # Find and fill password
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(password)
            
            # Handle captcha if present
            try:
                captcha_field = self.driver.find_element(By.NAME, "captcha")
                print("⚠️ Captcha detected - manual intervention required")
                input("Please solve captcha and press Enter to continue...")
            except NoSuchElementException:
                pass
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for dashboard to load
            self.wait.until(EC.url_contains("dashboard"))
            print("✅ Login successful!")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def navigate_to_name_change(self):
        """Navigate to name change application"""
        try:
            print("🧭 Navigating to name change application...")
            
            # Look for "Apply now" button on dashboard
            apply_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Apply now')]")
            if apply_buttons:
                apply_buttons[0].click()
                time.sleep(2)
            
            # Navigate to applications page
            self.driver.get("https://connect.torrentpower.com/tplcp/application/myapplications")
            time.sleep(3)
            
            # Click on "Name change" option
            name_change_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Name change')]"))
            )
            name_change_button.click()
            time.sleep(3)
            
            # Wait for name change form to load
            self.wait.until(EC.url_contains("namechangerequest"))
            print("✅ Name change form loaded!")
            return True
            
        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            return False
    
    def fill_name_change_form(self, form_data):
        """Fill the name change form automatically"""
        try:
            print("📝 Filling name change form...")
            
            # Select city dropdown
            if form_data.get('city'):
                city_dropdown = Select(self.driver.find_element(By.NAME, "city"))
                city_dropdown.select_by_visible_text(form_data['city'])
                time.sleep(1)
            
            # Fill service number
            if form_data.get('service_number'):
                service_field = self.driver.find_element(By.NAME, "serviceNumber")
                service_field.clear()
                service_field.send_keys(form_data['service_number'])
                time.sleep(1)
            
            # Fill mobile number
            if form_data.get('mobile'):
                mobile_field = self.driver.find_element(By.NAME, "mobileNumber")
                mobile_field.clear()
                mobile_field.send_keys(form_data['mobile'])
                time.sleep(1)
            
            # Fill email
            if form_data.get('email'):
                email_field = self.driver.find_element(By.NAME, "email")
                email_field.clear()
                email_field.send_keys(form_data['email'])
                time.sleep(1)
            
            # Handle captcha
            try:
                captcha_field = self.driver.find_element(By.NAME, "captcha")
                print("⚠️ Captcha detected - manual intervention required")
                input("Please solve captcha and press Enter to continue...")
            except NoSuchElementException:
                pass
            
            print("✅ Form filled successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Form filling failed: {e}")
            return False
    
    def submit_application(self):
        """Submit the name change application"""
        try:
            print("📤 Submitting application...")
            
            # Find and click submit button
            submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
            submit_button.click()
            
            # Wait for confirmation
            time.sleep(5)
            
            # Check for success message or application number
            try:
                success_message = self.driver.find_element(By.XPATH, "//*[contains(text(), 'success') or contains(text(), 'submitted')]")
                print(f"✅ Application submitted successfully: {success_message.text}")
                return True
            except NoSuchElementException:
                print("⚠️ Application submitted but no confirmation message found")
                return True
                
        except Exception as e:
            print(f"❌ Submission failed: {e}")
            return False
    
    def automate_name_change(self, login_data, form_data):
        """Complete automation flow"""
        try:
            print("🚀 Starting Torrent Power name change automation...")
            
            # Step 1: Login
            if not self.login(login_data['username'], login_data['password']):
                return {"success": False, "error": "Login failed"}
            
            # Step 2: Navigate to name change
            if not self.navigate_to_name_change():
                return {"success": False, "error": "Navigation failed"}
            
            # Step 3: Fill form
            if not self.fill_name_change_form(form_data):
                return {"success": False, "error": "Form filling failed"}
            
            # Step 4: Submit (optional - can be manual)
            print("📋 Form ready for submission!")
            print("You can now manually review and submit the form")
            
            # Take screenshot for verification
            screenshot_path = f"torrent_power_form_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            
            return {
                "success": True,
                "message": "Name change form filled successfully",
                "screenshot": screenshot_path,
                "next_step": "Manual review and submission recommended"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Close browser and cleanup"""
        if hasattr(self, 'driver'):
            self.driver.quit()

# Example usage
def test_torrent_power_automation():
    """Test the automation with sample data"""
    
    # Login credentials (user needs to provide)
    login_data = {
        "username": "your_username",
        "password": "your_password"
    }
    
    # Form data to fill
    form_data = {
        "city": "Ahmedabad",
        "service_number": "TP2025123456",
        "mobile": "9876543210",
        "email": "user@example.com"
    }
    
    # Run automation
    rpa = TorrentPowerRPA(headless=False)  # Set to True for headless mode
    result = rpa.automate_name_change(login_data, form_data)
    
    print("\n🎯 Automation Result:")
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Message: {result['message']}")
        print(f"Screenshot: {result['screenshot']}")
    else:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    test_torrent_power_automation()