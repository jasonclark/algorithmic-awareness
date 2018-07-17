#!/usr/bin/python3
#program the library

goals = ['food', 'research', 'testing', 'socializing']

def action (goals, methods):
  if goals = 'food' :
    location = 'coffee shop'
  else :
    location = 'vending machine'
  elif goals = 'research' :
    location = 'reference desk'
    methods = ['text', 'email', 'askQuestion']
      if methods = 'text' :
        print("Text 34455")
      elif methods = 'email' :
        print("Email asklibrary@montana.edu")
      else :
        print("Speak to librarian in front of you.")
  elif goals = 'testing' : 
    location = 'Basement'
  else :
    location = '2nd floor, where the party 🎉  is!'
  return

#run the library action function with values
action (goals='research', methods='email')
