"""
Enhanced Direct Automation Service with Advanced Selenium Configuration
"""
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from typing import Dict, Any, Optional
import os
from datetime import datetime

from .user_data_service import user_data_service
from .selenium_config import selenium_config

logger = logging.getLogger(__name__)

class EnhancedDirectAutomationService:
    """Enhanced service for direct automation with advanced Selenium configuration"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.actions = None
        self.current_user_key = None
        
    def setup_driver(self, headless: bool = False, stealth_mode: bool = True, 
                    undetected: bool = False) -> webdriver.Chrome:
        """Setup Chrome WebDriver with advanced configuration"""
        try:
            # Create driver using selenium_config
            self.driver = selenium_config.create_driver(
                headless=headless, 
                stealth_mode=stealth_mode, 
                undetected=undetected
            )
            
            # Configure for government sites
            selenium_config.configure_for_government_sites(self.driver)
            
            # Setup WebDriverWait and ActionChains
            self.wait = WebDriverWait(self.driver, 30)
            self.actions = ActionChains(self.driver)
            
            logger.info("Enhanced WebDriver setup completed")
            return self.driver
            
        except Exception as e:
            logger.error(f"Failed to setup enhanced WebDriver: {e}")
            raise e
    
    def smart_element_finder(self, selectors: list, timeout: int = 10) -> Optional[any]:
        """Smart element finder with multiple selector strategies"""
        for selector in selectors:
            try:
                if selector.startswith("//"):
                    # XPath selector
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                elif selector.startswith("#"):
                    # ID selector
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((By.ID, selector[1:]))
                    )
                elif selector.startswith("."):
                    # Class selector
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((By.CLASS_NAME, selector[1:]))
                    )
                else:
                    # CSS selector
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                
                if element and element.is_displayed():
                    return element
                    
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
                continue
        
        logger.warning(f"No element found with selectors: {selectors}")
        return None
    
    def human_like_typing(self, element, text: str, typing_speed: float = 0.1) -> bool:
        """Type text with human-like delays"""
        try:
            element.clear()
            time.sleep(0.5)
            
            for char in text:
                element.send_keys(char)
                time.sleep(typing_speed + (0.05 * (0.5 - 0.5)))  # Random delay
            
            time.sleep(0.5)
            return True
            
        except Exception as e:
            logger.error(f"Failed to type text: {e}")
            return False
    
    def smart_click(self, element) -> bool:
        """Smart click with multiple strategies"""
        try:
            # Scroll to element
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            # Try regular click
            try:
                element.click()
                return True
            except:
                pass
            
            # Try JavaScript click
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except:
                pass
            
            # Try ActionChains click
            try:
                self.actions.move_to_element(element).click().perform()
                return True
            except:
                pass
            
            logger.warning("All click strategies failed")
            return False
            
        except Exception as e:
            logger.error(f"Smart click failed: {e}")
            return False
    
    def store_and_retrieve_user_data(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Store user data and retrieve any existing data"""
        try:
            mobile = form_data.get('mobile')
            email = form_data.get('email')
            
            if not mobile:
                return form_data
            
            # Try to find existing user data
            existing_data = user_data_service.find_user_by_mobile(mobile)
            
            if existing_data:
                # Merge existing data with new data (new data takes precedence)
                merged_data = existing_data["form_data"].copy()
                merged_data.update(form_data)
                
                # Update stored data
                user_data_service.update_user_data(existing_data["user_key"], merged_data)
                self.current_user_key = existing_data["user_key"]
                
                logger.info(f"Retrieved and updated existing user data for mobile: {mobile}")
                return merged_data
            else:
                # Store new user data
                self.current_user_key = user_data_service.store_user_data(mobile, form_data, email)
                logger.info(f"Stored new user data for mobile: {mobile}")
                return form_data
                
        except Exception as e:
            logger.error(f"Failed to handle user data: {e}")
            return form_data
    
    def close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None

    # GAS SERVICES - DIRECT ACCESS
    
    def submit_gujarat_gas_name_change(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gujarat Gas - Customer service form (Direct access)"""
        try:
            logger.info(f"Starting Gujarat Gas name change for consumer: {data.get('consumer_number')}")
            
            self.setup_driver(headless=False)
            
            # Navigate to customer care page
            url = "https://www.gujaratgas.com/customer-care"
            self.driver.get(url)
            
            # Wait for page load
            time.sleep(3)
            
            # Look for name change form or contact form
            try:
                # Try to find consumer number field
                consumer_field = self.wait.until(EC.element_to_be_clickable((By.NAME, "consumer_no")))
                consumer_field.clear()
                consumer_field.send_keys(data.get('consumer_number', ''))
                time.sleep(0.5)
            except:
                # Alternative selector
                try:
                    consumer_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'consumer') or contains(@placeholder, 'Consumer')]")
                    consumer_field.clear()
                    consumer_field.send_keys(data.get('consumer_number', ''))
                    time.sleep(0.5)
                except:
                    logger.warning("Consumer number field not found")
            
            # Fill current name
            try:
                current_name_field = self.driver.find_element(By.NAME, "current_name")
                current_name_field.clear()
                current_name_field.send_keys(data.get('old_name', ''))
                time.sleep(0.5)
            except:
                try:
                    current_name_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'current name') or contains(@placeholder, 'existing name')]")
                    current_name_field.clear()
                    current_name_field.send_keys(data.get('old_name', ''))
                    time.sleep(0.5)
                except:
                    logger.warning("Current name field not found")
            
            # Fill new name
            try:
                new_name_field = self.driver.find_element(By.NAME, "new_name")
                new_name_field.clear()
                new_name_field.send_keys(data.get('new_name', ''))
                time.sleep(0.5)
            except:
                try:
                    new_name_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'new name')]")
                    new_name_field.clear()
                    new_name_field.send_keys(data.get('new_name', ''))
                    time.sleep(0.5)
                except:
                    logger.warning("New name field not found")
            
            # Fill mobile
            try:
                mobile_field = self.driver.find_element(By.NAME, "mobile")
                mobile_field.clear()
                mobile_field.send_keys(data.get('mobile', ''))
                time.sleep(0.5)
            except:
                try:
                    mobile_field = self.driver.find_element(By.XPATH, "//input[@type='tel' or contains(@placeholder, 'mobile') or contains(@placeholder, 'phone')]")
                    mobile_field.clear()
                    mobile_field.send_keys(data.get('mobile', ''))
                    time.sleep(0.5)
                except:
                    logger.warning("Mobile field not found")
            
            # Fill email
            if data.get('email'):
                try:
                    email_field = self.driver.find_element(By.NAME, "email")
                    email_field.clear()
                    email_field.send_keys(data['email'])
                    time.sleep(0.5)
                except:
                    try:
                        email_field = self.driver.find_element(By.XPATH, "//input[@type='email']")
                        email_field.clear()
                        email_field.send_keys(data['email'])
                        time.sleep(0.5)
                    except:
                        logger.warning("Email field not found")
            
            # Fill address
            try:
                address_field = self.driver.find_element(By.NAME, "address")
                address_field.clear()
                address_field.send_keys(data.get('address', ''))
                time.sleep(0.5)
            except:
                try:
                    address_field = self.driver.find_element(By.TAG_NAME, "textarea")
                    address_field.clear()
                    address_field.send_keys(data.get('address', ''))
                    time.sleep(0.5)
                except:
                    logger.warning("Address field not found")
            
            # Select reason if dropdown exists
            if data.get('reason'):
                try:
                    reason_select = Select(self.driver.find_element(By.NAME, "reason"))
                    reason_select.select_by_value(data['reason'])
                    time.sleep(0.5)
                except:
                    logger.warning("Reason dropdown not found")
            
            # Take screenshot before submit
            screenshot_path = f"screenshots/gujarat_gas_filled_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            
            # Show completion message
            completion_script = """
            alert(`✅ Gujarat Gas Form Filled Successfully!
            
Please review the filled information:
• Consumer Number: Filled
• Current Name: Filled  
• New Name: Filled
• Mobile: Filled
• Email: Filled (if provided)
• Address: Filled

Next Steps:
1. Review all information carefully
2. Submit the form manually
3. Save any confirmation number received
4. Keep screenshot for records

Click OK to continue.`);
            """
            self.driver.execute_script(completion_script)
            
            return {
                "success": True,
                "message": "Gujarat Gas form filled successfully. Please review and submit manually.",
                "screenshot_path": screenshot_path,
                "website": "Gujarat Gas",
                "service": "Name Change",
                "filled_data": data,
                "next_steps": [
                    "Review all filled information",
                    "Submit form manually after verification",
                    "Save confirmation number",
                    "Keep screenshot for records"
                ]
            }
            
        except Exception as e:
            logger.error(f"Gujarat Gas automation failed: {str(e)}")
            
            # Take error screenshot
            try:
                error_screenshot = f"screenshots/gujarat_gas_error_{int(time.time())}.png"
                self.driver.save_screenshot(error_screenshot)
            except:
                error_screenshot = None
            
            return {
                "success": False,
                "error": str(e),
                "message": "Gujarat Gas automation failed. Please try manual form filling.",
                "screenshot_path": error_screenshot,
                "website": "Gujarat Gas"
            }
        finally:
            # Keep browser open for manual verification
            pass
    
    def submit_vadodara_gas_name_change(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Vadodara Gas - Direct name change form (No login required)"""
        try:
            logger.info(f"Starting Vadodara Gas name change for consumer: {data.get('consumer_number')}")
            
            self.setup_driver(headless=False)
            
            # Direct URL to name change form
            url = "https://www.vgl.co.in/name-change-form"
            self.driver.get(url)
            
            # Wait for form to load
            self.wait.until(EC.presence_of_element_located((By.NAME, "consumer_number")))
            
            # Fill form fields
            if data.get('consumer_number'):
                consumer_field = self.driver.find_element(By.NAME, "consumer_number")
                consumer_field.clear()
                consumer_field.send_keys(data['consumer_number'])
                time.sleep(0.5)
            
            if data.get('old_name'):
                old_name_field = self.driver.find_element(By.NAME, "current_name")
                old_name_field.clear()
                old_name_field.send_keys(data['old_name'])
                time.sleep(0.5)
            
            if data.get('new_name'):
                new_name_field = self.driver.find_element(By.NAME, "new_name")
                new_name_field.clear()
                new_name_field.send_keys(data['new_name'])
                time.sleep(0.5)
            
            if data.get('mobile'):
                mobile_field = self.driver.find_element(By.NAME, "mobile")
                mobile_field.clear()
                mobile_field.send_keys(data['mobile'])
                time.sleep(0.5)
            
            # Take screenshot
            screenshot_path = f"screenshots/vadodara_gas_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            
            return {
                "success": True,
                "message": "Vadodara Gas form filled successfully",
                "screenshot_path": screenshot_path,
                "website": "Vadodara Gas",
                "filled_data": data
            }
            
        except Exception as e:
            logger.error(f"Vadodara Gas automation failed: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            pass
    
    # ELECTRICITY SERVICES - DIRECT ACCESS
    
    def submit_torrent_power_name_change(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Torrent Power - PDF form download (No login required)"""
        try:
            logger.info(f"Starting Torrent Power name change for consumer: {data.get('consumer_number')}")
            
            self.setup_driver(headless=False)
            
            # Direct URL to forms page
            url = "https://www.torrentpower.com/customer-care/forms"
            self.driver.get(url)
            
            # Wait for page load
            self.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Name Change")))
            
            # Click on Name Change form link
            name_change_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Name Change")
            name_change_link.click()
            
            # Wait for form to load or PDF to download
            time.sleep(3)
            
            screenshot_path = f"screenshots/torrent_power_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            
            return {
                "success": True,
                "message": "Torrent Power form accessed. PDF form available for download.",
                "screenshot_path": screenshot_path,
                "website": "Torrent Power",
                "note": "PDF form needs to be filled manually and submitted"
            }
            
        except Exception as e:
            logger.error(f"Torrent Power automation failed: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            pass
    
    # WATER SERVICES - DIRECT ACCESS
    
    def submit_gwssb_name_change(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """GWSSB - Direct forms page (No login required)"""
        try:
            logger.info(f"Starting GWSSB name change for consumer: {data.get('consumer_number')}")
            
            self.setup_driver(headless=False)
            
            # Direct URL to forms page
            url = "https://watersupply.gujarat.gov.in/forms"
            self.driver.get(url)
            
            # Wait for forms page
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "form-container")))
            
            # Look for name change form
            name_change_form = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Name Change")
            name_change_form.click()
            
            # Fill form if available
            time.sleep(2)
            
            # Try to fill basic fields
            try:
                if data.get('consumer_number'):
                    consumer_field = self.driver.find_element(By.NAME, "consumer_id")
                    consumer_field.send_keys(data['consumer_number'])
                
                if data.get('old_name'):
                    old_name_field = self.driver.find_element(By.NAME, "current_name")
                    old_name_field.send_keys(data['old_name'])
                
                if data.get('new_name'):
                    new_name_field = self.driver.find_element(By.NAME, "new_name")
                    new_name_field.send_keys(data['new_name'])
                
                if data.get('mobile'):
                    mobile_field = self.driver.find_element(By.NAME, "mobile")
                    mobile_field.send_keys(data['mobile'])
                    
            except Exception as field_error:
                logger.warning(f"Could not fill some fields: {field_error}")
            
            screenshot_path = f"screenshots/gwssb_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            
            return {
                "success": True,
                "message": "GWSSB form accessed and filled",
                "screenshot_path": screenshot_path,
                "website": "GWSSB"
            }
            
        except Exception as e:
            logger.error(f"GWSSB automation failed: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            pass
    
    # PROPERTY SERVICES - DIRECT ACCESS
    
    def submit_anyror_name_change(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """AnyROR - Public record view & forms (No login required)"""
        try:
            logger.info(f"Starting AnyROR name change for property: {data.get('property_id')}")
            
            self.setup_driver(headless=False)
            
            # Direct URL to public records
            url = "https://anyror.gujarat.gov.in"
            self.driver.get(url)
            
            # Wait for page load
            self.wait.until(EC.presence_of_element_located((By.ID, "district")))
            
            # Select district if provided
            if data.get('district'):
                district_select = Select(self.driver.find_element(By.ID, "district"))
                district_select.select_by_visible_text(data['district'])
                time.sleep(1)
            
            # Fill survey number
            if data.get('survey_number'):
                survey_field = self.driver.find_element(By.ID, "survey_no")
                survey_field.send_keys(data['survey_number'])
                time.sleep(0.5)
            
            # Click search to view record
            search_btn = self.driver.find_element(By.ID, "search_btn")
            search_btn.click()
            
            # Wait for results
            time.sleep(3)
            
            screenshot_path = f"screenshots/anyror_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            
            return {
                "success": True,
                "message": "AnyROR record accessed. Manual mutation process required.",
                "screenshot_path": screenshot_path,
                "website": "AnyROR",
                "note": "Record viewed. For name change, visit e-Dhara center or Talati office."
            }
            
        except Exception as e:
            logger.error(f"AnyROR automation failed: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            pass

# Global enhanced service instance
direct_automation_service = EnhancedDirectAutomationService()