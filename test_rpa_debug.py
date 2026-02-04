#!/usr/bin/env python3
"""
RPA Debug Test Script for Windows EC2
Run this script to test RPA functionality step by step
"""

import sys
import os
import logging
import platform
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test if all required packages are available"""
    logger.info("🧪 Testing imports...")
    
    try:
        import selenium
        logger.info(f"✅ Selenium version: {selenium.__version__}")
    except ImportError as e:
        logger.error(f"❌ Selenium import failed: {e}")
        return False
    
    try:
        from selenium import webdriver
        logger.info("✅ WebDriver imported")
    except ImportError as e:
        logger.error(f"❌ WebDriver import failed: {e}")
        return False
    
    try:
        from selenium.webdriver.chrome.options import Options
        logger.info("✅ Chrome Options imported")
    except ImportError as e:
        logger.error(f"❌ Chrome Options import failed: {e}")
        return False
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        logger.info("✅ WebDriver Manager imported")
    except ImportError as e:
        logger.error(f"❌ WebDriver Manager import failed: {e}")
        return False
    
    return True

def test_chrome_installation():
    """Test Chrome browser installation"""
    logger.info("🧪 Testing Chrome installation...")
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe"
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if os.path.exists(path):
            logger.info(f"✅ Chrome found at: {path}")
            chrome_found = True
            
            # Try to get version
            try:
                import subprocess
                result = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    logger.info(f"✅ Chrome version: {result.stdout.strip()}")
            except Exception as e:
                logger.warning(f"⚠️ Could not get Chrome version: {e}")
            
            break
    
    if not chrome_found:
        logger.error("❌ Chrome not found in standard locations")
        logger.error("💡 Install Chrome: choco install googlechrome -y --ignore-checksums")
        return False
    
    return True

def test_chromedriver_setup():
    """Test ChromeDriver setup"""
    logger.info("🧪 Testing ChromeDriver setup...")
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        
        logger.info("📥 Downloading/locating ChromeDriver...")
        driver_path = ChromeDriverManager().install()
        logger.info(f"✅ ChromeDriver path: {driver_path}")
        
        if os.path.exists(driver_path):
            logger.info("✅ ChromeDriver file exists")
            return driver_path
        else:
            logger.error(f"❌ ChromeDriver file not found at: {driver_path}")
            return None
            
    except Exception as e:
        logger.error(f"❌ ChromeDriver setup failed: {e}")
        return None

def test_basic_webdriver():
    """Test basic WebDriver functionality"""
    logger.info("🧪 Testing basic WebDriver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        
        # Setup Chrome options
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        # Find Chrome binary
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                options.binary_location = path
                logger.info(f"✅ Using Chrome binary: {path}")
                break
        
        # Try to create driver
        logger.info("🚀 Creating Chrome driver...")
        
        # Method 1: Try with webdriver-manager
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            driver_path = ChromeDriverManager().install()
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            logger.info("✅ Driver created with webdriver-manager")
        except Exception as e:
            logger.warning(f"⚠️ webdriver-manager failed: {e}")
            # Method 2: Try system driver
            driver = webdriver.Chrome(options=options)
            logger.info("✅ Driver created with system Chrome")
        
        # Test basic functionality
        logger.info("🧪 Testing basic navigation...")
        test_html = """
        <html>
        <head><title>RPA Test</title></head>
        <body>
            <h1>RPA Test Page</h1>
            <input type="text" id="test-input" placeholder="Test input">
            <button id="test-button">Test Button</button>
        </body>
        </html>
        """
        
        driver.get(f"data:text/html,{test_html}")
        logger.info(f"✅ Page loaded, title: {driver.title}")
        
        # Test element interaction
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(driver, 10)
        
        # Find input element
        input_element = wait.until(EC.presence_of_element_located((By.ID, "test-input")))
        input_element.send_keys("Test successful!")
        logger.info("✅ Input element interaction successful")
        
        # Find button element
        button_element = driver.find_element(By.ID, "test-button")
        button_element.click()
        logger.info("✅ Button click successful")
        
        # Keep browser open for 5 seconds
        logger.info("⏳ Keeping browser open for 5 seconds...")
        time.sleep(5)
        
        # Close driver
        driver.quit()
        logger.info("✅ Driver closed successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ WebDriver test failed: {e}")
        logger.error(f"❌ Error type: {type(e).__name__}")
        return False

def test_torrent_power_navigation():
    """Test navigation to Torrent Power website"""
    logger.info("🧪 Testing Torrent Power navigation...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Setup Chrome options
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        # Find Chrome binary
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                options.binary_location = path
                break
        
        # Create driver
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            driver_path = ChromeDriverManager().install()
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
        except:
            driver = webdriver.Chrome(options=options)
        
        # Set timeouts
        driver.set_page_load_timeout(60)
        wait = WebDriverWait(driver, 30)
        
        # Navigate to Torrent Power
        url = "https://connect.torrentpower.com/tplcp/application/namechangerequest"
        logger.info(f"🌐 Navigating to: {url}")
        
        driver.get(url)
        
        # Wait for page to load
        logger.info("⏳ Waiting for page to load...")
        time.sleep(5)
        
        # Check current URL
        current_url = driver.current_url
        logger.info(f"🔍 Current URL: {current_url}")
        
        # Check page title
        page_title = driver.title
        logger.info(f"🔍 Page title: {page_title}")
        
        # Try to find some elements
        try:
            body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            logger.info("✅ Body element found")
        except:
            logger.warning("⚠️ Body element not found")
        
        # Look for form elements
        try:
            forms = driver.find_elements(By.TAG_NAME, "form")
            logger.info(f"✅ Found {len(forms)} form(s)")
        except:
            logger.warning("⚠️ No forms found")
        
        # Look for input elements
        try:
            inputs = driver.find_elements(By.TAG_NAME, "input")
            logger.info(f"✅ Found {len(inputs)} input(s)")
        except:
            logger.warning("⚠️ No inputs found")
        
        # Keep browser open for inspection
        logger.info("⏳ Keeping browser open for 30 seconds for inspection...")
        time.sleep(30)
        
        # Close driver
        driver.quit()
        logger.info("✅ Navigation test completed")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Navigation test failed: {e}")
        logger.error(f"❌ Error type: {type(e).__name__}")
        return False

def main():
    """Run all tests"""
    logger.info("🚀 Starting RPA Debug Tests for Windows EC2")
    logger.info("=" * 50)
    
    # System info
    logger.info(f"🔍 Platform: {platform.system()} {platform.release()}")
    logger.info(f"🔍 Python: {platform.python_version()}")
    logger.info(f"🔍 Node: {platform.node()}")
    
    tests = [
        ("Import Test", test_imports),
        ("Chrome Installation Test", test_chrome_installation),
        ("ChromeDriver Setup Test", test_chromedriver_setup),
        ("Basic WebDriver Test", test_basic_webdriver),
        ("Torrent Power Navigation Test", test_torrent_power_navigation)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results[test_name] = result
            if result:
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} CRASHED: {e}")
            results[test_name] = False
    
    # Summary
    logger.info(f"\n{'='*20} SUMMARY {'='*20}")
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {test_name}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! RPA should work.")
    else:
        logger.error("❌ Some tests failed. Check the logs above for details.")
        logger.error("💡 Common fixes:")
        logger.error("   - Install Chrome: choco install googlechrome -y --ignore-checksums")
        logger.error("   - Install Python packages: pip install selenium webdriver-manager requests")
        logger.error("   - Run as Administrator")
        logger.error("   - Check Windows Firewall settings")

if __name__ == "__main__":
    main()