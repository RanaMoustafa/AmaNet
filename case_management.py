import random
from datetime import datetime
import json
def Sign_in():
    print("   Authorized Personal Login     ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")        
    national_id = input("Enter your national ID: ")
    
    print(" Login Successful! Welcome user :" , username)
    return username, password, national_id  

class Case:
    def __init__(self,victim_name,victim_phone,case_type):
        self.case_id=random.randint(1000,9999)
        self.victim_name=victim_name
        self.victim_phone=victim_phone
        self.case_type=case_type
        self.case_status="New"
        self.created_at=datetime.now()
    def display_case(self):
        print("Case ID:",self.case_id)
        print("Vicim Name:",self.victim_name)
        print("Victim Phone:",self.victim_phone)  
        print("Case Type:",self.case_type)  
        print("Case Status:",self.case_status)
        print("Created At:",self.created_at)
    def to_dict(self):
        return {
            "case_id":self.case_id,
            "victim_name":self.victim_name,
            "victim_phone":self.victim_phone,
            "case_type":self.case_type,
            "case_status":self.case_status,
            "created_at":str(self.created_at)
        }  


def save_cases(cases):
    info=[]

    for case in cases:
        info.append(case.to_dict())
    file=open("cases.json","w")
    json.dump(info,file,indent=4)
    file.close()
def load_cases():
    file=open("cases.json","r")
    data=json.load(file)
    file.close()
    return data

def collect_case_type():                     
    print("\n--- Available Case Types ---")
    print("1. Financial Blackmail ")
    print("2. Emotional/Photo Blackmail ")
    print("3. Electronic Harassment ")
    print("4. Identity Theft ")
    print("5. Other ")
    
    while True:
        type_choice = input("Select Case Type (1-5): ").strip()
        if type_choice == '1':
            return "Financial Blackmail"
        elif type_choice == '2':
            return "Emotional/Photo Blackmail"
        elif type_choice == '3':
            return "Electronic Harassment"
        elif type_choice == '4':
            return "Identity Theft"
        elif type_choice == '5':
            return input("Enter you case :")
        else:
            print(" [!] Invalid choice. Please enter a number from 1 to 5 ")