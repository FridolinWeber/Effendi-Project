#if application becomes larger it is better to put the methods in several scripts

import sys
from PyQt4 import QtGui, QtCore #QtCore has to be imported to include buttons to the application


# define the layout of main window
class Window(QtGui.QMainWindow): #main application mostly always inherits from QtGui.QMainWindow or QT.Widget

    # initialize the window layout
    def __init__(self): #sets the core application stuff (e.g. a template) /// main menu (like also menu bars can be put into the init method ///
        super(Window, self).__init__() #super returns the parent object
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Test GUI")
        self.setWindowIcon(QtGui.QIcon('pythonLogo.png')) #creats the icon of the window

        #this is the stuff for the main menu

        extractAction = QtGui.QAction("&Quit", self) #extract action is connected to the menu bar
        extractAction.setShortcut("Q") #creats a shorcut to trigger extractAction
        extractAction.setStatusTip('Closes the application')
        # when a user clicks on the menu item, call close_application
        extractAction.triggered.connect(self.close_application) #triggers the close application method

        self.statusBar() #calls the status bar if mouse hovers across the quit button

        mainMenu = self.menuBar() #something has to be added to the menu bar. Because of this the object mainMenu is created. (You have to assign something to a variable if you want to modify it
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)

        self.home() #reference to home method(see below)

    # define what goes on the home screen
    def home(self): #method that is specific to the specific page that one is on
        btn = QtGui.QPushButton("Quit", self)  #btn ->defines a button
        btn.clicked.connect(self.close_application) #whenever there is an event, .connect is needed ->passes through a method
        btn.setStatusTip('Closes the application')
        btn.resize(btn.minimumSizeHint()) #creates the button with the minimum space needed (btn.resize(100,100))makes button larger or btn.resize(btn.sizeHint())
        btn.move(400, 276) #sets the button to a specific location
        self.statusBar()

        #create a toolbar
        settingsAction = QtGui.QAction(QtGui.QIcon('settings.png'), 'Settings', self) #this is how an icon can be added to the toolbar ("Settigs" pop up if the mouse hovers the icon)
        settingsAction.triggered.connect(self.close_application) #action that the toolbar button is connected to
        self.toolBar = self.addToolBar("Settings") #toolbar that is added
        self.toolBar.addAction(settingsAction)


        maxiAction = QtGui.QAction(QtGui.QIcon('maxi.png'), 'Maximize', self)
        maxiAction.triggered.connect(self.enlarge_window)
        self.toolBar = self.addToolBar("Maximize")
        self.toolBar.addAction(maxiAction)

        #everything that is to appear in this window has to be before self.show()
        self.show()

    # closes the window
    def close_application(self):

        #choice: ask the user, if he really wants to close the application
       choice = QtGui.QMessageBox.question(self, 'Exit',
                                           'Are you sure you want to quit?',
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
       if choice == QtGui.QMessageBox.Yes:
            print ("Exiting....")
            sys.exit()
       else:
            pass


    def enlarge_window(self):
        self.setGeometry(50, 50, 800, 400)


# run the main window
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window() #create instance of window class
    sys.exit(app.exec_())


run()
