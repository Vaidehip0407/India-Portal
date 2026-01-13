"""
DGVCL RPA Integration - Auto-fill portal without extension
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import subprocess
import json
import os
from pathlib import Path

router = APIRouter(prefix="/api/rpa", tags=["RPA Automation"])

class DGVCLAutoFillRequest(BaseModel):
    mobile: str
    consumer_number: Optional[str] = None
    applicant_name: Optional[str] = None
    email: Optional[str] = None
    discom: str = "DGVCL"

class RPAResponse(BaseModel):
    success: bool
    message: str
    session_id: Optional[str] = None
    portal_url: Optional[str] = None

# Store active RPA sessions
active_sessions = {}

@router.post("/dgvcl/auto-fill", response_model=RPAResponse)
async def trigger_dgvcl_autofill(
    request: DGVCLAutoFillRequest,
    background_tasks: BackgroundTasks
):
    """
    Trigger RPA bot to auto-fill DGVCL portal
    Bot will open browser and fill form automatically
    """
    try:
        # Get RPA script path
        rpa_script = Path(__file__).parent.parent.parent.parent / "rpa-automation" / "dgvcl_name_change_final.py"
        
        if not rpa_script.exists():
            raise HTTPException(
                status_code=500,
                detail="RPA script not found. Please ensure rpa-automation folder exists."
            )
        
        # Prepare data for RPA bot
        rpa_data = {
            "mobile": request.mobile,
            "consumer_number": request.consumer_number,
            "applicant_name": request.applicant_name,
            "email": request.email,
            "discom": request.discom
        }
        
        # Save data to temp file for RPA bot to read
        temp_file = Path("/tmp/dgvcl_rpa_data.json")
        with open(temp_file, "w") as f:
            json.dump(rpa_data, f)
        
        # Run RPA bot in background
        background_tasks.add_task(run_rpa_bot, str(rpa_script), str(temp_file))
        
        return RPAResponse(
            success=True,
            message="RPA bot started! Browser will open automatically and fill the form.",
            portal_url="https://portal.guvnl.in/login.php"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start RPA bot: {str(e)}"
        )

def run_rpa_bot(script_path: str, data_file: str):
    """Run RPA bot in background"""
    try:
        # Run Python script
        result = subprocess.run(
            ["python3", script_path, data_file],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            print(f"✅ RPA bot completed successfully")
            print(result.stdout)
        else:
            print(f"❌ RPA bot failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ RPA bot timeout after 5 minutes")
    except Exception as e:
        print(f"❌ RPA bot error: {str(e)}")

@router.get("/dgvcl/status/{session_id}")
async def get_rpa_status(session_id: str):
    """Get RPA bot status"""
    if session_id in active_sessions:
        return active_sessions[session_id]
    else:
        return {
            "status": "not_found",
            "message": "Session not found"
        }
