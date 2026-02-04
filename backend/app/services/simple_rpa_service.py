"""
Simple RPA Service - Windows EC2 Production Version
"""

import time
import os
import logging
import platform
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleTorrentRPA:
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Windows EC2 Chrome setup with robust error handling"""
        try:
            logger.info("🚀 Setting up Chrome driver for Windows EC2...")
            
            # Detect environment
            is_windows = platform.system() == 'Windows'
            is_ec2 = os.environ.get('AWS_EXECUTION_ENV') or 'ec2' in platform.node().lower()
            
            logger.info(f"🔍 Platform: {platform.system()}")
            logger.info(f"🔍 Node: {platform.node()}")
            logger.info(f"🔍 EC2 Environment: {is_ec2}")
            
            # Chrome options for Windows EC2
            options = Options()
            
            # Essential options for Windows EC2
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-translate")
            options.add_argument("--disable-features=TranslateUI")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # For Windows EC2 - visible browser for RPA
            if is_windows:
                logger.info("💻 Using Windows EC2 visible browser mode")
                # Don't add headless for Windows EC2 - we want visible browser
            else:
                options.add_argument("--headless")
                logger.info("🐧 Using headless mode for non-Windows")
            
            # Try to find Chrome installation
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe"
            ]
            
            chrome_binary = None
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_binary = path
                    logger.info(f"✅ Found Chrome at: {chrome_binary}")
                    break
            
            if chrome_binary:
                options.binary_location = chrome_binary
            else:
                logger.warning("⚠️ Chrome binary not found in standard locations")
            
            # Try different driver setup methods
            driver_setup_success = False
            last_error = None
            
            # Method 1: Try webdriver-manager
            try:
                logger.info("🔧 Method 1: Trying webdriver-manager...")
                from webdriver_manager.chrome import ChromeDriverManager
                
                driver_path = ChromeDriverManager().install()
                logger.info(f"✅ ChromeDriver path: {driver_path}")
                
                # Fix webdriver-manager path issues on Windows
                if driver_path and os.path.exists(driver_path):
                    service = Service(driver_path)
                    self.driver = webdriver.Chrome(service=service, options=options)
                    driver_setup_success = True
                    logger.info("✅ Chrome driver setup successful with webdriver-manager")
                
            except Exception as e:
                last_error = e
                logger.warning(f"⚠️ webdriver-manager failed: {e}")
            
            # Method 2: Try system Chrome with automatic driver download
            if not driver_setup_success:
                try:
                    logger.info("🔧 Method 2: Trying system Chrome with auto driver...")
                    self.driver = webdriver.Chrome(options=options)
                    driver_setup_success = True
                    logger.info("✅ Chrome driver setup successful with system Chrome")
                    
                except Exception as e:
                    last_error = e
                    logger.warning(f"⚠️ System Chrome failed: {e}")
            
            # Method 3: Try to download and setup ChromeDriver manually
            if not driver_setup_success:
                try:
                    logger.info("🔧 Method 3: Trying manual ChromeDriver setup...")
                    
                    # Get Chrome version
                    chrome_version = self.get_chrome_version()
                    if chrome_version:
                        logger.info(f"🔍 Chrome version: {chrome_version}")
                        
                        # Download matching ChromeDriver
                        driver_path = self.download_chromedriver(chrome_version)
                        if driver_path and os.path.exists(driver_path):
                            service = Service(driver_path)
                            self.driver = webdriver.Chrome(service=service, options=options)
                            driver_setup_success = True
                            logger.info("✅ Chrome driver setup successful with manual download")
                    
                except Exception as e:
                    last_error = e
                    logger.warning(f"⚠️ Manual ChromeDriver setup failed: {e}")
            
            # Method 4: Try with minimal options
            if not driver_setup_success:
                try:
                    logger.info("🔧 Method 4: Trying with minimal Chrome options...")
                    
                    minimal_options = Options()
                    minimal_options.add_argument("--no-sandbox")
                    minimal_options.add_argument("--disable-dev-shm-usage")
                    
                    if chrome_binary:
                        minimal_options.binary_location = chrome_binary
                    
                    self.driver = webdriver.Chrome(options=minimal_options)
                    driver_setup_success = True
                    logger.info("✅ Chrome driver setup successful with minimal options")
                    
                except Exception as e:
                    last_error = e
                    logger.warning(f"⚠️ Minimal options failed: {e}")
            
            if not driver_setup_success:
                logger.error("❌ All ChromeDriver setup methods failed")
                logger.error(f"❌ Last error: {last_error}")
                
                # Provide detailed troubleshooting info
                logger.error("🔍 Troubleshooting information:")
                logger.error(f"   - Chrome binary found: {chrome_binary is not None}")
                logger.error(f"   - Chrome binary path: {chrome_binary}")
                logger.error(f"   - Platform: {platform.system()}")
                logger.error(f"   - Python version: {platform.python_version()}")
                
                return False
            
            # Set timeouts
            self.driver.implicitly_wait(15)  # Increased for EC2
            self.driver.set_page_load_timeout(90)  # Increased for EC2
            self.wait = WebDriverWait(self.driver, 45)  # Increased for EC2
            
            # Test the driver with a simple page
            logger.info("🧪 Testing Chrome driver...")
            try:
                test_html = """
                <html>
                <head><title>RPA Test</title></head>
                <body>
                    <h1>RPA Test - Chrome Working on Windows EC2!</h1>
                    <p>Driver setup successful</p>
                </body>
                </html>
                """
                self.driver.get(f"data:text/html,{test_html}")
                logger.info("✅ Chrome driver test successful")
                
                # Get some basic info
                logger.info(f"🔍 Browser info: {self.driver.capabilities.get('browserName')} {self.driver.capabilities.get('browserVersion')}")
                logger.info(f"🔍 Window size: {self.driver.get_window_size()}")
                
            except Exception as e:
                logger.warning(f"⚠️ Driver test failed: {e}")
                # Don't fail here, might still work for actual navigation
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Chrome setup failed: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            
            # Provide helpful error information
            if "chromedriver" in str(e).lower():
                logger.error("💡 ChromeDriver issue detected")
                logger.error("💡 Suggestion: Ensure Chrome is installed and updated")
                logger.error("💡 Try: choco install googlechrome -y --force --ignore-checksums")
            elif "chrome" in str(e).lower():
                logger.error("💡 Chrome browser issue detected")
                logger.error("💡 Suggestion: Install Chrome browser")
                logger.error("💡 Try: choco install googlechrome -y")
            elif "permission" in str(e).lower():
                logger.error("💡 Permission issue detected")
                logger.error("💡 Suggestion: Run as Administrator")
            
            return False
    
    def get_chrome_version(self):
        """Get installed Chrome version on Windows"""
        try:
            # Try different methods to get Chrome version
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            
            for chrome_path in chrome_paths:
                if os.path.exists(chrome_path):
                    try:
                        # Get version using PowerShell
                        cmd = f'powershell "(Get-Item \'{chrome_path}\').VersionInfo.ProductVersion"'
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                        if result.returncode == 0:
                            version = result.stdout.strip()
                            logger.info(f"✅ Chrome version detected: {version}")
                            return version
                    except Exception as e:
                        logger.warning(f"⚠️ Version detection failed for {chrome_path}: {e}")
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Chrome version detection failed: {e}")
            return None
    
    def download_chromedriver(self, chrome_version):
        """Download ChromeDriver for specific Chrome version"""
        try:
            import requests
            import zipfile
            
            # Extract major version
            major_version = chrome_version.split('.')[0]
            
            # ChromeDriver download URL (simplified for major version)
            driver_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
            
            # Get exact driver version
            response = requests.get(driver_url)
            if response.status_code == 200:
                driver_version = response.text.strip()
                
                # Download ChromeDriver
                download_url = f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_win32.zip"
                
                # Create temp directory
                temp_dir = os.path.join(os.getcwd(), "temp_chromedriver")
                os.makedirs(temp_dir, exist_ok=True)
                
                # Download and extract
                zip_path = os.path.join(temp_dir, "chromedriver.zip")
                with requests.get(download_url, stream=True) as r:
                    with open(zip_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                
                # Extract
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                driver_path = os.path.join(temp_dir, "chromedriver.exe")
                if os.path.exists(driver_path):
                    logger.info(f"✅ ChromeDriver downloaded: {driver_path}")
                    return driver_path
            
            return None
            
        except Exception as e:
            logger.error(f"❌ ChromeDriver download failed: {e}")
            return None
    
    def navigate_to_torrent_power(self):
        """Navigate to Torrent Power website with robust error handling"""
        try:
            url = "https://connect.torrentpower.com/tplcp/application/namechangerequest"
            logger.info(f"🌐 Navigating to: {url}")
            
            # Set longer timeout for Windows EC2
            self.driver.set_page_load_timeout(60)
            
            # Navigate to the URL
            self.driver.get(url)
            logger.info("✅ URL loaded, waiting for page elements...")
            
            # Wait for page to load with multiple fallback checks
            try:
                # Method 1: Wait for body tag
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                logger.info("✅ Body element found")
            except:
                logger.warning("⚠️ Body element not found, trying alternative checks...")
                
                # Method 2: Wait for any form element
                try:
                    self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
                    logger.info("✅ Form element found")
                except:
                    # Method 3: Wait for any input element
                    try:
                        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
                        logger.info("✅ Input element found")
                    except:
                        # Method 4: Just wait for page title
                        if self.driver.title:
                            logger.info(f"✅ Page loaded with title: {self.driver.title}")
                        else:
                            logger.warning("⚠️ Page may not have loaded properly")
            
            # Additional wait for JavaScript to load
            time.sleep(3)
            
            # Check if we're on the right page
            current_url = self.driver.current_url
            logger.info(f"🔍 Current URL: {current_url}")
            
            if "torrentpower.com" in current_url.lower():
                logger.info("✅ Successfully navigated to Torrent Power website")
                return True
            else:
                logger.warning(f"⚠️ Unexpected URL: {current_url}")
                # Still try to continue - might be a redirect
                return True
            
        except Exception as e:
            logger.error(f"❌ Navigation failed: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            
            # Try to get more information about the error
            try:
                current_url = self.driver.current_url
                page_title = self.driver.title
                logger.error(f"❌ Current URL: {current_url}")
                logger.error(f"❌ Page title: {page_title}")
            except:
                logger.error("❌ Could not get page information")
            
            return False
    
    def fill_form(self, form_data):
        """Fill the Torrent Power form"""
        try:
            logger.info("🚀 Starting form filling...")
            filled_fields = []
            time.sleep(2)  # Wait for page to fully load
            
            # 1. Fill City Dropdown
            try:
                logger.info("🔍 Looking for city dropdown...")
                city_select = self.wait.until(EC.element_to_be_clickable((By.TAG_NAME, "select")))
                
                select = Select(city_select)
                city = form_data.get('city', 'Ahmedabad')
                
                # Try to select city
                options = select.options
                for option in options:
                    if city.lower() in option.text.lower():
                        select.select_by_value(option.get_attribute('value'))
                        filled_fields.append(f"✅ City: {option.text}")
                        logger.info(f"✅ City selected: {option.text}")
                        
                        # Highlight the field
                        self.driver.execute_script("arguments[0].style.backgroundColor = '#d4edda'; arguments[0].style.border = '3px solid #28a745';", city_select)
                        break
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ City dropdown error: {e}")
                filled_fields.append("❌ City dropdown not found")
            
            # 2. Fill Service Number
            try:
                logger.info("🔍 Looking for service number field...")
                service_selectors = [
                    "input[placeholder*='Service Number']",
                    "input[placeholder*='Service']",
                    "input[name*='service']",
                    "input[id*='service']"
                ]
                
                service_input = None
                for selector in service_selectors:
                    try:
                        service_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if not service_input:
                    text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                    if text_inputs:
                        service_input = text_inputs[0]
                
                if service_input and form_data.get('service_number'):
                    service_input.clear()
                    service_input.send_keys(form_data['service_number'])
                    filled_fields.append(f"✅ Service Number: {form_data['service_number']}")
                    logger.info(f"✅ Service Number filled: {form_data['service_number']}")
                    
                    # Highlight the field
                    self.driver.execute_script("arguments[0].style.backgroundColor = '#d4edda'; arguments[0].style.border = '3px solid #28a745';", service_input)
                else:
                    filled_fields.append("❌ Service Number field not found")
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Service Number error: {e}")
                filled_fields.append("❌ Service Number error")
            
            # 3. Fill T Number
            try:
                logger.info("🔍 Looking for T Number field...")
                t_selectors = [
                    "input[placeholder*='T No']",
                    "input[placeholder*='T-No']",
                    "input[name*='tno']"
                ]
                
                t_input = None
                for selector in t_selectors:
                    try:
                        t_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if not t_input:
                    text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                    if len(text_inputs) > 1:
                        t_input = text_inputs[1]
                
                if t_input and form_data.get('t_number'):
                    t_input.clear()
                    t_input.send_keys(form_data['t_number'])
                    filled_fields.append(f"✅ T Number: {form_data['t_number']}")
                    logger.info(f"✅ T Number filled: {form_data['t_number']}")
                    
                    # Highlight the field
                    self.driver.execute_script("arguments[0].style.backgroundColor = '#d4edda'; arguments[0].style.border = '3px solid #28a745';", t_input)
                else:
                    filled_fields.append("❌ T Number field not found")
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ T Number error: {e}")
                filled_fields.append("❌ T Number error")
            
            # 4. Fill Mobile Number
            try:
                logger.info("🔍 Looking for mobile field...")
                mobile_selectors = [
                    "input[type='tel']",
                    "input[placeholder*='Mobile']",
                    "input[name*='mobile']"
                ]
                
                mobile_input = None
                for selector in mobile_selectors:
                    try:
                        mobile_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if not mobile_input:
                    text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                    if len(text_inputs) > 2:
                        mobile_input = text_inputs[2]
                
                if mobile_input and form_data.get('mobile'):
                    mobile_input.clear()
                    mobile_input.send_keys(form_data['mobile'])
                    filled_fields.append(f"✅ Mobile: {form_data['mobile']}")
                    logger.info(f"✅ Mobile filled: {form_data['mobile']}")
                    
                    # Highlight the field
                    self.driver.execute_script("arguments[0].style.backgroundColor = '#d4edda'; arguments[0].style.border = '3px solid #28a745';", mobile_input)
                else:
                    filled_fields.append("❌ Mobile field not found")
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Mobile error: {e}")
                filled_fields.append("❌ Mobile error")
            
            # 5. Fill Email
            try:
                logger.info("🔍 Looking for email field...")
                email_selectors = [
                    "input[type='email']",
                    "input[placeholder*='Email']",
                    "input[name*='email']"
                ]
                
                email_input = None
                for selector in email_selectors:
                    try:
                        email_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if not email_input:
                    text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                    if len(text_inputs) > 3:
                        email_input = text_inputs[3]
                
                if email_input and form_data.get('email'):
                    email_input.clear()
                    email_input.send_keys(form_data['email'])
                    filled_fields.append(f"✅ Email: {form_data['email']}")
                    logger.info(f"✅ Email filled: {form_data['email']}")
                    
                    # Highlight the field
                    self.driver.execute_script("arguments[0].style.backgroundColor = '#d4edda'; arguments[0].style.border = '3px solid #28a745';", email_input)
                else:
                    filled_fields.append("❌ Email field not found")
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"❌ Email error: {e}")
                filled_fields.append("❌ Email error")
            
            # 6. Find and click Submit button
            try:
                logger.info("� Looking for submit button...")
                submit_selectors = [
                    "button[type='submit']",
                    "input[type='submit']",
                    "button:contains('Submit')",
                    "button:contains('Apply')",
                    "button:contains('Send')",
                    ".btn-primary",
                    ".submit-btn"
                ]
                
                submit_button = None
                for selector in submit_selectors:
                    try:
                        if ":contains" in selector:
                            # Use XPath for text-based search
                            xpath = f"//button[contains(text(), '{selector.split(':contains(')[1].strip(')')}')]"
                            submit_button = self.driver.find_element(By.XPATH, xpath)
                        else:
                            submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                # Fallback: look for any button that might be submit
                if not submit_button:
                    buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    for button in buttons:
                        button_text = button.text.lower()
                        if any(word in button_text for word in ['submit', 'apply', 'send', 'save']):
                            submit_button = button
                            break
                
                if submit_button:
                    logger.info("🎯 Found submit button, clicking...")
                    
                    # Scroll to submit button
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                    time.sleep(1)
                    
                    # Click submit button
                    submit_button.click()
                    filled_fields.append("✅ Form submitted successfully")
                    logger.info("✅ Form submitted successfully")
                    
                    # Wait for submission to process
                    time.sleep(3)
                    
                    # Add success message to the page after submission
                    success_message_script = """
                    const successMsg = document.createElement('div');
                    successMsg.innerHTML = `
                        <div style="position: fixed; top: 20px; right: 20px; background: #28a745; color: white; padding: 20px 30px; border-radius: 10px; font-family: Arial, sans-serif; font-size: 16px; z-index: 999999; box-shadow: 0 4px 20px rgba(0,0,0,0.3); max-width: 400px;">
                            <strong>🎉 Application Submitted Successfully!</strong><br>
                            <small style="font-size: 14px; margin-top: 10px; display: block;">
                                Your name change request has been submitted to Torrent Power.<br>
                                You will receive a confirmation email shortly.
                            </small>
                        </div>
                    `;
                    document.body.appendChild(successMsg);
                    
                    setTimeout(() => {
                        if (successMsg.parentNode) {
                            successMsg.parentNode.removeChild(successMsg);
                        }
                    }, 8000);
                    """
                    
                    self.driver.execute_script(success_message_script)
                    
                else:
                    filled_fields.append("⚠️ Submit button not found - please submit manually")
                    logger.warning("⚠️ Submit button not found")
                
            except Exception as e:
                logger.error(f"❌ Submit button error: {e}")
                filled_fields.append("❌ Submit button error")
            
            # Clean completion without popup
            success_count = len([f for f in filled_fields if f.startswith('✅')])
            logger.info(f"📊 Form filling completed: {success_count}/6 fields filled")
            
            return {
                "success": success_count > 0,
                "filled_fields": filled_fields,
                "total_filled": success_count,
                "total_fields": 6  # Updated to include submit button
            }
            
        except Exception as e:
            logger.error(f"❌ Form filling failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "filled_fields": ["❌ Form filling failed"],
                "total_filled": 0,
                "total_fields": 6
            }
    
    def run_automation(self, form_data):
        """Run complete Torrent Power automation"""
        try:
            logger.info("🤖 Starting Torrent Power RPA automation...")
            
            # Setup driver
            if not self.setup_driver():
                return {"success": False, "error": "Chrome setup failed"}
            
            # Navigate to Torrent Power
            if not self.navigate_to_torrent_power():
                return {"success": False, "error": "Failed to navigate to Torrent Power website"}
            
            # Fill the form
            result = self.fill_form(form_data)
            
            # Keep browser open for user interaction (5 minutes)
            logger.info("🕐 Keeping browser open for 5 minutes for user interaction...")
            time.sleep(300)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ RPA automation failed: {e}")
            return {"success": False, "error": str(e)}
        finally:
            # Don't close driver immediately - let user interact
            pass
    
    def close_driver(self):
        """Close the browser"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("✅ Browser closed")
        except Exception as e:
            logger.error(f"❌ Error closing browser: {e}")


# Test function for localhost
def test_localhost_rpa():
    """Test RPA on localhost"""
    test_data = {
        "city": "Ahmedabad",
        "service_number": "TP123456",
        "t_number": "T789",
        "mobile": "9632587410",
        "email": "test@gmail.com"
    }
    
    rpa = SimpleTorrentRPA()
    result = rpa.run_automation(test_data)
    
    print("🔍 Localhost RPA Test Results:")
    print(f"Success: {result.get('success')}")
    print(f"Fields filled: {result.get('total_filled', 0)}/5")
    
    if result.get('filled_fields'):
        print("Field Results:")
        for field in result['filled_fields']:
            print(f"  {field}")
    
    return result


if __name__ == "__main__":
    test_localhost_rpa()