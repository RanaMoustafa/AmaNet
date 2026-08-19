from case_management import Case, save_cases, collect_case_type,Sign_in
from risk_assessment import run_risk_assessment
from extorter_data import collect_extorter_data
from evidence_data import collect_evidence
from location_data import get_final_location
from report import generate_report, submit_report_simulation, show_emergency_guideLines

def main():
    print("==================================================")
    print("          Welcome to Aman Police System           ")
    print("==================================================")
    username, password, national_id = Sign_in()
   
    print("\n[STEP 1] Enter Victim Details:")
    v_name = input("Enter Victim Name: ")
    v_phone = input("Enter Victim Phone: ")
    c_type = collect_case_type()
    my_case = Case(v_name, v_phone, c_type)
    cases_list = [my_case]

   
    print("\n[STEP 2] Risk Assessment:")
    risk_result = run_risk_assessment()

    
    print("\n[STEP 3] Extorter & Evidence Information:")
    extorter = collect_extorter_data()
    evidence_list = collect_evidence()
    gov_name, gov_details = get_final_location()

   
    print("\n[STEP 4] Report Generation:")
    generate_report(my_case, risk_result, extorter, evidence_list, gov_name, gov_details)
    submit_report_simulation()
    show_emergency_guideLines()

    save_cases(cases_list)
    print("\n[Done] System Closed. All data saved securely.")

if __name__ == "__main__":
    main()