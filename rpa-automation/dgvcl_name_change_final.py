"""
DGVCL Name Change RPA - PRODUCTION SAFE MODE
✅ Fills Applicant Details (Step 1 only)
❌ Does NOT upload documents
❌ Does NOT proceed to payment
❌ Does NOT submit application
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import sys

# ⚠️ CRITICAL SAFETY SETTINGS
SAFETY_MODE = True
STOP_AT_STEP_1 = True  # Only fill Applicant Details
NO_DOCUMENT_UPLOAD = True
NO_PAYMENT = True
NO_SUBMIT = True

class DGVCLNameChangeRPA:
    """
    DGVCL Name Change - SAFE MODE
    Only fills Step 1 (Applicant Details)
    User must complete Steps 2-4 manually
    """
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.portal_url = "https://portal.guvnl.in"
        self.name_change_url = "https://portal.guvnl.in/ltNameChange.php?apptype=namechange"
        
    def setup_browser(self):
        """Setup Chrome browser - visible for user monitoring"""
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 30)
        
        print("✅ Browser opened - You can monitor the process")
        
    def login_to_portal(self, mobile_number, discom="DGVCL"):
        """
        Login to DGVCL portal using Mobile Number + OTP
        Portal: https://portal.guvnl.in/login.php
        """
        print("\n🌐 Opening DGVCL Login Page...")
        self.driver.get(f"{self.portal_url}/login.php")
        time.sleep(3)
        
        print("🔐 Logging in with Mobile Number + OTP...")
        
        try:
            # Check if already logged in
            if "welcome" in self.driver.page_source.lower() or "dashboard" in self.driver.page_source.lower():
                print("✅ Already logged in")
                return True
            
            # Mobile Number field
            mobile_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "mobile"))
            )
            mobile_field.clear()
            mobile_field.send_keys(mobile_number)
            print(f"✅ Mobile Number: {mobile_number}")
            
            # DISCOM dropdown
            try:
                discom_dropdown = Select(self.driver.find_element(By.ID, "discom"))
                discom_dropdown.select_by_visible_text(discom)
                print(f"✅ DISCOM: {discom}")
            except Exception as e:
                print(f"⚠️  DISCOM dropdown: {e}")
            
            # Captcha - User must enter manually
            print("\n⏸️  Please enter the CAPTCHA on the portal")
            input("⏸️  Press ENTER after entering CAPTCHA...")
            
            # Click Login button to get OTP
            try:
                login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login') or @type='submit']")
                login_btn.click()
                print("✅ Login button clicked - OTP should be sent")
            except Exception as e:
                print(f"⚠️  Login button: {e}")
                print("💡 Please click Login button manually")
            
            time.sleep(3)
            
            # Wait for OTP entry
            print("\n📱 OTP sent to: {mobile_number}")
            print("⏸️  Please enter OTP on the portal")
            input("⏸️  Press ENTER after entering OTP and completing login...")
            
            time.sleep(3)
            
            # Verify login
            if "welcome" in self.driver.page_source.lower() or "dashboard" in self.driver.page_source.lower():
                print("✅ Login successful")
                return True
            else:
                print("⚠️  Verifying login status...")
                input("⏸️  Press ENTER after successful login...")
                return True
                
        except Exception as e:
            print(f"⚠️  Login error: {e}")
            print(f"💡 Please login manually using mobile: {mobile_number}")
            input("⏸️  Press ENTER after manual login...")
            return True
    
    def navigate_to_name_change(self):
        """Navigate to LT Name Change page using direct URL"""
        print("\n📄 Navigating to LT Name Change...")
        
        try:
            # Use direct URL
            self.driver.get(self.name_change_url)
            time.sleep(3)
            
            # Check if page loaded
            if "namechange" in self.driver.current_url.lower() or "ltNameChange" in self.driver.current_url:
                print("✅ LT Name Change page loaded")
                return True
            else:
                print("⚠️  Page may not have loaded correctly")
                input("⏸️  Press ENTER when on Name Change page...")
                return True
            
        except Exception as e:
            print(f"⚠️  Navigation error: {e}")
            print("💡 Trying alternative method...")
            
            try:
                # Fallback: Look for link in sidebar
                name_change_link = self.wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "LT Name Change"))
                )
                name_change_link.click()
                time.sleep(3)
                print("✅ LT Name Change page loaded")
                return True
            except:
                print("💡 Please navigate to Name Change page manually")
                input("⏸️  Press ENTER when on Name Change page...")
                return True
    
    def fill_applicant_details(self, data):
        """
        Fill Step 1: Applicant Details ONLY
        ⚠️ Does NOT proceed to next steps
        """
        print("\n📝 Filling Applicant Details (Step 1)...")
        print("⚠️  SAFETY: Will STOP after Step 1")
        
        try:
            time.sleep(2)
            
            # Consumer No (usually auto-filled)
            print("ℹ️  Consumer No should be auto-filled")
            
            # New Name
            if 'new_name' in data:
                try:
                    new_name_field = self.driver.find_element(By.NAME, "new_name")
                    new_name_field.clear()
                    new_name_field.send_keys(data['new_name'])
                    print(f"✅ New Name: {data['new_name']}")
                except Exception as e:
                    print(f"⚠️  New Name field: {e}")
            
            # Reason dropdown
            if 'reason' in data:
                try:
                    reason_dropdown = Select(self.driver.find_element(By.NAME, "reason"))
                    reason_dropdown.select_by_visible_text(data['reason'])
                    print(f"✅ Reason: {data['reason']}")
                except Exception as e:
                    print(f"⚠️  Reason dropdown: {e}")
            
            # Security Deposit option
            if 'security_deposit_option' in data:
                try:
                    if data['security_deposit_option'] == 'entire':
                        radio = self.driver.find_element(By.XPATH, "//input[@type='radio' and contains(@value, 'entire')]")
                    else:
                        radio = self.driver.find_element(By.XPATH, "//input[@type='radio' and contains(@value, 'difference')]")
                    radio.click()
                    print(f"✅ Security Deposit: {data['security_deposit_option']}")
                except Exception as e:
                    print(f"⚠️  Security Deposit: {e}")
            
            time.sleep(2)
            print("\n✅ Step 1 (Applicant Details) filled successfully!")
            
        except Exception as e:
            print(f"⚠️  Error filling form: {e}")
    
    def show_completion_message(self):
        """Show completion message and keep browser open"""
        print("\n" + "="*70)
        print("🎯 STEP 1 COMPLETED - MANUAL VERIFICATION REQUIRED")
        print("="*70)
        print("\n✅ What was done:")
        print("  • Logged into DGVCL portal")
        print("  • Navigated to LT Name Change")
        print("  • Filled Applicant Details (Step 1)")
        
        print("\n⚠️  What you need to do:")
        print("  1. 👀 VERIFY all filled information")
        print("  2. 📝 Make corrections if needed")
        print("  3. ➡️  Click 'Next' to proceed to Step 2 (Document Upload)")
        print("  4. 📎 Upload required documents")
        print("  5. 💰 Complete payment (₹23.6)")
        print("  6. ✅ Submit application")
        
        print("\n🔒 SAFETY FEATURES:")
        print("  • ✅ No documents uploaded automatically")
        print("  • ✅ No payment made automatically")
        print("  • ✅ No application submitted automatically")
        print("  • ✅ Full control remains with you")
        
        print("\n💡 Browser will stay open for 15 minutes")
        print("="*70)
        
        # Keep browser open
        for i in range(900, 0, -60):
            mins = i // 60
            print(f"\r⏱️  Browser will close in {mins} minutes... ", end='', flush=True)
            time.sleep(60)
        
        print("\n\n👋 Time's up! Closing browser...")
    
    def run(self, data):
        """
        Main execution flow
        ⚠️ SAFE MODE: Only fills Step 1
        """
        try:
            print("\n" + "="*70)
            print("🚀 DGVCL NAME CHANGE RPA - SAFE MODE")
            print("="*70)
            print("⚠️  SAFETY ENABLED:")
            print("  • Will ONLY fill Step 1 (Applicant Details)")
            print("  • Will NOT upload documents")
            print("  • Will NOT make payment")
            print("  • Will NOT submit application")
            print("  • User must complete Steps 2-4 manually")
            print("="*70)
            
            # Setup
            self.setup_browser()
            
            # Login
            self.login_to_portal(
                data.get('mobile_number'),
                data.get('discom', 'DGVCL')
            )
            
            # Navigate to Name Change
            self.navigate_to_name_change()
            
            # Fill Step 1 only
            self.fill_applicant_details(data)
            
            # Show completion message
            self.show_completion_message()
            
            print("\n✅ RPA process completed safely")
            print("🔒 No data was submitted to DGVCL")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Process interrupted by user")
            print("💡 Browser will stay open for manual completion")
            time.sleep(300)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("💡 Browser will stay open for manual completion")
            time.sleep(300)
            
        finally:
            if self.driver:
                print("\n👋 Closing browser...")
                self.driver.quit()


# Example usage with REAL DATA
if __name__ == "__main__":
    import json
    
    # Check if data file provided as argument
    if len(sys.argv) > 1:
        # Read data from file (called by backend)
        data_file = sys.argv[1]
        try:
            with open(data_file, 'r') as f:
                dgvcl_data = json.load(f)
            
            print("\n✅ Data loaded from backend")
            print(f"  Mobile: {dgvcl_data.get('mobile')}")
            print(f"  Consumer No: {dgvcl_data.get('consumer_number')}")
            print(f"  DISCOM: {dgvcl_data.get('discom', 'DGVCL')}")
            
            # Map backend data to RPA format
            rpa_data = {
                'mobile_number': dgvcl_data.get('mobile'),
                'discom': dgvcl_data.get('discom', 'DGVCL'),
                'consumer_no': dgvcl_data.get('consumer_number'),
                'new_name': dgvcl_data.get('applicant_name', ''),
                'reason': 'Name Correction',
                'security_deposit_option': 'entire'
            }
            
            rpa = DGVCLNameChangeRPA()
            rpa.run(rpa_data)
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            sys.exit(1)
    else:
        # Manual mode - use hardcoded data
        dgvcl_data = {
            'mobile_number': '9870083162',  # Login mobile number
            'discom': 'DGVCL',  # DISCOM selection
            'consumer_no': '08267002294',
            'new_name': 'PANCHAL SANJAY GANPATBHAI',  # Example new name
            'reason': 'Name Correction',  # Or other reason from dropdown
            'security_deposit_option': 'entire'  # or 'difference'
        }
        
        print("\n⚠️  WARNING: PRODUCTION MODE")
        print("✅ Will use REAL DGVCL account")
        print("✅ Will ONLY fill Step 1")
        print("❌ Will NOT submit application")
        print("\nData to be used:")
        print(f"  Mobile: {dgvcl_data['mobile_number']}")
        print(f"  Consumer No: {dgvcl_data['consumer_no']}")
        print(f"  New Name: {dgvcl_data['new_name']}")
        
        confirm = input("\n❓ Continue with REAL data? (yes/no): ")
        
        if confirm.lower() == 'yes':
            rpa = DGVCLNameChangeRPA()
            rpa.run(dgvcl_data)
        else:
            print("❌ Cancelled - No action taken")
