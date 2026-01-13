# DGVCL Auto-Fill Solution (No Extension Needed!) 🤖

## Problem
- Chrome Extension har koi install nahi kar sakta
- Manual form filling time consuming hai
- Users ko technical knowledge nahi hai

## Solution: RPA Bot (Backend Automation)

Backend se **Selenium bot** automatically browser khol ke form fill karega!

---

## How It Works 🔄

```
User submits form → Backend triggers RPA bot
                  ↓
Bot opens Chrome browser (visible)
                  ↓
Bot logs into DGVCL portal
                  ↓
Bot fills mobile & DGVCL dropdown
                  ↓
Bot fills Step 1 (Applicant Details)
                  ↓
Browser stays open for user
                  ↓
User completes remaining steps manually
```

---

## Setup on EC2 Server

### 1. Install Chrome & ChromeDriver

```bash
# SSH into EC2
ssh -i gov-portal.pem ubuntu@your-ec2-ip

# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f -y

# Install ChromeDriver
wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# Verify installation
google-chrome --version
chromedriver --version
```

### 2. Install Python Dependencies

```bash
cd unified-portal
pip3 install selenium
```

### 3. Test RPA Bot Manually

```bash
cd rpa-automation
python3 dgvcl_name_change_final.py
```

---

## Usage

### From Your Portal:

1. **User fills form:**
   - Go to: `http://your-ec2-ip:3000/services/electricity`
   - Select DGVCL
   - Fill mobile: 9999999999
   - Fill consumer number: 1234567890
   - Click Submit

2. **RPA Bot triggers automatically:**
   - Backend calls RPA script
   - Chrome browser opens on EC2 server
   - Bot logs into DGVCL portal
   - Bot fills mobile & DGVCL dropdown
   - Bot fills Step 1 fields

3. **User completes manually:**
   - Browser stays open
   - User uploads documents (Step 2)
   - User makes payment (Step 3)
   - User submits application (Step 4)

---

## API Endpoint

```bash
POST /api/rpa/dgvcl/auto-fill
Content-Type: application/json

{
  "mobile": "9999999999",
  "consumer_number": "1234567890",
  "applicant_name": "John Doe",
  "email": "john@example.com",
  "discom": "DGVCL"
}
```

**Response:**
```json
{
  "success": true,
  "message": "RPA bot started! Browser will open automatically.",
  "portal_url": "https://portal.guvnl.in/login.php"
}
```

---

## Safety Features 🔒

✅ **Only fills Step 1** - No automatic submission
✅ **Visible browser** - User can monitor process
✅ **No document upload** - User uploads manually
✅ **No payment** - User pays manually
✅ **No final submit** - User submits manually
✅ **15 minute timeout** - Browser stays open

---

## Advantages vs Extension

| Feature | Chrome Extension | RPA Bot |
|---------|-----------------|---------|
| Installation | ❌ User must install | ✅ No installation |
| Works for all users | ❌ Only who install | ✅ Yes, all users |
| Technical knowledge | ❌ Required | ✅ Not required |
| Browser compatibility | ❌ Chrome only | ✅ Any browser |
| Auto-fill capability | ⚠️ Limited (CORS) | ✅ Full control |
| OTP handling | ❌ Cannot handle | ✅ Can handle |
| Document upload | ❌ Cannot do | ✅ Can do (if enabled) |

---

## Troubleshooting

### Bot not starting?

**Check Chrome installation:**
```bash
google-chrome --version
# Should show: Google Chrome 114.x.x
```

**Check ChromeDriver:**
```bash
chromedriver --version
# Should show: ChromeDriver 114.x.x
```

**Check Selenium:**
```bash
python3 -c "import selenium; print(selenium.__version__)"
# Should show: 4.x.x
```

### Bot fails to open browser?

**Install display server (for headless EC2):**
```bash
sudo apt-get install xvfb
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &
```

**Or use headless mode:**
Edit `dgvcl_name_change_final.py`:
```python
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
```

### Bot cannot find elements?

**Check DGVCL portal structure:**
- Portal may have changed
- Update selectors in script
- Check console logs

---

## Alternative: Simple Iframe Solution

Agar RPA bot bhi nahi chahiye, to **iframe** use karein:

### Option 3: Embedded Portal (Simplest!)

```javascript
// In NameChangeForm.jsx
const handleSubmit = () => {
  // Save data
  localStorage.setItem('dgvcl_data', JSON.stringify(formData));
  
  // Show DGVCL portal in iframe
  setIframeUrl('https://portal.guvnl.in/login.php');
  setShowIframe(true);
};

// Render iframe
{showIframe && (
  <iframe 
    src={iframeUrl}
    width="100%"
    height="800px"
    title="DGVCL Portal"
  />
)}
```

**Pros:**
- ✅ No extension needed
- ✅ No RPA bot needed
- ✅ User stays on your portal
- ✅ Simple implementation

**Cons:**
- ❌ Cannot auto-fill (CORS)
- ❌ User must fill manually
- ❌ Portal may block iframe (X-Frame-Options)

---

## Recommendation 🎯

**Best Solution:** RPA Bot (Option 1)
- Fully automatic
- No user installation
- Works for everyone
- Professional experience

**Fallback:** Manual Portal Open (Current)
- Simple
- No setup needed
- User fills manually

**Not Recommended:** Chrome Extension
- Requires installation
- Not all users can install
- Technical knowledge needed

---

## Implementation Status

✅ RPA script created (`dgvcl_name_change_final.py`)
✅ Backend API endpoint (`/api/rpa/dgvcl/auto-fill`)
✅ Frontend integration (NameChangeForm.jsx)
⏳ EC2 setup pending (Chrome + ChromeDriver)
⏳ Testing pending

---

## Next Steps

1. **Setup EC2:**
   ```bash
   # Install Chrome & ChromeDriver
   # Install Selenium
   # Test RPA script
   ```

2. **Deploy Code:**
   ```bash
   git pull origin main
   pm2 restart backend
   pm2 restart frontend
   ```

3. **Test End-to-End:**
   - Submit form
   - Verify bot starts
   - Check browser opens
   - Verify fields filled

---

**Status:** ✅ Code Ready, ⏳ EC2 Setup Pending
**Last Updated:** January 12, 2026
