import os, sys, copy
from PyQt5 import QtCore, uic, QtWidgets, QtGui

class MenuWidget( QtWidgets.QTabWidget ):

    def __init__(
            self, 
            controller
        ):
        super(MenuWidget, self).__init__()
        self.controller = controller
        self.menuName = None
        self.buttonCallback = None
        self.buttonList = []
        self.setTabPosition(QtWidgets.QTabWidget.West)
        self.setElideMode(QtCore.Qt.ElideNone)
        self.setStyleSheet(
            "QTabBar::tab::disabled {width: 0; heigth: 0; margin: 0; padding: 0; border: none;}"
        )  

    def addTabContainer(self, tabId, tabName, tabIndex=1):
        tab = QtWidgets.QWidget()
        tab.setObjectName( tabName )
        tab.id = tabId
        layout_tab = QtWidgets.QVBoxLayout(tab)
        layout_tab.setObjectName(u'area')
        scroll = QtWidgets.QScrollArea(tab)
        scroll.setWidgetResizable(True)
        scroll_widget = QtWidgets.QWidget()
        scroll_widget.setGeometry(QtCore.QRect(0, 0, 328, 386))
        scroll_widget.setObjectName(u'scroll')
        layout_button = QtWidgets.QVBoxLayout(scroll_widget)
        layout_button.setObjectName(u'layout')
        scroll.setWidget(scroll_widget)
        layout_tab.addWidget(scroll)
        self.insertTab(tabIndex, tab, tabName)
        self.setCurrentIndex(0)

    def updateTabContainer(self, tabId, tabName): 
        tabIndex = self.getTabIndexFromId( tabId )
        self.setTabText( tabIndex, tabName)

    def deleteTabContainer(self, tabId): 
        tabIndex = self.getTabIndexFromId( tabId )
        if tabIndex is None:
            return
        """ if not self.emptyTab( tabIndex ):
            raise Exception('Aba com botões') """
        self.removeTab( tabIndex )

    def getTabContainerNames(self):
        return [
            {
                'name': self.tabText( idx ),
                'id': self.widget( idx ).id
            }
            for idx in range(self.count()) 
        ]

    def getTabIndexFromId(self, tabId):
        for idx in range(self.count()):
            tabWidget = self.widget( idx )
            if not( tabWidget.id == tabId ):
                continue
            return idx

    def emptyTab(self, tabIndex):
        tabWidget = self.widget( tabIndex )
        tabScroll = tabWidget.findChildren(QtWidgets.QScrollArea)[0].children()[0].children()[0]
        tabLayout = tabScroll.children()[0]
        return tabLayout.count() == 0

    def addButton(self, buttonConfig, callback):
        tabLayout = self.getTabLayout( buttonConfig[ 'buttonTabId' ] )
        button = QtWidgets.QPushButton()
        button.id = buttonConfig['buttonId']
        button.buttonConfig = buttonConfig
        button.setStyleSheet( 
            '''background-color: rgb({0}); color: rgb({1});'''.format( 
                buttonConfig[ 'buttonBackgroundColor' ],
                buttonConfig[ 'buttonTextColor' ]
            ) 
        )
        buttonName = buttonConfig['buttonName']
        button.setObjectName( buttonName )        
        count = tabLayout.count()
        if count >=0 and count <= 8:
            button.setText("{0}_[{1}]".format(buttonName, count+1 ))
            button.setShortcut(
                self.getButtonShortcut(count)
            )
        else:
            button.setText( buttonName )
        button.setToolTip( buttonConfig[ 'buttonTooltip' ] )
        button.clicked.connect(lambda b, button=button: callback( button.buttonConfig ))    
        tabLayout.addWidget(button)

    def getButtonShortcut(self, no):
        shortcuts = {
            0 : QtCore.Qt.Key_1,
            1 : QtCore.Qt.Key_2,
            2 : QtCore.Qt.Key_3,
            3 : QtCore.Qt.Key_4,
            4 : QtCore.Qt.Key_5,
            5 : QtCore.Qt.Key_6,
            6 : QtCore.Qt.Key_7,
            7 : QtCore.Qt.Key_8,
            8 : QtCore.Qt.Key_9
        }
        return shortcuts[no]

    def updateButton(self, newButtonConfig, oldButtonConfig, callback):
        self.deleteButton( oldButtonConfig )
        self.addButton( newButtonConfig, callback )

    def deleteButton(self, buttonConfig):
        tabLayout = self.getTabLayout( buttonConfig['buttonTabId'] )
        for idx in range(tabLayout.count()):
            if not( tabLayout.itemAt(idx).widget().id == buttonConfig['buttonId'] ):
                continue
            item = tabLayout.takeAt( idx )
            widget = item.widget()
            if widget:
                widget.deleteLater()
            del item
            return
        raise Exception('Botão não encontrado!')

    def getTabButtons(self, tabIndex):
        tabLayout = self.getTabLayout( self.widget( tabIndex ).id )
        return [
            tabLayout.itemAt(idx).widget()
            for idx in range(tabLayout.count())
        ]
        
    def getTabLayout(self, tabId):
        tabIdx = self.getTabIndexFromId( tabId )
        tabScroll = self.widget( tabIdx ).findChildren(QtWidgets.QScrollArea)[0].children()[0].children()[0]
        tabLayout = tabScroll.children()[0]
        return tabLayout

    def clean(self):
        while self.count() > 0:
            tabWidget = self.widget( 0 )
            self.deleteTabContainer( tabWidget.id )

    def setMenuName(self, menuName):
        self.menuName = menuName

    def getMenuName(self):
        return self.menuName

    def dump(self):
        menuDump = {
            "menuName": self.getMenuName(),
            "setup": []
        }
        for idx in range(self.count()):
            tabWidget = self.widget( idx )
            tabData = {
                "tabName": self.tabText( idx ),
                "tabId": tabWidget.id,
                "tabButtons": []
            }
            tabLayout = self.getTabLayout( tabWidget.id )
            for idx in range(tabLayout.count()):
                tabData['tabButtons'].append( tabLayout.itemAt(idx).widget().buttonConfig )
            menuDump["setup"].append( tabData )
        return menuDump

    def load(self, menuConfig, buttonCallback):
        self.buttonCallback = buttonCallback
        self.buttonList = []
        self.setMenuName( menuConfig["menuName"] )
        for tabData in menuConfig["setup"]:
            self.addTabContainer( tabData['tabId'], tabData['tabName'] )
            for buttonData in tabData['tabButtons']:
                self.buttonList.append( buttonData )
                self.addButton( buttonData, self.buttonCallback )

    def searchButtons(self, name):
        tabSearchId = '****'
        found = []
        if not name:
            self.deleteTabContainer( tabSearchId )
            return
        for buttonData in self.buttonList:
            if not( name in buttonData['buttonName'] or name in buttonData['buttonKeyWords'].split(';') ):
                continue
            buttonData['buttonTabId'] = tabSearchId
            found.append( buttonData )
        if not found:
            self.deleteTabContainer( tabSearchId )
            return
        self.deleteTabContainer( tabSearchId )
        self.addTabContainer( tabSearchId, '***Pesquisa***', 0 )
        [ self.addButton( buttonData, self.buttonCallback ) for buttonData in found ]