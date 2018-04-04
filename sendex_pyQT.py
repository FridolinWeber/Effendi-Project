import sys
from PyQt4 import QtGui, QtCore


# define the layout of main window
class Window(QtGui.QMainWindow):

    # initialize the window layout
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Test GUI")
        self.setWindowIcon(QtGui.QIcon('pythonLogo.png'))

        extractAction = QtGui.QAction("&Quit", self)
        extractAction.setShortcut("Q")
        extractAction.setStatusTip('Closes the application')
        # when a user clicks on the menu item, call close_application
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)

        self.home()

    # define what goes on the home screen
    def home(self):
        btn = QtGui.QPushButton("Quit", self)
        btn.clicked.connect(self.close_application)
        btn.setStatusTip('Closes the application')
        btn.resize(btn.minimumSizeHint())
        btn.move(400, 276)
        self.statusBar()

        settingsAction = QtGui.QAction(QtGui.QIcon('settings.png'), 'Settings', self)
        settingsAction.triggered.connect(self.close_application)
        self.toolBar = self.addToolBar("Settings")
        self.toolBar.addAction(settingsAction)


        maxiAction = QtGui.QAction(QtGui.QIcon('maxi.png'), 'Maximize', self)
        maxiAction.triggered.connect(self.enlarge_window)
        self.toolBar = self.addToolBar("Maximize")
        self.toolBar.addAction(maxiAction)
        self.show()

    # closes the window
    def close_application(self):

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
    GUI = Window()
    sys.exit(app.exec_())


run()
