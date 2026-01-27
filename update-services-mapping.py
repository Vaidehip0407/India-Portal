#!/usr/bin/env python3
"""
Update Services Data with Correct Direct Access Mapping
Based on actual website analysis
"""
import json

# Updated Direct Access Services with Actual Form Fields
DIRECT_ACCESS_SERVICES = {
    "gas": [
        {
            "id": "gujarat-gas",
            "name": "Gujarat Gas Ltd",
            "type": "government",
            "portal_url": "https://www.gujaratgas.com",
            "name_change_url": "https://iconnect.gujaratgas.com/Portal/outer-service-request_template.aspx",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": False,
            "direct_access": True,
            "automation_type": "direct_form",
            "form_type": "web_form",
            "reality_check": "Direct service request opens without login (verified)",
            "form_fields": [
                {
                    "name": "consumer_number",
                    "label": "Consumer Number",
                    "label_hindi": "उपभोक्ता संख्या",
                    "label_gujarati": "ગ્રાહક નંબર",
                    "type": "text",
                    "required": True,
                    "placeholder": "Enter Gujarat Gas consumer number",
                    "validation": "^[A-Z0-9]{8,12}$",
                    "selenium_selector": "input[name='txtConsumerNo']"
                },
                {
                    "name": "service_type",
                    "label": "Service Type",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": "name_change", "label": "Name Change"},
                        {"value": "address_change", "label": "Address Change"}
                    ],
                    "selenium_selector": "select[name='ddlServiceType']"
                },
                {
                    "name": "current_name",
                    "label": "Current Name (as per gas bill)",
                    "label_hindi": "वर्तमान नाम (गैस बिल के अनुसार)",
                    "label_gujarati": "વર્તમાન નામ (ગેસ બિલ મુજબ)",
                    "type": "text",
                    "required": True,
                    "placeholder": "Enter current name as per gas bill",
                    "ocr_field": "name",
                    "selenium_selector": "input[name='txtCurrentName']"
                },
                {
                    "name": "new_name",
                    "label": "New Name",
                    "label_hindi": "नया नाम",
                    "label_gujarati": "નવું નામ",
                    "type": "text",
                    "required": True,
                    "placeholder": "Enter new name",
                    "selenium_selector": "input[name='txtNewName']"
                },
                {
                    "name": "mobile",
                    "label": "Mobile Number",
                    "label_hindi": "मोबाइल नंबर",
                    "label_gujarati": "મોબાઇલ નંબર",
                    "type": "tel",
                    "required": True,
                    "placeholder": "Enter 10-digit mobile number",
                    "validation": "^[6-9][0-9]{9}$",
                    "selenium_selector": "input[name='txtMobile']"
                },
                {
                    "name": "email",
                    "label": "Email Address",
                    "label_hindi": "ईमेल पता",
                    "label_gujarati": "ઇમેઇલ સરનામું",
                    "type": "email",
                    "required": False,
                    "placeholder": "Enter email address",
                    "selenium_selector": "input[name='txtEmail']"
                },
                {
                    "name": "address",
                    "label": "Service Address",
                    "label_hindi": "सेवा पता",
                    "label_gujarati": "સેવા સરનામું",
                    "type": "textarea",
                    "required": True,
                    "placeholder": "Enter complete service address",
                    "ocr_field": "address",
                    "selenium_selector": "textarea[name='txtAddress']"
                },
                {
                    "name": "reason",
                    "label": "Reason for Name Change",
                    "label_hindi": "नाम परिवर्तन का कारण",
                    "label_gujarati": "નામ બદલવાનું કારણ",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": "marriage", "label": "Marriage", "label_hindi": "विवाह", "label_gujarati": "લગ્ન"},
                        {"value": "divorce", "label": "Divorce", "label_hindi": "तलाक", "label_gujarati": "છૂટાછેડા"},
                        {"value": "legal", "label": "Legal Name Change", "label_hindi": "कानूनी नाम परिवर्तन", "label_gujarati": "કાનૂની નામ બદલાવ"},
                        {"value": "other", "label": "Other", "label_hindi": "अन्य", "label_gujarati": "અન્ય"}
                    ],
                    "selenium_selector": "select[name='ddlReason']"
                }
            ]
        },
        {
            "id": "torrent-gas",
            "name": "Torrent Gas",
            "type": "private",
            "portal_url": "https://www.torrentgas.com",
            "name_change_url": "https://www.torrentgas.com/customer-services/name-change",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": False,
            "direct_access": True,
            "automation_type": "pdf_form",
            "form_type": "pdf_download",
            "reality_check": "PDF form opens without login",
            "form_fields": [
                {
                    "name": "consumer_number",
                    "label": "Consumer Number",
                    "label_hindi": "उपभोक्ता संख्या",
                    "label_gujarati": "ગ્રાહક નંબર",
                    "type": "text",
                    "required": True,
                    "placeholder": "Enter Torrent Gas consumer number",
                    "validation": "^[A-Z0-9]{8,12}$"
                },
                {
                    "name": "current_name",
                    "label": "Current Name (as per gas bill)",
                    "type": "text",
                    "required": True,
                    "ocr_field": "name"
                },
                {
                    "name": "new_name",
                    "label": "New Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "mobile",
                    "label": "Mobile Number",
                    "type": "tel",
                    "required": True,
                    "validation": "^[6-9][0-9]{9}$"
                },
                {
                    "name": "address",
                    "label": "Service Address",
                    "type": "textarea",
                    "required": True,
                    "ocr_field": "address"
                }
            ]
        },
        {
            "id": "vadodara-gas",
            "name": "Vadodara Gas Ltd",
            "type": "private",
            "portal_url": "https://www.vgl.co.in",
            "name_change_url": "https://www.vgl.co.in/customer-services",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": False,
            "direct_access": True,
            "automation_type": "pdf_form",
            "form_type": "affidavit_pdf",
            "reality_check": "Affidavit PDF without login",
            "form_fields": [
                {
                    "name": "consumer_number",
                    "label": "Consumer Number",
                    "type": "text",
                    "required": True,
                    "validation": "^[A-Z0-9]{8,12}$"
                },
                {
                    "name": "current_name",
                    "label": "Current Name",
                    "type": "text",
                    "required": True,
                    "ocr_field": "name"
                },
                {
                    "name": "new_name",
                    "label": "New Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "mobile",
                    "label": "Mobile Number",
                    "type": "tel",
                    "required": True,
                    "validation": "^[6-9][0-9]{9}$"
                },
                {
                    "name": "address",
                    "label": "Address",
                    "type": "textarea",
                    "required": True,
                    "ocr_field": "address"
                }
            ]
        }
    ],
    "electricity": [
        {
            "id": "torrent-power",
            "name": "Torrent Power",
            "type": "private",
            "portal_url": "https://www.torrentpower.com",
            "name_change_url": "https://connect.torrentpower.com",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": False,
            "direct_access": True,
            "automation_type": "pdf_form",
            "form_type": "pdf_download",
            "reality_check": "PDF form without login (portal optional)",
            "form_fields": [
                {
                    "name": "consumer_number",
                    "label": "Consumer Number",
                    "label_hindi": "उपभोक्ता संख्या",
                    "label_gujarati": "ગ્રાહક નંબર",
                    "type": "text",
                    "required": True,
                    "placeholder": "Enter Torrent Power consumer number",
                    "validation": "^[A-Z0-9]{10,14}$"
                },
                {
                    "name": "service_number",
                    "label": "Service Number",
                    "label_hindi": "सेवा संख्या",
                    "label_gujarati": "સેવા નંબર",
                    "type": "text",
                    "required": False,
                    "placeholder": "Enter service number if available"
                },
                {
                    "name": "current_name",
                    "label": "Current Name (as per electricity bill)",
                    "type": "text",
                    "required": True,
                    "ocr_field": "name"
                },
                {
                    "name": "new_name",
                    "label": "New Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "mobile",
                    "label": "Mobile Number",
                    "type": "tel",
                    "required": True,
                    "validation": "^[6-9][0-9]{9}$"
                },
                {
                    "name": "email",
                    "label": "Email Address",
                    "type": "email",
                    "required": False
                },
                {
                    "name": "address",
                    "label": "Service Address",
                    "type": "textarea",
                    "required": True,
                    "ocr_field": "address"
                },
                {
                    "name": "city",
                    "label": "City",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": "ahmedabad", "label": "Ahmedabad"},
                        {"value": "gandhinagar", "label": "Gandhinagar"},
                        {"value": "surat", "label": "Surat"},
                        {"value": "bhiwandi", "label": "Bhiwandi"},
                        {"value": "agra", "label": "Agra"}
                    ]
                }
            ]
        }
    ],
    "water": [
        {
            "id": "gwssb",
            "name": "Gujarat Water Supply (GWSSB)",
            "type": "government",
            "portal_url": "https://watersupply.gujarat.gov.in",
            "name_change_url": "https://watersupply.gujarat.gov.in/forms",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": False,
            "direct_access": True,
            "automation_type": "web_form",
            "form_type": "forms_page",
            "reality_check": "Forms page opens (no login)",
            "form_fields": [
                {
                    "name": "consumer_id",
                    "label": "Consumer ID / Connection Number",
                    "label_hindi": "उपभोक्ता आईडी / कनेक्शन संख्या",
                    "label_gujarati": "ગ્રાહક આઈડી / કનેક્શન નંબર",
                    "type": "text",
                    "required": True,
                    "placeholder": "Enter GWSSB consumer ID",
                    "validation": "^[A-Z0-9]{8,15}$"
                },
                {
                    "name": "zone",
                    "label": "Zone / Division",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": "ahmedabad", "label": "Ahmedabad Zone"},
                        {"value": "surat", "label": "Surat Zone"},
                        {"value": "vadodara", "label": "Vadodara Zone"},
                        {"value": "rajkot", "label": "Rajkot Zone"}
                    ]
                },
                {
                    "name": "current_name",
                    "label": "Current Name (as per water bill)",
                    "type": "text",
                    "required": True,
                    "ocr_field": "name"
                },
                {
                    "name": "new_name",
                    "label": "New Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "mobile",
                    "label": "Mobile Number",
                    "type": "tel",
                    "required": True,
                    "validation": "^[6-9][0-9]{9}$"
                },
                {
                    "name": "address",
                    "label": "Service Address",
                    "type": "textarea",
                    "required": True,
                    "ocr_field": "address"
                }
            ]
        }
    ],
    "property": [
        {
            "id": "anyror",
            "name": "AnyROR Gujarat",
            "type": "government",
            "portal_url": "https://anyror.gujarat.gov.in",
            "name_change_url": "https://anyror.gujarat.gov.in",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": False,
            "direct_access": True,
            "automation_type": "record_view",
            "form_type": "public_records",
            "reality_check": "Public record view & forms (no login)",
            "form_fields": [
                {
                    "name": "district",
                    "label": "District",
                    "label_hindi": "जिला",
                    "label_gujarati": "જિલ્લો",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": "ahmedabad", "label": "Ahmedabad"},
                        {"value": "surat", "label": "Surat"},
                        {"value": "vadodara", "label": "Vadodara"},
                        {"value": "rajkot", "label": "Rajkot"}
                    ]
                },
                {
                    "name": "taluka",
                    "label": "Taluka",
                    "type": "select",
                    "required": True,
                    "depends_on": "district"
                },
                {
                    "name": "village",
                    "label": "Village",
                    "type": "select",
                    "required": True,
                    "depends_on": "taluka"
                },
                {
                    "name": "survey_number",
                    "label": "Survey Number",
                    "type": "text",
                    "required": True,
                    "validation": "^[0-9/]+$"
                },
                {
                    "name": "current_owner",
                    "label": "Current Owner Name (as per 7/12)",
                    "type": "text",
                    "required": True,
                    "ocr_field": "name"
                },
                {
                    "name": "new_owner",
                    "label": "New Owner Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "mobile",
                    "label": "Mobile Number",
                    "type": "tel",
                    "required": True,
                    "validation": "^[6-9][0-9]{9}$"
                }
            ]
        },
        {
            "id": "edhara",
            "name": "e-Dhara Centers",
            "type": "government",
            "portal_url": "https://edhara.gujarat.gov.in",
            "name_change_url": "https://edhara.gujarat.gov.in",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": False,
            "direct_access": True,
            "automation_type": "assisted_service",
            "form_type": "center_service",
            "reality_check": "Assisted service (no personal login)",
            "form_fields": [
                {
                    "name": "district",
                    "label": "District",
                    "type": "select",
                    "required": True
                },
                {
                    "name": "taluka",
                    "label": "Taluka",
                    "type": "select",
                    "required": True
                },
                {
                    "name": "village",
                    "label": "Village",
                    "type": "select",
                    "required": True
                },
                {
                    "name": "survey_number",
                    "label": "Survey Number",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "current_owner",
                    "label": "Current Owner Name",
                    "type": "text",
                    "required": True,
                    "ocr_field": "name"
                },
                {
                    "name": "new_owner",
                    "label": "New Owner Name",
                    "type": "text",
                    "required": True
                },
                {
                    "name": "mobile",
                    "label": "Mobile Number",
                    "type": "tel",
                    "required": True,
                    "validation": "^[6-9][0-9]{9}$"
                }
            ]
        }
    ]
}

def update_services_data():
    """Update the services data file with direct access mapping"""
    
    # Read existing services data
    try:
        with open('/app/backend/app/data/services_data.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except:
        existing_data = {}
    
    # Update with direct access services
    updated_data = DIRECT_ACCESS_SERVICES.copy()
    
    # Save updated data
    output_file = '/app/backend/app/data/services_data_updated.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Updated services data saved to: {output_file}")
    
    # Print summary
    print("\n📋 DIRECT ACCESS SERVICES SUMMARY:")
    print("=" * 50)
    
    total_services = 0
    for category, services in updated_data.items():
        print(f"\n{category.upper()} ({len(services)} services):")
        for service in services:
            total_services += 1
            field_count = len(service.get('form_fields', []))
            automation_type = service.get('automation_type', 'unknown')
            print(f"  ✅ {service['name']} - {field_count} fields ({automation_type})")
 