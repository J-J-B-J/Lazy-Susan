#The time library is used to wait in between long chunks of text
from time import sleep

#Libraries by AIY that allow speech-to-text,
#LED control, text-to-speech and GPIO pin control
from aiy.cloudspeech import CloudSpeechClient
import aiy.leds
import aiy.voice.tts
from gpiozero import Motor

current_position = 0    #Set the # of degrees the table has turned = 0

#This dictionary keeps track of people and their positions around the table
modifiers = {
    "A": 0,
    "B": 90,
    "C": 180,
    "D": 270,
    }

#The modifier is used when the table needs to turn to face an item to a person.
#Each person has a modifier that is added to the current position to calculate
#how much to turn.
modifier = 0

objects = {}    #Contains the objects and their identifiers that are on the table.
all_objects = {}    #Contains all the objects and their identifiers.


def say(text):  #This function gets the speaker to say what is entered
    aiy.voice.tts.say(text, lang='en-AU', volume=60, pitch=130, speed=100,
                      device='default')

def getInput(prompt, hints):    #This function gets a spoken user input
    say(prompt) #Speak the prompt
    return CloudSpeechClient().recognize(language_code=en_AU,
                                         hint_phrases=hints)    #Get the input

#This function prints out all the objects in turn
#It's used when a change to the objects dictionary occurs
def list_items_on_table():
    say("Updated items on table.")  #Say what is said below
    for obj, identifier in objects.items(): #For each obj & id in objects
        say(obj + ".")  #Print name of object in bullet point format

def print_current_position(): #This function prints table's current position
    say("Table position " + str(current_position) + ".")
print_current_position()    #Run the above function upon program run

def get_modifier(): #This function returns the modifier for the specified user
    global modifier
    modifier = "X"  #So that if the input isn't existing, the program will know
    person = "" #Create the variable person outside of the while loop scope
    person = getInput("What seat?", modifiers.keys())    #Set person to user input
    for p, m in modifiers.items():
        if person == p:
            modifier = m
    if modifier == "X":
        say("That seat does not exist.")
    return modifier #Return the modifier once the user has given a valid answer






#This class is for real-world objects that can be placed on the lazy susan
class table_object:
    def __init__(self, name, pos, use):
        #Name, Position on table, Currently on table?
        self.name = name
        self.position = pos
        self.use = use
        
        #Add this object to the all_objects dictionary
        all_objects[self.name] = self

    #Goto turns table so that the chosen item is facing the chosen person
    def goto(self, modifier):
        global current_position #So that goto can change that table's position
        say("Going to " + self.name + ".")    #Say where the table should go
        time.sleep(1)

        turn = (self.position + modifier) - current_position    #Calculate turn
        current_position = (current_position + turn) % 360  #Update pos var

        #The following converts turns greater than 180 into negative numbers
        #E.g. 260 turn becomes -100 turn
        if(turn > 180):
            turn = (360 - turn) * -1
            
        if(turn < 0):
            #Print the turn as anticlockwise
            say("The table turned " + str(turn*-1) + " anticlockwise.")
        if(turn > 0):
            #Print the turn as clockwise
            say("The table turned " + str(turn) + " clockwise.")
        if(turn == 0):  #i.e. table is already in correct position
            say("The table did not move.")    #Print the turn as nothing
        print_current_position()    #Show the table's updated position

    def used(self): #This function enables the item
        self.use = True #Enable in object
        objects[self.name] = self   #Enable in objects dictionary
        list_items_on_table()   #Print updated table items
        
    def unused(self):   #This function disables the item
        self.use = False    #Disable in object
        del objects[self.name]  #Disable in objects dictionary
        list_items_on_table()   #Print updated table items

    def check_if_used(self):   #Checks weather or not the item is enabled
        return self.use == True





#These are the objects that can be enabled:
cutlery = table_object("Cutlery", 0, False)
tom_sauce = table_object("Tomato Sauce", 0, False)
bbq_sauce = table_object("BBQ Sauce", 0, False)
chilli_sauce = table_object("Sweet Chilli Sauce", 0, False)
salad = table_object("Salad", 0, False)
salt = table_object("Salt", 0, False)
pepper = table_object("Pepper", 0, False)
bible = table_object("Bible", 0, False)
olive_oil = table_object("Olive Oil", 0, False)





while True:
    board.button.wait_for_press()
    action = getInput("Enter action: ", ("Goto", "Edit"))   #Ask what the user wants to do

    
    if action == "Goto":    #If the user wants to turn the table:
        miodifier = get_modifier()  #Get the modifier for a specific person
        goto = getInput("Where to? ", objects.keys())  #Ask what item the person wants
        valid_answer_found = False  #The user hasn't yet provided valid answer
        for obj, identifier in objects.items(): #Repeat w all objects on table
            #If the item the user entered matches a table object
            if str(obj) == goto:
                identifier.goto(modifier)   #Turn table to the table object
                valid_answer_found = True
        if valid_answer_found == False:
            say("You can't go to that item now.")   #Give an error


    elif action == "Edit":  #If the user wants to change the items on the table
        edit = getInput("Item to Toggle? ", all_objects.keys())   #Ask for item

        #Check the existance of the item (it's presence in all_objects)
        item_exists = False #Haven't found the item yet
        for obj, identifier in all_objects.items(): #Repeat with all items
            if str(obj) == edit:    #If item in all_objects matches user input
                edit_identifier = identifier    #Store the ID of the object
                item_exists = True  #The item the user asked for exists
        if item_exists == False:
            say("The item you asked for dosen't exist.")

        #Toggle the item the user entered
        if edit_identifier.check_if_used() == True:   #If the item is enabled
            edit_identifier.unused()    #Disable the item
        else:   #If the item is disabled
            edit_identifier.used()  #Enable the item

    else:   #If the action provided isn't valid
        say("The action you entered wasn't valid")


