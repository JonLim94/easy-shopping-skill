from mycroft import MycroftSkill, intent_file_handler, intent_handler
from adapt.intent import IntentBuilder
from mycroft.skills.context import removes_context
from mycroft.util import LOG
import time
import cv2
import os
import sys
from multiprocessing import Process, Queue
sys.path.append('/home/ai-user/mycroft-core/skills/easy-shopping-skill/cvAPI') # update path if necessary
from util import callAPI, encode_image_from_file
import getObjLabel, getDetail


def take_photo(img_queue):
    '''
    Do taking photo
    '''
    LOG.info(LOGSTR + 'take photo process start')
    cap = cv2.VideoCapture(0)
    img_name = 'cap_img_' + str(time.time()) + '.jpg'
    img_path = '/home/ai-user/Documents/' + img_name # Remember to update path to image

    #<-- Take photo in specific time duration -->
    cout = 0
    while True:
        ret, frame = cap.read()
        cv2.waitKey(1)
        cv2.imshow('capture', frame)
        cout += 1 
        if cout == 50:
            img_queue.put(img_path)
            cv2.imwrite(img_path, frame)
            break

    cap.release()
    cv2.destroyAllWindows()
    LOG.info(LOGSTR + 'take photo process end')
    os._exit(0)
    
    
def generate_str(possible_list):
    res = ''
    if len(possible_list) == 3:
        res = possible_list[0] + ' ' + \
           possible_list[1] + ' and ' + possible_list[2]
    elif len(possible_list) == 2:
        res = possible_list[0] + ' and ' + possible_list[1]
    elif len(possible_list) == 1:
        res = possible_list[0]

    return res
        

class EasyShopping(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)


# SRBP Workshop 2.1.1 Adapt Intent
    @intent_handler(IntentBuilder('ViewItemInHand').require('ViewItemInHandKeyWord'))
    def handle_view_item_in_hand(self, message):
        self.speak_dialog('take.photo')
        self.img_multi = ''
        self.img_hand = ''
    
        # suppose we use camera to take a photo here, 
        # then the function will return an image path
        self.img_hand = '/home/ai-user/mycroft-core/skills/test/2.jpeg'

        # suppose we call CV API here to get the result, 
        # the result will all be list, then we use generate_str() to create string
        self.category_str = generate_str(['milk', 'bottle', 'drink'])
        self.brand_str = generate_str(['Dutch Lady', 'Lady'])
        self.color_str = generate_str(['white', 'black', 'blue'])
        self.kw_str = ' '.join(['milk', 'bottle', 'protein', 'pure', 'farm'])

        # set the context
        self.set_context('getDetailContext')

        # speak dialog
        self.speak_dialog('item.category', {'category': self.category_str})

    def handle_ask_item_detail(self, detail, detail_str):
        if detail_str == '':
            # add expect_response
            self.speak_dialog('cannot.get', {'detail': detail}, expect_response=True) # This calls .dialog file.
        else:
            dialog_str = 'item.' + detail
            # add expect_response
            self.speak_dialog(dialog_str, {detail: detail_str}, expect_response=True) # This calls .dialog file.
            
    @intent_handler(IntentBuilder('AskItemCategory').require('Category').require('getDetailContext').build())
    def handle_ask_item_category(self, message):
        self.handle_ask_item_detail('category', self.category_str)
#        self.speak('I am talking about the category of the item')


    @intent_handler(IntentBuilder('AskItemColor').require('Color').require('getDetailContext').build())
    def handle_ask_item_color(self, message):
        self.handle_ask_item_detail('color', self.color_str)
#        self.speak('I am talking about the color of the item')

    @intent_handler(IntentBuilder('AskItemBrand').require('Brand').require('getDetailContext').build())
    def handle_ask_item_brand(self, message):
         self.handle_ask_item_detail('brand', self.brand_str)
#         self.handle_ask_item_detail('brand', self.brand_str)

    
    @intent_handler(IntentBuilder('AskItemKw').require('Kw').require('getDetailContext').build())
    def handle_ask_item_keywords(self, message):
        self.handle_ask_item_detail('keyword', self.kw_str)
#        self.speak('I am talking about the keywords of the item')


    @intent_handler(IntentBuilder('AskItemInfo').require('Info').require('getDetailContext').build())
    def handle_ask_item_complete_info(self, message):
        if self.color_str == '':
            self.handle_ask_item_detail('category', self.category_str)
        else:
            self.speak_dialog('item.complete.info', {
                          'category': self.category_str, 'color': self.color_str})
        self.handle_ask_item_detail('brand', self.brand_str)
        self.handle_ask_item_detail('keyword', self.kw_str)        
#        self.speak('I am speaking the complete information of the item')


