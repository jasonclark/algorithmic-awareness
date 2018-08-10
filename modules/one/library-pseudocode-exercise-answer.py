# !/usr/bin/python3
# in this program, we are encoding a person's options navigating the library

goals = ['food', 'research', 'testing', 'socializing']
actions = ['speak', 'text', 'email', 'walk']

def navigate_library(goals, actions=0):
    if goals == 'food' and actions == 0:
        location = 'coffee shop'
	message = "Have some coffee coffee, buzz buzz..."
    elif goals == 'research':
        location = 'reference desk'
        if actions == 'text':
            message = "Text a librarian at 34455."
        elif actions == 'email':
            message = "Email asklibrary@montana.edu."
        else:
            message = "Speak to librarian in front of you."
    elif goals == 'testing' and actions == 0:
        location = 'Basement'
	message = "Bummer. You need to take a test."
    else:
        location = '2nd floor'
	message = "It's where the party is!"
    return location
    return message

# run the library navigation function with values
navigate_library(goals='research', actions='text')
#print "Your library goal was " + goals + "."
#print "You are at the " + location + ". " + message

