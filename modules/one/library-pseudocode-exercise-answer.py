Program Library();

goal (food, research, testing, socializing);

action {
  if goal = food {
    location = "coffee shop";
  } else {
    location = "vending machine"
  }
  elseif goal = research {
    location = "reference desk";
    methods (text, email, askQuestion)
      if { method = "text" {
        print("text 34455");
      } elseif method = "email"
        print("email asklibrary@montana.edu");
      } else {
        print("speak to librarian in front of you.");
      }
  } elseif goal = "testing" 
    location = "Basement";
  } else {
    location = "2nd floor"
  }
}


Run Library();