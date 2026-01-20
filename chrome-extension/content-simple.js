// DGVCL Complete Auto-Fill Extension - v5.0 (Complete Flow Automation)
console.log('🚀 DGVCL Extension v6.0 - LATEST VERSION WITH CAPTCHA AUTO-CLICK');

// Run on page load
window.addEventListener('load', runExtension);
document.addEventListener('DOMContentLoaded', runExtension);

function runExtension() {
  if (!window.location.hostname.includes('guvnl.in')) return;
  
  const url = window.location.href;
  console.log('🔍 Page:', url);
  
  // STEP 1: Login Page
  if (url.includes('login.php')) {
    setTimeout(handleLoginPage, 1000);
  }
  // STEP 2: OTP Page
  else if (url.includes('checkOtp.php')) {
    setTimeout(handleOTPPage, 500);
  }
  // STEP 3: Select User Page
  else if (url.includes('Submit_Otp.php')) {
    setTimeout(handleSelectUserPage, 1000);
  }
  // STEP 4: Dashboard Page
  else if (url.includes('prtlDashboard.php')) {
    setTimeout(handleDashboardPage, 2000);
  }
  // STEP 5: Name Change Form Page
  else if (url.includes('ltNameChange.php') || url.includes('LTNameChange') || url.includes('namechange')) {
    setTimeout(handleNameChangeFormPage, 2000);
  }
}

// ============ STEP 1: LOGIN PAGE ============
function handleLoginPage() {
  const params = new URLSearchParams(window.location.search);
  const mobile = params.get('mobile');
  const discom = params.get('discom');
  
  if (!mobile) return;
  
  console.log('📱 STEP 1: Login - Filling:', mobile, discom);
  
  // Fill Mobile Number
  const mobileInput = document.querySelector('input[placeholder="Mobile No"]') ||
                     document.querySelector('input[type="text"]:not([placeholder*="Captcha"])');
  
  if (mobileInput && !mobileInput.placeholder.includes('Captcha')) {
    mobileInput.value = mobile;
    mobileInput.dispatchEvent(new Event('input', {bubbles: true}));
    mobileInput.style.background = '#c8f7c5';
    mobileInput.style.border = '2px solid #27ae60';
    console.log('✅ Mobile filled');
  }
  
  // Fill DISCOM Dropdown
  const select = document.querySelector('select');
  if (select && discom) {
    for (let opt of select.options) {
      if (opt.text.toUpperCase().includes(discom.toUpperCase())) {
        select.value = opt.value;
        select.dispatchEvent(new Event('change', {bubbles: true}));
        select.style.background = '#c8f7c5';
        select.style.border = '2px solid #27ae60';
        console.log('✅ DISCOM selected');
        break;
      }
    }
  }
  
  showMsg('✅ STEP 1: Auto-filled Login\n👉 Enter Captcha & Click Login', 'green');
  
  // Auto-click Login button after captcha is filled
  console.log('🔍 Looking for captcha field...');
  const captchaInput = document.querySelector('input[placeholder*="Captcha"]') || 
                      document.querySelector('input[placeholder*="captcha"]') ||
                      document.querySelector('input[name*="captcha"]') ||
                      document.querySelector('input[id*="captcha"]');
  
  if (captchaInput) {
    console.log('✅ Found captcha field:', captchaInput);
    captchaInput.style.border = '2px solid #e74c3c';
    
    // Monitor captcha input for changes
    captchaInput.addEventListener('input', function() {
      console.log('📝 Captcha input detected, length:', this.value.length);
      
      if (this.value.length >= 4) { // Assuming captcha is at least 4 characters
        console.log('✅ Captcha seems complete, looking for login button...');
        
        setTimeout(() => {
          // Try multiple selectors for login button
          const loginBtn = document.querySelector('input[value="Login"]') ||
                          document.querySelector('button[type="submit"]') ||
                          document.querySelector('input[type="submit"]') ||
                          document.querySelector('button:contains("Login")') ||
                          document.querySelector('.btn-primary') ||
                          document.querySelector('[onclick*="login"]');
          
          if (loginBtn) {
            console.log('✅ Found login button:', loginBtn);
            console.log('✅ Captcha entered, auto-clicking Login...');
            showMsg('🤖 Auto-clicking Login button...', 'blue');
            loginBtn.click();
          } else {
            console.log('❌ Login button not found');
            console.log('Available buttons:', document.querySelectorAll('button, input[type="submit"], input[type="button"]'));
          }
        }, 1500); // Wait 1.5 seconds after captcha entry
      }
    });
  } else {
    console.log('❌ Captcha field not found');
    console.log('Available input fields:', document.querySelectorAll('input'));
  }
}

