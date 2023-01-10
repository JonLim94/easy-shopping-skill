from mycroft import MycroftSkill, intent_file_handler, intent_handler
from adapt.intent import IntentBuilder

class EasyShopping(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)


# SRBP Workshop 1.3.2 Adapt Intent Parser
#    @intent_handler(IntentBuilder('FAQ.Adapt.intent').require('FAQ').require('ESA').build())
#    def handle_shopping_easy(self, message):
#        self.speak_dialog('shopping.easy')



# SRBP Workshop 1.3.2 Padatious Intent Parser	
    @intent_handler('FAQ.Adapt.intent')
    def handle_FAQ_Adapt(self, message):
    	self.speak('Hello ESA!')
 
    	    	
    @intent_handler('FAQ.Padatious.intent')
    def handle_FAQ_Padatious(self, message):
        category_label = message.data.get('cat')
        str = category_label + ' is a skill which analyzes the photo taken by the user and then replies with the detected goods in the photos.'
        self.speak(str)
     	
   
def create_skill():
    return EasyShopping()

