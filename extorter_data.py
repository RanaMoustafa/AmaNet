def collect_extorter_data():
  print("\n--- Extorter Data ---")
  extorter_name = input("Enter extorter name : ")
  extorter_phone = input("Enter extorter's phone number: ")
  extorter_profile_link = input("Enter extorter's profile link: ")

  extorter_data ={
    "extorter_name": extorter_name,
    "extorter_phone": extorter_phone,                                            
    "extorter_profile_link": extorter_profile_link
   
    }
  return  extorter_data


