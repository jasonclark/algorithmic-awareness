Program Library();

goal (ADD-YOUR-GOALS-AS-A-COMMA-SEPARATED-LIST-HERE);

action {
  if goal = ADD-ONE-OF-YOUR-GOALS-HERE {
    location = "ADD-A-POTENTIAL-LOCATION-FOR-GOAL-HERE";
  } else {
    location = "ADD-A-POTENTIAL-LOCATION-FOR-GOAL-HERE"
  }
  elseif goal = ADD-ONE-OF-YOUR-COMPLEX-GOALS-HERE {
    location = "ADD-A-POTENTIAL-LOCATION-FOR-GOAL-HERE";
    methods (ADD-YOUR-COMPLEX-METHODS-AS-A-COMMA-SEPARATED-LIST-HERE)
      if { method = "ADD-ONE-OF-YOUR-METHODS-HERE" {
        print("ADD-ONE-OF-YOUR-METHOD-RESULTS-HERE");
      } elseif method = "ADD-ONE-OF-YOUR-METHODS-HERE"
        print("ADD-ONE-OF-YOUR-METHOD-RESULTS-HERE");
      } else {
        print("ADD-YOUR-FINAL-METHOD-RESULT-HERE");
      }
  } elseif goal = "ADD-ONE-OF-YOUR=GOALS-HERE" 
    location = "ADD-A-POTENTIAL-LOCATION-FOR-GOAL-HERE";
  } else {
    location = "ADD-A-POTENTIAL-LOCATION-FOR-GOAL-HERE"
  }
}


Run Library();
