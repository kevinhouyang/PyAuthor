import sys
import os
# from PyQt5 import QtGui, QtCore
# from PyQt5.QtWidgets import QAction, QMainWindow, QPlainTextEdit, QFileDialog, QApplication
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QAction, QMainWindow, QPlainTextEdit, QFileDialog, QApplication, QTreeView, QFileSystemModel, QDockWidget
from PyQt5.QtCore import Qt

class Main(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.filename = ""

        self.initUI()

        style = open("style.qss", 'r')
        self.setStyleSheet(style.read())

    def initAction(self):
        self.newAction = QAction(QtGui.QIcon("icons/new.png"), "New", self)
        self.newAction.setStatusTip("Create a new document")
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.triggered.connect(self.new)

        self.openAction = QAction(QtGui.QIcon("icons/open.png"),"Open file", self)
        self.openAction.setStatusTip("Open existing document")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QAction(QtGui.QIcon("icons/save.png"),"Save",self)
        self.saveAction.setStatusTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.saveAsAction = QAction("Save As", self)
        self.saveAsAction.setStatusTip("Save document as")
        self.saveAsAction.setShortcut("Ctrl+Shift+S")
        self.saveAsAction.triggered.connect(self.saveAs)

        self.exitAction = QAction("Exit", self)
        self.exitAction.setStatusTip("Exit word processor")
        self.exitAction.setShortcut("Ctrl+W")
        self.exitAction.triggered.connect(sys.exit)

        self.hideDirAction = QAction("Toggle Dir Visibility", self)
        self.hideDirAction.setStatusTip("Show/Hide the Directory View")
        self.hideDirAction.setShortcut("Ctrl+\\")
        self.hideDirAction.triggered.connect(self.toggleDirVisibility)

    # def initFormatbar(self):
    #     self.formatbar = self.addToolBar("Format")

    def initMenubar(self):
        menubar = self.menuBar()

        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")

        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)
        file.addAction(self.saveAsAction)
        file.addAction(self.exitAction)

        view.addAction(self.hideDirAction)

    def initFont(self):
        self.font = QtGui.QFont("Futura", pointSize=16)
        self.document.setDefaultFont(self.font)

    def initFileTree(self):
        #TODO: fix the scope of these variables
        #TODO: setpathindex
        #TODO: toggle hideable

        self.dockWidget = QDockWidget(self)
        # titleWidget = QtWidget(self)
        # self.dockWidget.setTitleBarWidget(titleWidget)
        self.view = QTreeView(self)

        self.model = QFileSystemModel()
        self.model.setRootPath("/Users/kevinhouyang/Development/")
        self.view.setModel(self.model)
        self.view.setRootIndex(self.model.index("/Users/kevinhouyang/Development/typy"));
        self.dockWidget.setWidget(self.view)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.dockWidget)
        self.dockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dockWidget.setVisible(False)

    def initUI(self):
        self.editor = QPlainTextEdit(self)
        self.document = self.editor.document()

        self.document.setDocumentMargin(100)
        self.initFont()

        self.editor.setCenterOnScroll(True)
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

        self.initAction()
        self.initMenubar()

        self.setCentralWidget(self.editor)
        self.initFileTree()
        # init dockwidget

        self.setGeometry(100,100,1030,800)
        self.setWindowTitle("QtWriter")


    #TODO fix this..? how do i get formatting to show
    def updateFocus(self):
        for i in range(self.document.lineCount()):
            print(i)
            currBlock = self.document.findBlockByLineNumber(i)
            print(currBlock.text())
            currBlock.blockFormat().setBackground(QtGui.QColor(10,10,10))

            # print(currBlock.blockFormat().fontUnderline())
            #
        self.editor.update()
        # for each line in the textdocument
        # adjust its lightness in accordance to distance from cursor line


    def new(self):
        spawn = Main(self)
        spawn.show()

    def open(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Open File', ".", "(*.txt)")[0]

        if self.filename:
            with open(self.filename, "r") as file:
                self.document.setPlainText(file.read())

        self.setWindowTitle("QtWriter - " + os.path.basename(self.filename))
        # self.updateFocus()

    def save(self):
        if not self.filename:
            self.filename = QFileDialog.getSaveFileName(self, 'Save File')[0]

        if self.filename:
            if not self.filename.endswith(".txt"):
                self.filename += ".txt"

            with open(self.filename,"w") as file:
                file.write(self.editor.toPlainText())

    def saveAs(self):
        self.filename = QFileDialog.getSaveFileName(self, 'Save File')[0]
        self.save()

    def exit(self):
        print("just tried to exit!")

    def toggleDirVisibility(self):
        if self.dockWidget.isVisible():
            self.dockWidget.setVisible(False)
        else:
            self.dockWidget.setVisible(True)

def main():
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