// ============ STEP 2: OTP PAGE ============
function handleOTPPage() {
  console.log('📱 STEP 2: OTP Page');
  console.log('🔍 Current URL:', window.location.href);
  showMsg('📱 STEP 2: Enter OTP\n👉 Enter OTP sent to mobile & Click Submit', 'blue');
  
  // Focus OTP field
  const otpInput = document.querySelector('input[placeholder*="OTP"]') || 
                   document.querySelector('input[type="text"]');
  if (otpInput) {
    otpInput.focus();
    otpInput.style.border = '2px solid #3498db';
    console.log('✅ OTP input field focused');
    
    // Auto-click Submit after OTP is entered
    otpInput.addEventListener('input', function() {
      if (this.value.length >= 4) { // Assuming OTP is at least 4 digits
        setTimeout(() => {
          const submitBtn = document.querySelector('input[value="Submit Otp"]') ||
                           document.querySelector('button[type="submit"]') ||
                           document.querySelector('input[type="submit"]') ||
                           document.querySelector('button:contains("Submit")');
          
          if (submitBtn) {
            console.log('✅ OTP entered, auto-clicking Submit...');
            showMsg('🤖 Auto-clicking Submit button...', 'blue');
            submitBtn.click();
          }
        }, 1000); // Wait 1 second after OTP entry
      }
    });
  }
}

// ============ STEP 3: SELECT USER PAGE ============
function handleSelectUserPage() {
  console.log('🔄 STEP 3: Auto-submitting user selection...');
  console.log('🔍 Current URL:', window.location.href);
  showMsg('🔄 STEP 3: Auto-submitting...', 'orange');
  
  setTimeout(() => {
    const submitBtn = document.querySelector('input[value="Submit"]') ||
                     document.querySelector('input[type="submit"]') ||
                     document.querySelector('button[type="submit"]');
    
    if (submitBtn) {
      console.log('✅ Submit button found, clicking...');
      submitBtn.click();
    } else {
      console.log('⚠️ Submit button not found, trying fallback...');
      // Fallback: find any button with Submit text
      document.querySelectorAll('input, button').forEach(btn => {
        if (btn.value === 'Submit' || btn.textContent === 'Submit') {
          console.log('✅ Submit button (fallback) found, clicking...');
          btn.click();
        }
      });
    }
  }, 1500);
}

