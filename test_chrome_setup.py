"""
Quick test to verify Chrome and ChromeDriver setup
"""

import os
import sys

def test_chrome_installation():
    """Test if Chrome is installed"""
    print("🔍 Testing Chrome installation...")
    
    chrome_paths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe")
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome found at: {path}")
            chrome_found = True
            break
    
    if not chrome_found:
        print("❌ Chrome not found! Please install Google Chrome.")
        return False
    
    return True

def test_selenium():
    """Test if Selenium is installed"""
    print("\n🔍 Testing Selenium installation...")
    
    try:
        import selenium
        print(f"✅ Selenium installed: version {selenium.__version__}")
        return True
    except ImportError:
        print("❌ Selenium not installed!")
        return False

def test_webdriver_manager():
    """Test if webdriver-manager is installed"""
    print("\n🔍 Testing webdriver-manager installation...")
    
    try:
        import webdriver_manager
        print(f"✅ webdriver-manager installed")
        return True
    except ImportError:
        print("❌ webdriver-manager not installed!")
        return False

def test_chrome_driver():
    """Test if ChromeDriver can be initialized"""
    print("\n🔍 Testing ChromeDriver initialization...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        print("📦 Downloading/locating ChromeDriver...")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Set Chrome binary path
        chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe")
        ]
        
        for chrome_path in chrome_paths:
            if os.path.exists(chrome_path):
                chrome_options.binary_location = chrome_path
                break
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ ChromeDriver initialized successfully!")
        
        # Test navigation
        print("🧪 Testing navigation...")
        driver.get("data:text/html,<html><body><h1>Test</h1></body></html>")
        print("✅ Navigation test successful!")
        
        driver.quit()
        print("✅ Driver closed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ ChromeDriver test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 Chrome & ChromeDriver Setup Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Chrome Installation", test_chrome_installation()))
    results.append(("Selenium", test_selenium()))
    results.append(("webdriver-manager", test_webdriver_manager()))
    results.append(("ChromeDriver", test_chrome_driver()))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! Chrome automation is ready to use.")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
