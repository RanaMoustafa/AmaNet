from datetime import datetime

list_evidence = []


evidence_types = [
    "Screenshot",
    "Message",
    "File",
    "Video",
    "Audio",
    "Link",
    "Other"
]


def evidence_validate(type_evidence):
    for evidence_type in evidence_types:
        if type_evidence.lower() == evidence_type.lower():
            return True

    return False

def add_evidence():

    while True:
        print(" Evidence Types: ")
        print("1: Screenshot")
        print("2: Message")
        print("3: File")
        print("4: Video")
        print("5: Audio")
        print("6: Link")
        print("7: Other")

        type_evidence = input("Enter evidence type: ")

        if evidence_validate(type_evidence):
            break

        print("Invalid evidence type. Please try again.")

    description = input("Enter evidence description: ")

    file_path = input("Enter evidence file path (or leave empty): ")
        

    evidence_time = datetime.now()



    evidence = {
        "type_evidence": type_evidence,
        "description": description,
        "file_path": file_path,
        "evidence_time": evidence_time
    }

    list_evidence.append(evidence)
    print("Evidence added successfully.")

def collect_evidence():
  
    while True:
        add_evidence() 
        add_more = input("Do you want to add another evidence? (Yes/No): ")
        if add_more.lower() == "no":
            break
    return list_evidence


