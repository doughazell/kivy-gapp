from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.uix.carousel import Carousel

# 8/9/17 DH: Changing button text and sleeping prior to reverting it
import time

# 2/11/17 DH: Adding Google Sheets
import gspread

import sys
from kivy.logger import Logger
Logger.info('DH:'+str(sys.version))

from oauth2client.service_account import ServiceAccountCredentials

red = [1,0,0,1]
green = [0,1,0,1]
blue =  [0,0,1,1]
purple = [1,0,1,1]

def populateCarousel(self):
    # 20/2/18 DH: Just starting to refactor the hack...XP, all the way...
    try:
        # 2/11/17 DH:
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

        self.sheet = client.open("Addresses").worksheet("Personal")

        list_of_dicts = self.sheet.get_all_records()
        record_num = len(list_of_dicts)
        self.lbl1.text = str(record_num) + ' records'

        for idx in range(0,record_num):
            lbl = Label()
            values = self.sheet.row_values(idx+2)
            if values:
                for i in range(5):
                    value = values.pop(2)
                    lbl.text += value + '\n'
                #print "Adding: " + lbl.text
                self.add_widget(lbl)

    except AttributeError:
        self.lbl1.text = str(sys.exc_info()[1])

    except:
        self.lbl1.text='Error with Google Sheets!'


#class RootWidget(BoxLayout):
#class RootWidget(GridLayout):
class RootWidget(Carousel):

    def __init__(self, **kwargs):

        super(RootWidget, self).__init__(**kwargs)

        # ---------------------- NUI Functionality -----------------------
        btn1 = Button(text='btn 1')
        # 17/6/17 DH: https://kivy.org/docs/api-kivy.uix.behaviors.button.html
        #   so 'on_press' rather than 'on_pressed' as alluded to in https://kivy.org/docs/guide/events.html
        btn1.bind(on_press=self.btn1_pressed)
        btn1.bind(on_release=self.btn1_released)
        self.btn1=btn1

        cb = CustomBtn()
        # 19/8/17 DH: Testing override of 'on_pressed'
        #cb.bind(mypressed=self.btn_pressed)
        cb.bind(pressed=self.cstbtn_pressed)

        btn2 = Button(text='btn 2')
        btn2.bind(on_press=self.btn2_pressed)
        btn2.bind(on_release=self.btn2_released)

        # ---------------------- NUI Layout ----------------------
        layout1 = BoxLayout(spacing=10, size_hint_y=None, height=50)
        lbl1 = Label(text='Yea baby...!', color=red)
        self.lbl1 = lbl1
        layout1.add_widget(lbl1)

        layout2 = BoxLayout(spacing=10)
        layout2.add_widget(btn1)
        layout2.add_widget(cb)
        layout2.add_widget(btn2)

        # 24/2/18 DH: GridLayout
        grid = GridLayout(rows=2)
        grid.add_widget(layout1)
        grid.add_widget(layout2)

        # 24/2/18 DH: Carousel
        self.direction='right'

        # 24/2/18 DH: Initially add the start screen then add the table rows later
        self.add_widget(grid)

        populateCarousel(self)

    def cstbtn_pressed(self, instance, pos):
        #print ('pos: printed from root widget: {pos}'.format(pos=pos))
        self.btn1.text='pos: {pos}'.format(pos=pos)

    def btn1_pressed(self, instance):
        #print ('yay...:)')

        instance.text="Hey totally...3"
        #time.sleep(1)
        #print ('yay2...:)')

    def btn1_released(self, instance):
        instance.text="btn 1"

    '''
    def btn2_pressed(self, instance):
        instance.text="Google Sheets coming...:)"

    '''
    def btn2_pressed(self, instance):
        try:
            list_of_dicts = self.sheet.get_all_records()
            record_num = len(list_of_dicts)
            instance.text = str(record_num) + ' records'

        except AttributeError:
            instance.text = str(sys.exc_info()[1])
        except:
            instance.text = str(sys.exc_info()[0])

    def btn2_released(self, instance):
        instance.text="Totally Google Sheets...:)"


class CustomBtn(Widget):

    # 19/8/17 DH: Testing override of 'on_pressed'
    #mypressed = ListProperty([0, 0])
    pressed = ListProperty([0, 0])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # 19/8/17 DH: Testing override of 'on_pressed'
            #self.mypressed = touch.pos
            self.pressed = touch.pos
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return True
        return super(CustomBtn, self).on_touch_down(touch)

    '''
    https://kivy.org/docs/guide/events.html
    "We define the pressed Property of type ListProperty, giving it a default value of [0, 0].
     From this point forward, the on_pressed event will be called whenever the value of this property is changed."

    It is just "on" a change to the Kivy Property class assigned to the variable defined in class CustomBtn
    (hence still works with 'mypressed' rather than the event connection of 'pressed')
    https://kivy.org/docs/api-kivy.properties.html#observe-using-on-propname

    'self'     is current class
    'instance' is property class
    'pos'      is list value
    '''

    # 19/8/17 DH: Testing override of 'on_pressed'
    # 9/9/17 DH: Needs to have same suffix as property assigned to 'touch.pos' in 'CustomBtn.on_touch_down'
    #            (as mentioned in multi-line comments above...!)
    #            [This GUI programming is feeling like learning Java in the 2nd semester of my MSc in 1999...
    #             ...when there was real hope for the future...]
    #def on_mypressed(self, instance, pos):
    def on_pressed(self, instance, pos):
        print ('pressed at {pos}'.format(pos=pos))

class TestApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    TestApp().run()
