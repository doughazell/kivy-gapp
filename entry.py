from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import sys

red = [1,0,0,1]
green = [0,1,0,1]
blue =  [0,0,1,1]
purple = [1,0,1,1]

class Entry(Screen):
    def __init__(self, **kwargs):
        super(Entry, self).__init__(**kwargs)

        entry_carousel = ObjectProperty(None)
        btnAdmin = ObjectProperty(None)
        btnEntry = ObjectProperty(None)
        btnSave = ObjectProperty(None)
        lblHd = ObjectProperty(None)

    def populateFields(self):
        self.display = self.manager.get_screen('display')

        #lbl = Label()

        layoutMain = BoxLayout(orientation='vertical')
        self.fieldsIndexed = {}

        for key in sorted(self.display.hdsIndexed.keys()):
            #lbl.text += str(key) + ': ' +  self.display.hdsIndexed[key] + '\n'

            layout = BoxLayout(orientation='horizontal')
            lbl = Label(text=self.display.hdsIndexed[key], color=red)
            #txt = TextInput(multiline=False, background_color=red, size_hint_x=None, width=300)
            txt = TextInput(multiline=False)

            self.fieldsIndexed[key] = txt

            layout.add_widget(lbl)
            layout.add_widget(txt)

            layoutMain.add_widget(layout)

        #self.entry_carousel.add_widget(lbl)
        self.entry_carousel.add_widget(layoutMain)

    def entryBtn_pressed(self):
        #print('entryBtn_pressed')
        self.manager.transition = SlideTransition(direction="down")
        self.manager.current = 'display'

    def adminBtn_pressed(self):
        #print('adminBtn_pressed')
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'main'

    def saveBtn_pressed(self):
        '''
        print('saveBtn_pressed')
        print('-----------------------------')
        for key in sorted(self.fieldsIndexed.keys()):
            print str(key) + ': ' + self.fieldsIndexed[key].text

        print('-----------------------------')
        '''
        try:
            townID = [k for k,v in self.display.hdsIndexed.items() if v == 'Town'][0]
            firstID = [k for k,v in self.display.hdsIndexed.items() if v == 'First Line'][0]

            #print 'Town: ' + str(townID) + ', First Line: ' + str(firstID)

            if not self.fieldsIndexed[firstID].text:
                self.displayMsg('First Line must not be blank')
            elif not self.fieldsIndexed[townID].text:
                self.displayMsg('Town must not be blank')
            else:
                # 3/7/18 DH: Save the data set

                newrecord = []
                for key in sorted(self.fieldsIndexed.keys()):
                    newrecord.append( str(self.fieldsIndexed[key].text) )

                # 4/7/18 DH: A sheet has a default of 1000 rows, so need to resize to number of rows present
                self.display.sheet.resize(self.display.record_num + 1)
                self.display.sheet.append_row(newrecord)

                #self.display.record_num += 1

                print 'REQUEST TO DB for all records'
                table = self.manager.get_screen('display')
                table.list_of_dicts = table.sheet.get_all_records(head=1)
                table.record_num = len(table.list_of_dicts)

                main = self.manager.get_screen('main')
                main.repopulateCarousel()


                # 5/7/18 DH: Not work with v0.6.2/Google Sheets API v3
                # Next empty row number needs to accomodate record num + headings
                #self.display.sheet.insert_row(newrecord, self.display.record_num + 2)

        except:
            self.displayMsg( str(sys.exc_info()[0]) )
            raise

    def displayMsg(self,msg):
        self.lblHd.font_size = 24
        self.lblHd.text = msg
        Clock.schedule_once(self.resetLabelHd, 4)

    def resetLabelHd(self, dt):
        self.lblHd.font_size = 32
        self.lblHd.text = 'Welcome'
