"""
OCR Service for extracting data from documents
Supports: Aadhar Card, PAN Card, Electricity Bill, Gas Bill, etc.
"""
import re
from typing import Dict, Optional
import pytesseract
from PIL import Image
import io

class OCRService:
    """Extract text and structured data from documents"""
    
    @staticmethod
    def extract_text_from_image(image_bytes: bytes) -> str:
        """Extract raw text from image using Tesseract OCR"""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""
    
    @staticmethod
    def extract_aadhar_data(text: str) -> Dict[str, str]:
        """Extract Aadhar card details"""
        data = {}
        
        # Extract Aadhar number (12 digits)
        aadhar_pattern = r'\b\d{4}\s?\d{4}\s?\d{4}\b'
        aadhar_match = re.search(aadhar_pattern, text)
        if aadhar_match:
            data['aadhar'] = aadhar_match.group().replace(' ', '')
        
        # Extract name (usually after "Name:" or before "DOB:")
        name_patterns = [
            r'(?:Name|नाम)[:\s]+([A-Za-z\s]+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
        ]
        for pattern in name_patterns:
            name_match = re.search(pattern, text, re.IGNORECASE)
            if name_match:
                data['name'] = name_match.group(1).strip()
                break
        
        # Extract DOB
        dob_pattern = r'(?:DOB|Date of Birth|जन्म तिथि)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})'
        dob_match = re.search(dob_pattern, text, re.IGNORECASE)
        if dob_match:
            data['dob'] = dob_match.group(1)
        
        # Extract Address
        address_pattern = r'(?:Address|पता)[:\s]+(.+?)(?=\n\n|\Z)'
        address_match = re.search(address_pattern, text, re.IGNORECASE | re.DOTALL)
        if address_match:
            data['address'] = address_match.group(1).strip()
        
        return data
    
    @staticmethod
    def extract_electricity_bill_data(text: str) -> Dict[str, str]:
        """Extract electricity bill details"""
        data = {}
        
        # Consumer number patterns
        consumer_patterns = [
            r'(?:Consumer No|Consumer Number|उपभोक्ता संख्या)[:\s]+([A-Z0-9]+)',
            r'(?:Account No|खाता संख्या)[:\s]+([A-Z0-9]+)'
        ]
        for pattern in consumer_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['consumer_number'] = match.group(1).strip()
                break
        
        # Name
        name_patterns = [
            r'(?:Name|नाम)[:\s]+([A-Za-z\s]+)',
            r'(?:Consumer Name)[:\s]+([A-Za-z\s]+)'
        ]
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['name'] = match.group(1).strip()
                break
        
        # Address
        address_pattern = r'(?:Address|पता)[:\s]+(.+?)(?=\n\n|Bill|Amount|\Z)'
        address_match = re.search(address_pattern, text, re.IGNORECASE | re.DOTALL)
        if address_match:
            data['address'] = address_match.group(1).strip()
        
        # Mobile number
        mobile_pattern = r'(?:Mobile|Mob|मोबाइल)[:\s]+([6-9]\d{9})'
        mobile_match = re.search(mobile_pattern, text, re.IGNORECASE)
        if mobile_match:
            data['mobile'] = mobile_match.group(1)
        
        return data
    
    @staticmethod
    def extract_gas_bill_data(text: str) -> Dict[str, str]:
        """Extract gas bill details"""
        data = {}
        
        # Consumer/Customer number
        consumer_patterns = [
            r'(?:Consumer No|Customer No|BP No)[:\s]+([A-Z0-9]+)',
            r'(?:उपभोक्ता संख्या)[:\s]+([A-Z0-9]+)'
        ]
        for pattern in consumer_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['consumer_number'] = match.group(1).strip()
                break
        
        # Name
        name_pattern = r'(?:Name|Customer Name|नाम)[:\s]+([A-Za-z\s]+)'
        name_match = re.search(name_pattern, text, re.IGNORECASE)
        if name_match:
            data['name'] = name_match.group(1).strip()
        
        # Address
        address_pattern = r'(?:Address|पता)[:\s]+(.+?)(?=\n\n|Bill|Amount|\Z)'
        address_match = re.search(address_pattern, text, re.IGNORECASE | re.DOTALL)
        if address_match:
            data['address'] = address_match.group(1).strip()
        
        # Mobile
        mobile_pattern = r'(?:Mobile|Contact|मोबाइल)[:\s]+([6-9]\d{9})'
        mobile_match = re.search(mobile_pattern, text, re.IGNORECASE)
        if mobile_match:
            data['mobile'] = mobile_match.group(1)
        
        return data
    
    @staticmethod
    def extract_pan_card_data(text: str) -> Dict[str, str]:
        """Extract PAN card details"""
        data = {}
        
        # PAN number
        pan_pattern = r'\b[A-Z]{5}\d{4}[A-Z]\b'
        pan_match = re.search(pan_pattern, text)
        if pan_match:
            data['pan'] = pan_match.group()
        
        # Name
        name_pattern = r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
        name_match = re.search(name_pattern, text)
        if name_match:
            data['name'] = name_match.group(1).strip()
        
        # Father's name
        father_pattern = r"(?:Father's Name)[:\s]+([A-Za-z\s]+)"
        father_match = re.search(father_pattern, text, re.IGNORECASE)
        if father_match:
            data['father_name'] = father_match.group(1).strip()
        
        # DOB
        dob_pattern = r'(\d{2}[/-]\d{2}[/-]\d{4})'
        dob_match = re.search(dob_pattern, text)
        if dob_match:
            data['dob'] = dob_match.group(1)
        
        return data
    
    @classmethod
    def process_document(cls, image_bytes: bytes, document_type: str) -> Dict[str, str]:
        """
        Process document and extract relevant data
        
        Args:
            image_bytes: Image file bytes
            document_type: Type of document (aadhar, pan, electricity_bill, gas_bill, etc.)
        
        Returns:
            Dictionary with extracted data
        """
        # Extract text from image
        text = cls.extract_text_from_image(image_bytes)
        
        if not text:
            return {}
        
        # Process based on document type
        if document_type == 'aadhar':
            return cls.extract_aadhar_data(text)
        elif document_type == 'electricity_bill':
            return cls.extract_electricity_bill_data(text)
        elif document_type == 'gas_bill':
            return cls.extract_gas_bill_data(text)
        elif document_type == 'pan':
            return cls.extract_pan_card_data(text)
        else:
            # Generic extraction
            return {
                'raw_text': text,
                'name': cls.extract_aadhar_data(text).get('name', ''),
                'address': cls.extract_aadhar_data(text).get('address', '')
            }

# Singleton instance
ocr_service = OCRService()
