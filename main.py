from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.uix.carousel import Carousel
from kivy.uix.textinput import TextInput

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

# 8/9/17 DH: Changing button text and sleeping prior to reverting it
#import time
# 27/6/18 DH: Sleep blocks an event driven framework like Kivy and events are not handled
from kivy.clock import Clock

import sys

#from kivy.config import Config
#Config.set('graphics', 'width', '1440')
#Config.set('graphics', 'height', '2560')

from table import Table
from entry import Entry

red = [1,0,0,1]
green = [0,1,0,1]
blue =  [0,0,1,1]
purple = [1,0,1,1]

# ====================== class Sheets(Screen) =========================
class Sheets(Screen):
    def __init__(self, **kwargs):
        super(Sheets, self).__init__(**kwargs)

        lbl1 = ObjectProperty(None)
        btn1 = ObjectProperty(None)
        txt1 = ObjectProperty(None)
        lbl1 = ObjectProperty(None)
        lbl2 = ObjectProperty(None)
        btnAdmin = ObjectProperty(None)

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    #def adminBtn_pressed(self, instance):
    def adminBtn_pressed(self):
        #print('adminBtn_pressed')
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'display'

    def repopulateCarousel(self):
        table = self.manager.get_screen('display')
        try:
            #self.clear_widgets()
            labelsNew = []

            cols = self.txt1.text.split(",")
            for idx in range(0,table.record_num):
                # 8/7/18 DH: Can't remove a widget of a newly created record...!
                try:
                    table.table_carousel.remove_widget(table.labels[idx])
                except IndexError:
                    #print('idx: ' + str(idx) + ' newly created so no label to remove...')
                    pass

                lbl = Label()

                values = table.list_of_dicts[idx]
                #print values

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
                        lbl.text += str( values.get(table.hdsIndexed.get(int(col))) ) + '\n'
                    except:
                        print(str(sys.exc_info()[1]))
                        #raise

                table.table_carousel.add_widget(lbl)
                labelsNew.append(lbl)

            table.labels = labelsNew
            self.lbl1.text='Repopulating carousel: job\'s a good\'n...:)'

            # Sleep blocks an event driven framework like Kivy and events are not handled
            #time.sleep(2)
            Clock.schedule_once(self.clearLabel1, 2)

        except AttributeError:
            self.lbl1.text = str(sys.exc_info()[1])

        except:
            self.lbl1.text='Error repopulating carousel!'
            # 29/5/18 DH: Debug only
            raise

    def clearLabel1(self, dt):
        self.lbl1.text=''

    def on_enter(self):
        if self.manager.has_screen('display'):
            try:
                self.display = self.manager.get_screen('display')
                self.display.chg
                del self.display.chg
            except:
                print('Order: ' + self.txt1.text)
                self.repopulateCarousel()

    def btn1_pressed(self, instance):
        try:
            self.btn1Txt = instance.text
            instance.text = self.txt1.text

            try:
                self.display
            except:
                self.display = self.manager.get_screen('display')

            row = self.display.orderCell[0]
            col = self.display.orderCell[1]
            value = self.txt1.text

            #self.display.sheet.update_cell(self.orderCell[0], self.orderCell[1], self.txt1.text)
            self.display.sheet.update_cell(row, col, value)

            self.lbl1.text = 'Google sheets updated with: ' + value
            Clock.schedule_once(self.clearLabel1, 4)

        except AttributeError:
            instance.text = str(sys.exc_info()[1])
        except:
            instance.text = str(sys.exc_info()[0])

    def btn1_released(self, instance):
        instance.text=self.btn1Txt


# ====================== END: class Sheets(Screen) =========================

# ====================== class SheetsApp(App) =========================
class SheetsApp(App):

    def build(self):
        # 19/6/18 DH: Leaving a little bit of history...:)
        #return RootWidget()

        manager = ScreenManager()

        main = Sheets(name='main')
        manager.add_widget( main )

        table = Table(name='display')
        manager.add_widget( table )
        table.populateCarousel(main)

        entry = Entry(name='update')
        manager.add_widget( entry )
        entry.populateFields()

        return manager


    '''
    def adminBtn_pressed(self, instance):
        if self.screen == 'main':
            instance.text="Use main carousel"

            self.adminCarousel.size_hint_y = 1
            self.adminCarousel.size_hint_x = 1
            self.adminCarousel.pos_hint = {'top': 1, 'right': 1}

            self.entryAdmin.show_login()

            self.screen = 'admin'
        else:
            instance.text="Use admin carousel"

            self.adminCarousel.size_hint_y = 0.15
            self.adminCarousel.size_hint_x = 0.4
            self.adminCarousel.pos_hint = {'top': 0.17, 'right': 0.7}

            self.screen = 'main'

        #self.adminCarousel.load_next()
        #self.adminCarousel.load_previous()
    '''

# ====================== END: class SheetsApp(App) =========================


if __name__ == '__main__':
    SheetsApp().run()
