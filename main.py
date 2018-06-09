from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.uix.carousel import Carousel
from kivy.uix.textinput import TextInput

# 8/9/17 DH: Changing button text and sleeping prior to reverting it
import time

# 2/11/17 DH: Adding Google Sheets
import gspread

import sys
from kivy.logger import Logger
Logger.info('DH:'+str(sys.version))

from oauth2client.service_account import ServiceAccountCredentials

#from kivy.config import Config
#Config.set('graphics', 'width', '1440')
#Config.set('graphics', 'height', '2560')

red = [1,0,0,1]
green = [0,1,0,1]
blue =  [0,0,1,1]
purple = [1,0,1,1]

# 8/6/18 DH: Populate lookup for Col ID's
def getSheetHeadings(self):
    # 31/5/18 DH: Such a sweeeet python built-in function...filter()...:)

    print 'REQUEST TO DB for row 1 (ie headings)'
    headings = filter(None, self.sheet.row_values(1))

    lastCol = len(headings)
    print 'Last col: ' + str(lastCol)

    self.orderCell = [1,lastCol]

    print 'REQUEST TO DB for cell ' + str(self.orderCell[0]) + ',' + str(self.orderCell[1])
    order = self.sheet.cell(self.orderCell[0], self.orderCell[1])

    print('Col order: ' + order.value)
    self.txt1.text = order.value

    # The last col heading contains the last used field display order
    self.lbl2.text = ''
    for col in range(1,lastCol):

        print 'REQUEST TO DB for cell 1,' + str(col)
        heading = self.sheet.cell(1,col)

        print ('Col ' + str(col) + ' = ' + heading.value)

        self.lbl2.text += str(col) + ' = ' + heading.value + '\n'

def getHeadings(self):
    '''
    print self.list_of_dicts

    print '-----------------------------'
    keyList = sorted(self.list_of_dicts[0].keys())
    print keyList
    print keyList[0]
    print '-----------------------------'
    '''

    print 'REQUEST TO DB for row 1 (ie headings)'
    headings = filter(None, self.sheet.row_values(1))

    order = headings.pop()
    print 'Order: ' + order
    self.txt1.text = order

    self.lbl2.text = ''
    self.hdsIndexed = {}
    col = 1
    for heading in headings:
        self.hdsIndexed[col] = heading
        #print ('Col ' + str(col) + ' = ' + heading)

        self.lbl2.text += str(col) + ' = ' + heading + '\n'
        col += 1
    #print self.hdsIndexed

def populateCarousel(self):
    # 20/2/18 DH: Just starting to refactor the hack...XP, all the way...
    try:
        # 2/11/17 DH:
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

        print 'Opening \'Addresses:Personal\'...'
        self.sheet = client.open("Addresses").worksheet("Personal")

        print 'REQUEST TO DB for all records'
        self.list_of_dicts = self.sheet.get_all_records(head=1)

        self.record_num = len(self.list_of_dicts)
        self.lbl1.text = str(self.record_num) + ' records'

        # 31/5/18 DH:Now dynamically getting table headings + display order
        #getSheetHeadings(self)
        getHeadings(self)

        # 29/5/18 DH: Create empty array for label slides to removed on repopulateCarousel()
        self.labels = []

        cols = self.txt1.text.split(",")
        # === Rows ===
        for idx in range(0,self.record_num):
            lbl = Label()

            #print 'REQUEST TO DB for row ' + str(idx+2)
            #values = self.sheet.row_values(idx+2)

            values = self.list_of_dicts[idx]

            if values:
                # ||| Cols |||

                # 22/3/18 DH: Selected cols added as specified in TextInput 'txt1'
                #colsIndexed = dict(zip(range(1,8), values))

                #print '-----------------------------'
                #print values
                #print self.hdsIndexed

                for col in cols:
                    #ROW: values = self.list_of_dicts[idx]
                    #COL HEADINGS: self.hdsIndexed
                    #print str(col) + ' = ' + self.hdsIndexed.get(int(col)) + ' = ' + values.get(self.hdsIndexed.get(int(col)))
                    #print '-----------------------------'

                    #lbl.text += colsIndexed.get(int(col)) + '\n'
                    lbl.text += values.get(self.hdsIndexed.get(int(col))) + '\n'

                # Add record to carousel
                #print "Adding: " + lbl.text
                self.add_widget(lbl)

                self.labels.append(lbl)

    except AttributeError:
        self.lbl1.text = str(sys.exc_info()[1])

    except:
        self.lbl1.text='Error with Google Sheets!'
        # 29/5/18 DH: Debug only
        #raise


class RootWidget(Carousel):

    def __init__(self, **kwargs):

        super(RootWidget, self).__init__(**kwargs)

        # 14/4/18 DH: Shift to kv file
        btn1 = ObjectProperty(None)

        # 21/5/18 DH: next step to shift...
        txt1 = ObjectProperty(None)
        lbl1 = ObjectProperty(None)
        # 30/5/18 DH: Adding a bit more UX (User Experience)
        lbl2 = ObjectProperty(None)

        # 24/2/18 DH: Carousel
        self.direction='right'

        populateCarousel(self)

    def repopulateCarousel(self):
        try:
            #self.clear_widgets()
            labelsNew = []

            cols = self.txt1.text.split(",")
            for idx in range(0,self.record_num):
                #print self.colsDictDB[idx]
                self.remove_widget(self.labels[idx])

                lbl = Label()

                values = self.list_of_dicts[idx]

                for col in cols:
                    try:
                        #populateCarousel():
                        # ROW: values = self.list_of_dicts[idx]
                        # COL HEADINGS: self.hdsIndexed
                        # lbl.text += values.get(self.hdsIndexed.get(int(col))) + '\n'

                        # --- Orig ---
                        #print('Recol: ' + col + '= ' + self.colsDictDB[idx].get(int(col)) )
                        #lbl.text += self.colsDictDB[idx].get(int(col)) + '\n'
                        # ------------
                        #print('Recol: ' + col + '= ' + values.get(self.hdsIndexed.get(int(col))) )
                        lbl.text += values.get(self.hdsIndexed.get(int(col))) + '\n'
                    except:
                        print(str(sys.exc_info()[1]))

                self.add_widget(lbl)
                labelsNew.append(lbl)
                #print('--------------')

            self.labels = labelsNew
            self.lbl1.text='Repopulating carousel: job\'s a good\'n...:)'

        except:
            self.lbl1.text='Error repopulating carousel!'
            # 29/5/18 DH: Debug only
            #raise

    def on_enter(self, txtinput):
        print('Order: ' + txtinput.text)
        self.repopulateCarousel()


    def btn1_pressed(self, instance):
        try:
            self.btn1Txt = instance.text
            instance.text = self.txt1.text

            self.sheet.update_cell(self.orderCell[0], self.orderCell[1], self.txt1.text)

            self.lbl1.text = 'Google sheets updated with: ' + self.txt1.text

        except AttributeError:
            instance.text = str(sys.exc_info()[1])
        except:
            instance.text = str(sys.exc_info()[0])

    def btn1_released(self, instance):
        #time.sleep(2)
        instance.text=self.btn1Txt

    # -------------------------------------------------------------------------------------------------
    # 5/6/18 DH: Kept in with 'class CustomBtn(Widget)' for ref (even though not currently using it...)
    def cstbtn_pressed(self, instance, pos):
        #print ('pos: printed from root widget: {pos}'.format(pos=pos))
        self.btn1.text='pos: {pos}'.format(pos=pos)


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

class SheetsApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    SheetsApp().run()
