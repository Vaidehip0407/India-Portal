"""
Documents Router - Upload, OCR, and Auto-fill
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import os
from datetime import datetime

from app.database import get_db
from app.auth import get_current_user
from app.models import User, Document
from app.services.ocr_service import ocr_service

router = APIRouter(prefix="/api/documents", tags=["Documents"])

# Upload directory
UPLOAD_DIR = "uploads/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload document and extract data using OCR
    
    Supported document types:
    - aadhar: Aadhar Card
    - pan: PAN Card
    - electricity_bill: Electricity Bill
    - gas_bill: Gas Bill
    - water_bill: Water Bill
    - property_document: Property Document
    """
    try:
        # Read file content
        content = await file.read()
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{current_user.id}_{document_type}_{timestamp}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        # Save file
        with open(filepath, "wb") as f:
            f.write(content)
        
        # Extract data using OCR
        extracted_data = {}
        if file.content_type and file.content_type.startswith('image/'):
            extracted_data = ocr_service.process_document(content, document_type)
        
        # Save document record in database
        document = Document(
            user_id=current_user.id,
            document_type=document_type,
            filename=filename,
            filepath=filepath,
            extracted_data=extracted_data
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        
        return {
            "success": True,
            "message": "Document uploaded successfully",
            "document_id": document.id,
            "extracted_data": extracted_data,
            "filename": filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/")
async def get_user_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all documents for current user"""
    documents = db.query(Document).filter(
        Document.user_id == current_user.id
    ).order_by(Document.created_at.desc()).all()
    
    return documents

@router.get("/{document_id}")
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific document"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document

@router.get("/autofill/{document_type}")
async def get_autofill_data(
    document_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get auto-fill data from user's uploaded documents
    Returns merged data from all relevant documents
    """
    # Get user's documents of this type
    documents = db.query(Document).filter(
        Document.user_id == current_user.id,
        Document.document_type == document_type
    ).order_by(Document.created_at.desc()).limit(1).all()
    
    if not documents:
        return {"data": {}}
    
    # Return extracted data from most recent document
    return {"data": documents[0].extracted_data or {}}

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete document"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file from disk
    if os.path.exists(document.filepath):
        os.remove(document.filepath)
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return {"success": True, "message": "Document deleted successfully"}
