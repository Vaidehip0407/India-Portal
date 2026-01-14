// DGVCL Complete Auto-Fill Extension
console.log('🚀 DGVCL Auto-Fill Extension Started');

// Wait for page to load
window.addEventListener('load', function() {
  console.log('📄 Page loaded:', window.location.href);
  
  // Check if we're on DGVCL portal
  if (window.location.hostname === 'portal.guvnl.in') {
    
    // Detect which page we're on
    const url = window.location.href;
    
    // PAGE 1: Login Page (login.php)
    if (url.includes('login.php')) {
      console.log('📍 On Login Page');
      handleLoginPage();
    }
    
    // PAGE 2: OTP Page (checkOtp.php)
    else if (url.includes('checkOtp.php')) {
      console.log('📍 On OTP Page');
      handleOTPPage();
    }
    
    // PAGE 3: Select User Page (Submit_Otp.php)
    else if (url.includes('Submit_Otp.php')) {
      console.log('📍 On Select User Page');
      handleSelectUserPage();
    }
    
    // PAGE 4: Dashboard (prtlDashboard.php)
    else if (url.includes('prtlDashboard.php')) {
      console.log('📍 On Dashboard - SUCCESS!');
      showNotification('✅ Login Successful! Welcome to DGVCL Dashboard');
    }
  }
});

// PAGE 1: Login Page Handler
function handleLoginPage() {
  const urlParams = new URLSearchParams(window.location.search);
  const mobile = urlParams.get('mobile');
  const discom = urlParams.get('discom');
  
  console.log('📦 URL Data:', { mobile, discom });
  
  if (mobile && discom) {
    setTimeout(function() {
      // Fill Mobile No
      const mobileField = document.querySelector('input[placeholder="Mobile No"]') ||
                         document.querySelector('input[placeholder*="Mobile"]');
      
      if (mobileField) {
        mobileField.value = mobile;
        mobileField.dispatchEvent(new Event('input', { bubbles: true }));
        mobileField.dispatchEvent(new Event('change', { bubbles: true }));
        mobileField.style.backgroundColor = '#90EE90';
        console.log('✅ Filled Mobile No:', mobile);
      }
      
      // Fill DISCOM dropdown
      const discomDropdown = document.querySelector('select');
      if (discomDropdown) {
        const options = discomDropdown.options;
        for (let i = 0; i < options.length; i++) {
          if (options[i].text.includes(discom) || options[i].value.includes(discom)) {
            discomDropdown.selectedIndex = i;
            discomDropdown.dispatchEvent(new Event('change', { bubbles: true }));
            discomDropdown.style.backgroundColor = '#90EE90';
            console.log('✅ Selected DISCOM:', discom);
            break;
          }
        }
      }
      
      showNotification('✅ Auto-filled! Enter Captcha & Click Login');
      
    }, 2000);
  }
}

// PAGE 2: OTP Page Handler
function handleOTPPage() {
  console.log('📍 OTP Page - Waiting for user to enter OTP...');
  showNotification('📱 Enter OTP and click Submit Otp');
  
  // Don't auto-click - user needs to enter OTP first
  // Just show helpful message
}

// PAGE 3: Select User Page Handler
function handleSelectUserPage() {
  console.log('📍 Select User Page - Auto-clicking Submit...');
  
  setTimeout(function() {
    // Find and click Submit button
    const submitBtn = document.querySelector('input[type="submit"]') ||
                     document.querySelector('button[type="submit"]') ||
                     document.querySelector('input[value="Submit"]');
    
    if (submitBtn) {
      console.log('✅ Found Submit button, clicking...');
      showNotification('🔄 Auto-submitting...');
      submitBtn.click();
    } else {
      console.log('❌ Submit button not found');
      // Try to find any button with "Submit" text
      const allButtons = document.querySelectorAll('input, button');
      allButtons.forEach(function(btn) {
        if (btn.value === 'Submit' || btn.textContent === 'Submit') {
          console.log('✅ Found Submit button (alternative), clicking...');
          btn.click();
        }
      });
    }
  }, 1500);
}

// Show notification
function showNotification(message) {
  // Remove existing notification
  const existing = document.getElementById('dgvcl-notification');
  if (existing) existing.remove();
  
  const notification = document.createElement('div');
  notification.id = 'dgvcl-notification';
  notification.style.cssText = 'position:fixed;top:20px;right:20px;background:#4CAF50;color:white;padding:15px 25px;border-radius:10px;font-size:16px;z-index:999999;box-shadow:0 4px 20px rgba(0,0,0,0.3);';
  notification.textContent = message;
  document.body.appendChild(notification);
  
  setTimeout(function() {
    notification.remove();
  }, 5000);
}

console.log('✅ Extension script loaded');
