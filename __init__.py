from mycroft import MycroftSkill, intent_file_handler, intent_handler
from adapt.intent import IntentBuilder

class EasyShopping(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

#    @intent_handler(IntentBuilder('FAQ.Adapt.intent').require('FAQ').require('ESA').build())
#    def handle_shopping_easy(self, message):
#        self.speak_dialog('shopping.easy')
	
    @intent_handler('FAQ.Adapt.intent')
    def handle_FAQ_Adapt(self, message):
    	self.speak('Hello ESA!')
 
    
    	    	
    @intent_handler('is.there.any.goods.intent')
    def handle_is_there_any_goods(self, message):
        category_label = message.data.get('cat')
        str = 'yes, I find ' +  category_label + ' is a skill which analyzes the photo taken by the user and then replies with the detected goods in the photos.'
        self.speak(str)
     	

    @intent_handler('FAQ.Padatious.intent')
    def handle_shopping_easy_padatious(self, message):
    	ESA_label = message.data.get('cat_ESA')
    	reply = str(ESA_label) + " is a skill which analyzes the photo taken by the user and then replies with the detected goods in the photos."
    	self.speak(reply)
   

def create_skill():
    return EasyShopping()

