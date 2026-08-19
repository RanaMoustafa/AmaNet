import arabic_reshaper
from bidi.algorithm import get_display
from datetime import datetime,date

def generate_report(case_obj, risk_data, extorter_data, list_evidence, gov_name, gov_details):
    print("--- Generating Official Police Report ---")
    now = datetime.now()
    report_time = now.time()
    report_date=date.today()

    def fix_arabic(text):
       reshaped_text = arabic_reshaper.reshape(text)
       bidi_text = get_display(reshaped_text)
       return bidi_text
    directorate_fixed = fix_arabic(gov_details['directorate'])
    address_fixed = fix_arabic(gov_details['address'])    
    
    
    evidence_str = ""
    if len(list_evidence) > 0:
        counter = 1
        for ev in list_evidence:
            evidence_str += f"{counter} _Type: { ev['type_evidence']} |Description : {ev['description'] } |File : {ev['file_path'] }\n"
            counter = counter + 1
    else:
        evidence_str = "No evidence attached.\n"
    
    
    report_content = f"""
====================================================
            Aman - OFFICIAL INCIDENT REPORT
====================================================
Date of Report: {report_date}
Time of Report:{report_time}

[ CASE DETAILS ]
Case ID       : {case_obj.case_id}
Victim Name   : {case_obj.victim_name}
Victim Phone  : {case_obj.victim_phone}
Case Type     : {case_obj.case_type}
Current Status: {case_obj.case_status}

[ EXTORTER INFORMATION ]
Phone Number  : {extorter_data.get('phone_extorter', 'Not Found')}
Profile Link  : {extorter_data.get('link_profile_extorter', 'Not Found')}

[ RISK ASSESSMENT ]
Risk Level    : {risk_data['risk_level']}
Risk Score    : {risk_data['risk_score']} / 12

[ EVIDENCE COLLECTED ]
{evidence_str}
[ OFFICIAL DISPATCH LOCATION ]
Governorate   : {gov_name}
Directorate   : {directorate_fixed}
Address       : {address_fixed}
Hotline       : {gov_details['hotline']}
Landline      : {gov_details['phone']}
WhatsApp      : {gov_details['whatsapp']}
====================================================
"""
    print(report_content)


    filename = "Police_Report_" + str(case_obj.case_id) + ".txt"  
    
    with open(filename, "w",encoding="utf-8") as file:
        file.write(report_content)
    
    print("Report saved successfully as: " + filename + "\n")


def submit_report_simulation():
   
    print("--- Starting Submission Process ---")
    
    input("Press Enter to prepare report data...")
    print("Preparing Report Data... Done!\n")
    
    input("Press Enter to encrypt evidence files...")
    print("Encrypting Evidence Files... Done!\n")
    
    input("Press Enter to connect to Secure Police Server...")
    print("Connecting to Secure Police Server... Done!\n")
    
    input("Press Enter to dispatch report...")
    print("Dispatching Report... Done!\n")
    
    print("Report Submitted Successfully!")


def show_emergency_guideLines():
    print("\n==================================================")
    print("         IMPORTANT SAFETY GUIDELINES        ")
    print("==================================================")
    print("1. DO NOT pay any money to the extorter. (It will not stop them).")
    print("2. DO NOT delete any chats, photos, or voice notes (They are your evidence).")
    print("3. Block the extorter immediately from all your accounts.")
    print("4. Inform your trusted family members or friends for support.")
    print("\nIf you are in immediate danger, please contact:")
    print("Website: https://moi.gov.eg/")
    print("Hotline: 108")