// ============ STEP 4: DASHBOARD PAGE ============
function handleDashboardPage() {
  console.log('🏠 STEP 4: Dashboard - Looking for LT Name Change...');
  
  // Debug: Check what's in localStorage
  console.log('🔍 Checking localStorage...');
  console.log('dgvcl_name_change_data:', localStorage.getItem('dgvcl_name_change_data'));
  console.log('dgvcl_autofill_data:', localStorage.getItem('dgvcl_autofill_data'));
  console.log('All localStorage keys:', Object.keys(localStorage));
  
  // Check if we have name change data - try both keys
  let storedData = localStorage.getItem('dgvcl_name_change_data') || localStorage.getItem('dgvcl_autofill_data');
  if (!storedData) {
    console.log('❌ No stored data found in localStorage');
    showMsg('⚠️ STEP 4: No data found\n👉 Manually click "LT Name Change"', 'orange');
    return;
  }
  
  console.log('📦 Found stored data:', storedData);
  const data = JSON.parse(storedData);
  console.log('📦 Parsed data:', data);
  
  if (data.application_type !== 'name_change') {
    console.log('❌ Not name change data, application_type:', data.application_type);
    showMsg('⚠️ STEP 4: Wrong data type\n👉 Navigate manually', 'orange');
    return;
  }
  
  console.log('✅ Name change data found, proceeding with automation...');
  showMsg('🤖 STEP 4: Auto-clicking "LT Name Change"...', 'blue');
  
  // Wait 3 seconds then click LT Name Change
  setTimeout(() => {
    // Multiple ways to find LT Name Change link
    const nameChangeLink = 
      // Method 1: Direct link
      document.querySelector('a[href*="ltNameChange"]') ||
      document.querySelector('a[href*="namechange"]') ||
      // Method 2: By text content
      Array.from(document.querySelectorAll('a')).find(a => 
        a.textContent.toLowerCase().includes('name change') ||
        a.textContent.toLowerCase().includes('lt name change')
      ) ||
      // Method 3: By image alt text
      document.querySelector('img[alt*="Name Change"]')?.parentElement ||
      // Method 4: By onclick attribute
      document.querySelector('[onclick*="namechange"]') ||
      document.querySelector('[onclick*="ltNameChange"]');
    
    if (nameChangeLink) {
      console.log('✅ Found LT Name Change link, clicking...');
      nameChangeLink.click();
    } else {
      // Manual search in all clickable elements
      const allClickable = document.querySelectorAll('a, div, span, td, li');
      allClickable.forEach(element => {
        const text = element.textContent || element.innerText || '';
        if (text.toLowerCase().includes('name change') || 
            text.toLowerCase().includes('lt name change')) {
          console.log('✅ Found Name Change element by text, clicking...');
          element.click();
        }
      });
    }
    
    // If still not found, show manual instruction
    setTimeout(() => {
      if (window.location.href.includes('prtlDashboard.php')) {
        showMsg('⚠️ Could not find "LT Name Change"\n👉 Please click manually', 'orange');
      }
    }, 2000);
    
  }, 3000);
}

// ============ STEP 5: NAME CHANGE FORM PAGE ============
function handleNameChangeFormPage() {
  console.log('📝 STEP 5: Name Change Form detected');
  
  // Debug: Check what's in localStorage
  console.log('🔍 Checking localStorage for form data...');
  console.log('dgvcl_name_change_data:', localStorage.getItem('dgvcl_name_change_data'));
  console.log('dgvcl_autofill_data:', localStorage.getItem('dgvcl_autofill_data'));
  
  // Get stored data - try both keys
  let storedData = localStorage.getItem('dgvcl_name_change_data') || localStorage.getItem('dgvcl_autofill_data');
  if (!storedData) {
    console.log('❌ No stored data found');
    showMsg('⚠️ No data found\n👉 Fill form manually', 'orange');
    return;
  }
  
  console.log('📦 Found stored data:', storedData);
  const data = JSON.parse(storedData);
  console.log('📦 Parsed data:', data);
  
  if (data.application_type !== 'name_change') {
    console.log('❌ Not name change data, application_type:', data.application_type);
    return;
  }
  
  console.log('✅ Name change data confirmed, filling form...');
  console.log('📦 Filling Name Change form with:', data);
  showMsg('🤖 STEP 5: Auto-filling Name Change form...', 'blue');
  
  let filled = 0;
  
  // Wait for form to load completely
  setTimeout(() => {
    
    // Fill New Name
    if (data.new_name) {
      const nameInputs = [
        document.querySelector('input[name*="name"]'),
        document.querySelector('input[name*="Name"]'),
        document.querySelector('input[placeholder*="name"]'),
        document.querySelector('input[placeholder*="Name"]')
      ];
      
      nameInputs.forEach(input => {
        if (input && !input.value) {
          fillInput(input, data.new_name);
          filled++;
        }
      });
    }
    
    // Fill Reason dropdown
    if (data.reason) {
      const reasonSelects = [
        document.querySelector('select[name*="reason"]'),
        document.querySelector('select[name*="Reason"]'),
        document.querySelector('select[id*="reason"]')
      ];
      
      reasonSelects.forEach(select => {
        if (select) {
          selectOption(select, data.reason);
          filled++;
        }
      });
    }
    
    // Handle Security Deposit radio buttons
    if (data.security_deposit_option) {
      const radioButtons = document.querySelectorAll('input[type="radio"]');
      radioButtons.forEach(radio => {
        const value = radio.value.toLowerCase();
        const option = data.security_deposit_option.toLowerCase();
        
        if ((option === 'entire' && value.includes('entire')) ||
            (option === 'difference' && value.includes('difference'))) {
          radio.checked = true;
          radio.dispatchEvent(new Event('change', {bubbles: true}));
          filled++;
        }
      });
    }
    
    // Fill Old Security Deposit Amount
    if (data.old_security_deposit) {
      const depositInputs = [
        document.querySelector('input[name*="deposit"]'),
        document.querySelector('input[name*="Deposit"]'),
        document.querySelector('input[name*="amount"]'),
        document.querySelector('input[name*="Amount"]')
      ];
      
      depositInputs.forEach(input => {
        if (input && !input.value) {
          fillInput(input, data.old_security_deposit);
          filled++;
        }
      });
    }
    
    if (filled > 0) {
      showMsg(`✅ STEP 5: Auto-filled ${filled} fields!\n👉 Auto-submitting form...`, 'green');
      console.log(`✅ Filled ${filled} fields in Name Change form`);
      
      // Auto-click Submit button after filling form
      setTimeout(() => {
        const submitBtn = document.querySelector('input[value="Submit"]') ||
                         document.querySelector('button[type="submit"]') ||
                         document.querySelector('input[type="submit"]') ||
                         document.querySelector('button:contains("Submit")') ||
                         document.querySelector('.btn-submit') ||
                         document.querySelector('[onclick*="submit"]');
        
        if (submitBtn) {
          console.log('✅ Found Submit button, auto-clicking...');
          showMsg('🤖 Auto-submitting Name Change form...', 'blue');
          submitBtn.click();
        } else {
          console.log('❌ Submit button not found');
          console.log('Available buttons:', document.querySelectorAll('button, input[type="submit"], input[type="button"]'));
          showMsg('⚠️ Submit button not found\n👉 Please submit manually', 'orange');
        }
      }, 2000); // Wait 2 seconds after filling form
      
    } else {
      showMsg('⚠️ Could not find form fields\n👉 Please fill manually', 'orange');
      
      // Debug: Show available form elements
      console.log('Available inputs:', document.querySelectorAll('input'));
      console.log('Available selects:', document.querySelectorAll('select'));
    }
    
  }, 1500);
}

