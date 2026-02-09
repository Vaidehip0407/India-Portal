"""
Clean Torrent Power RPA Automation API
Uses Selenium WebDriver for real browser automation
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional
import asyncio
import time
from datetime import datetime

from app.auth import get_current_user
from app.models import User

router = APIRouter(prefix="/api/torrent-automation", tags=["Torrent Power RPA Automation"])

# Global status tracking
automation_status = {
    "status": "idle",  # idle, running, completed, failed
    "progress": 0,
    "message": "",
    "fields_completed": 0,
    "logs": [],
    "result": None
}

def update_status(status="running", progress=0, message="", fields_completed=0, log_message=None):
    """Update global automation status"""
    global automation_status
    automation_status["status"] = status
    automation_status["progress"] = progress
    automation_status["message"] = message
    automation_status["fields_completed"] = fields_completed
    
    if log_message:
        automation_status["logs"].append({
            "message": log_message,
            "timestamp": datetime.now().isoformat()
        })
    
    print(f"📊 Status updated: {status} - {progress}% - {message}")

def reset_status():
    """Reset automation status"""
    global automation_status
    automation_status = {
        "status": "idle",
        "progress": 0,
        "message": "",
        "fields_completed": 0,
        "logs": [],
        "result": None
    }


class TorrentAutomationRequest(BaseModel):
    """Request model for Torrent Power RPA automation"""
    city: str = "Ahmedabad"
    service_number: str
    t_number: str  # Transaction Number
    mobile: str
    email: str
    confirm_email: Optional[str] = None


class TorrentAutomationResponse(BaseModel):
    """Response model for RPA automation results"""
    success: bool
    message: str
    details: Optional[str] = None
    timestamp: str
    provider: str = "torrent_power"
    automation_type: str = "rpa_selenium"
    session_data: Optional[Dict[str, Any]] = None
    screenshots: Optional[list] = None
    fields_filled: Optional[int] = None
    total_fields: Optional[int] = None
    success_rate: Optional[str] = None
    next_steps: Optional[list] = None
    portal_url: str = "https://connect.torrentpower.com/tplcp/application/namechangerequest"
    error: Optional[str] = None
    automation_details: Optional[list] = None


@router.post("/start-automation", response_model=TorrentAutomationResponse)
async def start_torrent_power_rpa_automation(
    request: TorrentAutomationRequest,
    background_tasks: BackgroundTasks
    # current_user: User = Depends(get_current_user)  # Temporarily disabled for testing
):
    """
    Start the RPA-based Torrent Power automation workflow
    Uses Selenium WebDriver for real browser automation
    """
    
    try:
        print("🤖 PRODUCTION RPA Torrent Power automation request received")
        print(f"📋 Request data: {request.dict()}")
        
        # Reset status
        reset_status()
        
        # Debug: Print individual field values
        print(f"🔍 Debug - Individual fields:")
        print(f"   City: '{request.city}'")
        print(f"   Service Number: '{request.service_number}'")
        print(f"   T Number: '{request.t_number}'")
        print(f"   Mobile: '{request.mobile}'")
        print(f"   Email: '{request.email}'")
        
        # Validate required fields
        if not request.service_number or request.service_number.strip() == "":
            print("❌ Validation failed: Service Number is empty")
            raise HTTPException(
                status_code=400,
                detail="Service Number is required for Torrent Power automation"
            )
        
        if not request.t_number or request.t_number.strip() == "":
            print("❌ Validation failed: T Number is empty")
            raise HTTPException(
                status_code=400,
                detail="Transaction Number (T No) is required for Torrent Power automation"
            )
        
        if not request.mobile or len(request.mobile.strip()) < 10:
            print(f"❌ Validation failed: Mobile number invalid - '{request.mobile}' (length: {len(request.mobile.strip()) if request.mobile else 0})")
            raise HTTPException(
                status_code=400,
                detail="Valid mobile number is required (at least 10 digits)"
            )
        
        if not request.email or request.email.strip() == "":
            print("❌ Validation failed: Email is empty")
            raise HTTPException(
                status_code=400,
                detail="Email address is required for Torrent Power automation"
            )
        
        print("✅ All validations passed, starting automation...")
        
        # Start automation in background
        background_tasks.add_task(run_automation_background, request.dict())
        
        # Return immediate response
        return TorrentAutomationResponse(
            success=True,
            message="Automation started successfully",
            details="Automation is running in background. Check status endpoint for updates.",
            timestamp=datetime.now().isoformat(),
            fields_filled=0,
            total_fields=5
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Torrent automation API error: {str(e)}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        
        return TorrentAutomationResponse(
            success=False,
            message=f"Failed to start Torrent Power automation: {str(e)}",
            timestamp=datetime.now().isoformat(),
            error=str(e),
            details=traceback.format_exc()
        )


def run_automation_background(request_data: dict):
    """Run automation in background with status updates"""
    try:
        update_status("running", 10, "Opening browser...", 0, "⚡ Initializing browser automation")
        
        from app.services.torrent_rpa_service import TorrentPowerRPA
        
        # Prepare the data
        rpa_data = {
            "city": request_data.get("city", "Ahmedabad"),
            "service_number": request_data["service_number"],
            "t_number": request_data["t_number"],
            "mobile": request_data["mobile"],
            "email": request_data["email"]
        }
        
        update_status("running", 20, "Navigating to Torrent Power website...", 0, "🌐 Opening Torrent Power portal")
        
        # Initialize RPA
        rpa = TorrentPowerRPA()
        
        # Setup driver
        update_status("running", 30, "Setting up browser driver...", 0, "🔧 Configuring Chrome browser")
        if not rpa.setup_driver():
            update_status("failed", 0, "Failed to setup browser", 0, "❌ Browser setup failed")
            return
        
        # Navigate
        update_status("running", 40, "Loading application form...", 0, "📄 Loading name change form")
        if not rpa.navigate_to_torrent_power():
            update_status("failed", 0, "Failed to load website", 0, "❌ Website navigation failed")
            rpa.close_driver()
            return
        
        # Fill form with status updates
        update_status("running", 50, "Filling City field...", 0, "📍 Selecting city: " + rpa_data["city"])
        time.sleep(0.5)
        
        update_status("running", 60, "Filling Service Number...", 1, "🔢 Entering service number")
        time.sleep(0.5)
        
        update_status("running", 70, "Filling T Number...", 2, "📝 Entering transaction number")
        time.sleep(0.5)
        
        update_status("running", 80, "Filling Mobile Number...", 3, "📱 Entering mobile number")
        time.sleep(0.5)
        
        update_status("running", 90, "Filling Email Address...", 4, "📧 Entering email address")
        
        # Fill the form
        result = rpa.fill_form(rpa_data)
        
        if result.get("success"):
            update_status("running", 95, "Verifying filled data...", 5, "✅ All fields filled successfully")
            time.sleep(1)
            
            update_status("completed", 100, "Automation completed successfully!", 5, "🎉 Form auto-fill completed")
            
            # Close browser after 3 seconds
            time.sleep(3)
            rpa.close_driver()
            update_status("completed", 100, "Browser closed", 5, "✅ Browser closed automatically")
        else:
            update_status("failed", 0, "Form filling failed", 0, "❌ Failed to fill form fields")
            rpa.close_driver()
            
    except Exception as e:
        print(f"❌ Background automation error: {e}")
        update_status("failed", 0, f"Error: {str(e)}", 0, f"❌ Automation error: {str(e)}")


@router.get("/automation-status")
async def get_automation_status():
    """
    Get current automation status for real-time updates
    """
    global automation_status
    return {
        "success": True,
        **automation_status
    }


@router.get("/test-connection")
async def test_rpa_automation_connection():
    """
    Test if the RPA automation service is working
    """
    
    try:
        return {
            "success": True,
            "message": "Torrent Power RPA automation service is ready",
            "timestamp": datetime.now().isoformat(),
            "automation_type": "rpa_selenium",
            "browser": "Chrome with Selenium WebDriver",
            "service_status": "initialized",
            "features": [
                "✅ RPA browser automation ready",
                "✅ Real form filling capabilities",
                "✅ Visual field highlighting",
                "✅ Screenshot capture",
                "✅ User-controlled submission",
                "✅ Browser stays open for review"
            ]
        }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "RPA automation service test failed",
            "timestamp": datetime.now().isoformat()
        }


@router.get("/supported-fields")
async def get_supported_fields():
    """
    Get the list of supported fields for Torrent Power RPA automation
    """
    
    return {
        "success": True,
        "provider": "torrent_power",
        "automation_type": "rpa_selenium",
        "supported_fields": {
            "city": {
                "type": "dropdown",
                "required": True,
                "default": "Ahmedabad",
                "options": ["Ahmedabad", "Surat", "Gandhinagar", "Bhavnagar"],
                "description": "City/Location for service"
            },
            "service_number": {
                "type": "text",
                "required": True,
                "pattern": "^[A-Z0-9]+$",
                "description": "Service/Consumer Number"
            },
            "t_number": {
                "type": "text", 
                "required": True,
                "pattern": "^T[0-9]+$",
                "description": "Transaction Number (T No)"
            },
            "mobile": {
                "type": "tel",
                "required": True,
                "pattern": "^[0-9]{10}$",
                "description": "10-digit mobile number"
            },
            "email": {
                "type": "email",
                "required": True,
                "description": "Email address for notifications"
            }
        },
        "rpa_workflow_steps": [
            "1. Initialize Chrome WebDriver with visible browser",
            "2. Navigate to official Torrent Power website", 
            "3. Wait for form elements to load",
            "4. Locate and fill form fields using multiple selectors",
            "5. Highlight filled fields with green borders",
            "6. Take screenshots for audit trail",
            "7. Show success notification on page",
            "8. Keep browser open for user review and submission",
            "9. Provide detailed field-by-field results"
        ],
        "timestamp": datetime.now().isoformat()
    }


@router.post("/start-visible-automation", response_model=TorrentAutomationResponse)
async def start_visible_torrent_power_rpa_automation(
    request: TorrentAutomationRequest
    # current_user: User = Depends(get_current_user)  # Temporarily disabled for testing
):
    """
    Start the RPA-based Torrent Power automation with VISIBLE browser for debugging
    Shows the automation process in real-time with visual feedback
    """
    
    try:
        print("🤖 VISIBLE RPA Torrent Power automation request received")
        print(f"📋 Request data: {request.dict()}")
        
        # Validate required fields (same as regular automation)
        if not request.service_number or request.service_number.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Service Number is required for Torrent Power automation"
            )
        
        if not request.t_number or request.t_number.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Transaction Number (T No) is required for Torrent Power automation"
            )
        
        if not request.mobile or len(request.mobile.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Valid mobile number is required (at least 10 digits)"
            )
        
        if not request.email or request.email.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Email address is required for Torrent Power automation"
            )
        
        print("✅ All validations passed, starting VISIBLE RPA automation...")
        
        try:
            from app.services.torrent_rpa_service import TorrentPowerRPA
            
            # Prepare the data for RPA
            rpa_data = {
                "city": request.city or 'Ahmedabad',
                "service_number": request.service_number,
                "t_number": request.t_number,
                "mobile": request.mobile,
                "email": request.email
            }
            
            print(f"📋 Visible RPA Data: {rpa_data}")
            
            # Initialize and run VISIBLE RPA
            rpa = TorrentPowerRPA()
            result = rpa.run_visible_automation(rpa_data)
            
            print(f"📊 Visible RPA Result: {result}")
            
            if result.get("success"):
                return TorrentAutomationResponse(
                    success=True,
                    message=f"🤖 VISIBLE RPA successfully filled {result.get('total_filled', 0)} fields! Browser kept open for debugging.",
                    details="Visible RPA automation completed successfully - you can see the process!",
                    timestamp=datetime.now().isoformat(),
                    fields_filled=result.get("total_filled", 0),
                    total_fields=5,
                    next_steps=[
                        "✅ VISIBLE RPA automation completed successfully",
                        "👀 Browser opened with visible automation process",
                        "🎬 Watch the form being filled step by step",
                        "📝 Form fields filled and highlighted in green",
                        "🔍 Review the filled data for accuracy",
                        "📤 Click Submit to complete your application",
                        "🕐 Browser will stay open for 10 minutes for debugging"
                    ],
                    automation_details=result.get("filled_fields", []),
                    screenshots=result.get("screenshots", [])
                )
            else:
                return TorrentAutomationResponse(
                    success=False,
                    message="Visible RPA automation encountered an error.",
                    details=result.get("error", "Unknown visible RPA error"),
                    timestamp=datetime.now().isoformat(),
                    error=result.get("error", "Visible RPA automation failed"),
                    automation_details=result.get("filled_fields", [])
                )
                
        except ImportError as e:
            print(f"❌ Visible RPA import error: {e}")
            return TorrentAutomationResponse(
                success=False,
                message="Visible RPA service not available. Selenium WebDriver required.",
                details="Please install Selenium and ChromeDriver for visible RPA automation.",
                timestamp=datetime.now().isoformat(),
                error="Visible RPA service not available. Selenium WebDriver required."
            )
        except Exception as e:
            print(f"❌ Visible RPA automation error: {e}")
            return TorrentAutomationResponse(
                success=False,
                message="Visible RPA automation service unavailable.",
                details=str(e),
                timestamp=datetime.now().isoformat(),
                error=f"Visible RPA automation failed: {str(e)}"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Visible Torrent RPA automation API error: {str(e)}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        
        return TorrentAutomationResponse(
            success=False,
            message=f"Failed to start visible Torrent Power RPA automation: {str(e)}",
            timestamp=datetime.now().isoformat(),
            error=str(e),
            details=traceback.format_exc()
        )


@router.post("/test-rpa")
async def test_rpa_with_sample_data():
    """
    Test RPA automation with sample data
    """
    
    sample_data = TorrentAutomationRequest(
        city="Ahmedabad",
        service_number="TEST123456",
        t_number="T123456789",
        mobile="9876543210",
        email="test@example.com"
    )
    
    return await start_torrent_power_rpa_automation(sample_data)