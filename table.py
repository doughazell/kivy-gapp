from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import ObjectProperty

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.carousel import Carousel
from kivy.uix.textinput import TextInput

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import sys

def getHeadings(table, main):
    '''
    print self.list_of_dicts

    print '-----------------------------'
    keyList = sorted(self.list_of_dicts[0].keys())
    print keyList
    print keyList[0]
    print '-----------------------------'
    '''

    print 'REQUEST TO DB for row 1 (ie headings)'
    headings = filter(None, table.sheet.row_values(1))

    lastCol = len(headings)
    table.orderCell = [1,lastCol]

    # 28/6/18 DH: Col order is the last heading
    order = headings.pop()
    print 'Order: ' + order
    main.txt1.text = order

    main.lbl2.text = ''
    table.hdsIndexed = {}
    col = 1
    for heading in headings:
        table.hdsIndexed[col] = heading
        #print ('Col ' + str(col) + ' = ' + heading)

        main.lbl2.text += str(col) + ' = ' + heading + '\n'
        col += 1
    #print self.hdsIndexed

class Table(Screen):
    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)

        table_carousel = ObjectProperty(None)
        btnAdmin = ObjectProperty(None)

    '''
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'main'
        #self.manager.get_screen('login').resetForm()

    def updateLabel(self):
        app = App.get_running_app()
        self.lbl1.text=app.username + ': ' + app.password
    '''

    def adminBtn_pressed(self):
        print('adminBtn_pressed')
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'main'
        self.chg = True


    def populateCarousel(table, main):
        # 20/2/18 DH: Just starting to refactor the hack...XP, all the way...
        try:
            # 2/11/17 DH:
            # use creds to create a client to interact with the Google Drive API
            scope = ['https://spreadsheets.google.com/feeds']
            creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
            client = gspread.authorize(creds)

            print 'Opening \'Addresses:Personal\'...'
            table.sheet = client.open("Addresses").worksheet("Personal")

            print 'REQUEST TO DB for all records'
            table.list_of_dicts = table.sheet.get_all_records(head=1)

            table.record_num = len(table.list_of_dicts)

            main.lbl1.text = str(table.record_num) + ' records'

            getHeadings(table, main)

            # 29/5/18 DH: Create empty array for label slides to removed on repopulateCarousel()
            table.labels = []

            # 24/2/18 DH: Carousel
            table.table_carousel.direction='right'

            cols = main.txt1.text.split(",")
            # === Rows ===
            for idx in range(0,table.record_num):
                lbl = Label()

                #print 'REQUEST TO DB for row ' + str(idx+2)
                #values = self.sheet.row_values(idx+2)

                values = table.list_of_dicts[idx]

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
                        lbl.text += values.get(table.hdsIndexed.get(int(col))) + '\n'

                    # Add record to carousel
                    #print "Adding: " + lbl.text
                    table.table_carousel.add_widget(lbl)

                    table.labels.append(lbl)

        except AttributeError:
            main.lbl1.text = str(sys.exc_info()[1])
            #raise

        except:
            main.lbl1.text='Error with Google Sheets!'
            # 29/5/18 DH: Debug only
            #raise