// ============ HELPER FUNCTIONS ============
function fillInput(input, value) {
  if (!input) return;
  
  input.focus();
  input.value = '';
  input.value = value;
  input.dispatchEvent(new Event('input', {bubbles: true}));
  input.dispatchEvent(new Event('change', {bubbles: true}));
  input.style.background = '#c8f7c5';
  input.style.border = '2px solid #27ae60';
}

function selectOption(select, value) {
  if (!select) return;
  
  for (let opt of select.options) {
    if (opt.text.toUpperCase().includes(value.toUpperCase()) || 
        opt.value.toUpperCase().includes(value.toUpperCase())) {
      select.value = opt.value;
      select.dispatchEvent(new Event('change', {bubbles: true}));
      select.style.background = '#c8f7c5';
      select.style.border = '2px solid #27ae60';
      break;
    }
  }
}

function showMsg(text, color) {
  const colors = {
    green: '#27ae60',
    blue: '#3498db', 
    orange: '#e67e22',
    red: '#e74c3c',
    purple: '#9b59b6'
  };
  
  // Remove old notification
  const old = document.getElementById('dgvcl-msg');
  if (old) old.remove();
  
  const div = document.createElement('div');
  div.id = 'dgvcl-msg';
  div.innerHTML = text.replace(/\n/g, '<br>');
  div.style.cssText = `
    position: fixed;
    top: 15px;
    right: 15px;
    background: ${colors[color] || colors.blue};
    color: white;
    padding: 15px 25px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: bold;
    z-index: 999999;
    box-shadow: 0 5px 25px rgba(0,0,0,0.3);
    max-width: 320px;
    line-height: 1.6;
  `;
  document.body.appendChild(div);
  
  setTimeout(() => { if(div.parentNode) div.remove(); }, 8000);
}

console.log('✅ DGVCL Extension Ready - Complete 5-Step Automation!');