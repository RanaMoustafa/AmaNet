threat_type=[
    ("direct_threat","Is there a direct threat of physical harm?"),
    ("private_content","Are private photos or videos being used to threaten you?"),
    ("repeated_threat","Has the threat been repeated multiple times?"),
    ("personal_info", "Does the extortionist know personal information like your address or workplace?"),
    ("financial_demand", "Is the extortionist demanding money or illegal favors?")
]


Risk_Scores = {
    "direct_threat": 3,
    "private_content": 3,
    "repeated_threat": 2,
    "personal_info": 2,
    "financial_demand": 2
}


def calculate_risk_score(answers_dict):
    total_score = 0
    for key in answers_dict:
        if answers_dict[key] == True:
            total_score = total_score + Risk_Scores[key]
    return total_score


def get_risk_level(score):
    if score >= 8:
        return "Critical"
    elif score >= 5:
        return "High"
    elif score >= 3:
        return "Medium"
    else:
        return "Low"

    
def run_risk_assessment():
    print("--- Starting Risk Assessment ---")
    user_answers = {}

    for item in threat_type:
        key = item[0]
        question_text = item[1]
        answer = input(question_text + " (Yes/No): ")
        if answer.strip().lower() in ["yes"]:
           user_answers[key] = True
        else:
           user_answers[key] = False

    risk_score = calculate_risk_score(user_answers)
    risk_level = get_risk_level(risk_score)
    result = {
        "risk_score": risk_score,
        "risk_level": risk_level
    }
        
    print("--- Assessment Result ---")
    print("Total Score:",risk_score)
    print("Risk Level:",risk_level)
    
    return result