#    @intenthandler('puchase.history.intent')
#    def handle_purchase_history(self, message):
#        purchase_history = pd.read.csv('purchase_history.txt', header=None)
#        history_req = self.ask_yesno('purchase.history') # This calls .dialog file.
#        if history_req == 'yes' and purchase_history != []:
#            self.speak('Yes, you have bought this item before')

#	elif history_req == 'yes' and purchase_history == []:
#	    self.speak('No, you have not bought this item before')

#        elif history_req == 'no':
#            self.speak('OK noted.')

#        else:
#            self.speak('I cannot understand what you are saying')
        

    @intent_handler(IntentBuilder('NoContext').one_of('Category', 'Color', 'Brand', 'Kw', 'Info'))
    def handle_no_context2(self, message):
        self.speak('Please let me have a look at what\'s in your hand first.')
        

    @intent_handler(IntentBuilder('FinishOneItem').require('Finish').require('getDetailContext').build())
    @removes_context('getDetailContext')
    def handle_finish_current_item(self, message):
        self.speak('Got your request. Let\'s continue shopping!')
        with open('purchase_history.txt', 'a') as history:
            history.write('new item')
        
        self.types_str = ''
        self.color_str = ''
        self.logo_str = ''
        self.kw_str = ''
        self.img_hand = ''
        self.img_multi = ''


# SRBP Workshop 2.1.1 Padatious Intent
#    LOGSTR = '********************====================########## '
# Edit in main class: class EasyShopping(MycroftSkill):
#    def __init__(self):
#        MycroftSkill.__init__(self)
#        self.category_str = ''
#        self.color_str = ''
#        self.brand_str = ''
#        self.kw_str = ''
#        self.img_multi = ''
#        self.img_hand = ''
#        self.log.info(LOGSTR + "_init_ EasyShoppingSkill")


#    @intent_handler('view.goods.intent')
#    def handle_view_goods(self, message):
#        self.speak_dialog('take.photo')
#        self.img_multi = ''
#        self.img_hand = ''

    # step 1.2: create another process to do the photo taking
#        img_queue = Queue()
#        take_photo_process = Process(target=take_photo, args=(img_queue,))
#        take_photo_process.daemon = True
#        take_photo_process.start()
#        take_photo_process.join()
#        self.img_multi = img_queue.get()

#        self.speak('I find some goods here, you can ask me whatever goods you want.', expect_response=True)

    # suppose we use camera to take a photo here, 
    # then the function will return an image path
#    self.img_multi = '/home/ai-user/mycroft-core/skills//test/multi.jpeg'

#    self.speak('I find some goods here, you can ask me whatever goods you want.')


#    @intent_handler('is.there.any.goods.intent')
#    def handle_is_there_any_goods(self, message):
#        if self.img_multi == '':
#            self.handle_no_context1(message)
#        else:
            # use try-catch block here, since there maybe error return from the cv api
#            try:        
#                self.log.info(LOGSTR + 'actual img path')
#                self.log.info(self.img_multi)
#                if MODE == 'TEST':
#                    self.log.info(LOGSTR + 'testing mode, use another image')
#                    self.img_multi = 'P/home/ai-user/mycroft-core/skills/test/multi.jpeg' # e.g. self.img_multi = '/home/ai-user/mycroft-core/skills/easy-shopping-skill/cvAPI/test/photo/multi.jpeg'

 #               objectlist = getObjLabel.getObjectsThenLabel(self.img_multi)
 #               label_list = []
 #               loc_list = []
 #               detected = 0

 #               category_label = message.data.get('category')
    
#                for obj in objectlist['objectList']:
#                    label_list.append(obj['name'])
#                    loc_list.append(obj['loc'])
            
        
#                for i in range(0,len(label_list)):
#                    label_str = generate_str(label_list[i])
#                    label_str = label_str.lower()
            
#                    if category_label is not None:
#                        if category_label in label_str:
#                            self.speak_dialog('yes.goods',
#                                        {'category': category_label,
 #                                       'location': loc_list[i]})
 #                           detected = 1
 #                           break
#                    else:
#                        continue
    
#                if detected == 0:
#                    self.speak_dialog('no.goods',
#                    {'category': category_label})

#            except Exception as e:
#                self.log.error((LOGSTR + "Error: {0}").format(e))
#                self.speak_dialog(
#                "exception", {"action": "calling computer vision API"})


# firstly create do.you.want.to.take.a.photo.dialog 
#    def handle_no_context1(self, message):
#        self.speak('Please let me have a look at what\'s in front of you first.')
#        # add prompts
#        take_photo = self.ask_yesno('do.you.want.to.take.a.photo') # This calls .dialog file.
#        if take_photo == 'yes':
#            self.handle_view_goods(message)
#        elif take_photo == 'no':
#            self.speak('OK. I won\'t take photo')
#        else:
#            self.speak('I cannot understand what you are saying')

    
def create_skill():
    return EasyShopping()

