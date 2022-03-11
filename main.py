import sys

from PyQt5.QtGui import QIcon, QFont, QColor, QPen
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, \
    QGraphicsLineItem, QGraphicsTextItem, QLabel, QGraphicsProxyWidget, QLineEdit, QMainWindow, QAction, qApp, \
    QListWidget, QListWidgetItem, QGraphicsItemGroup, QPushButton, QVBoxLayout, QPlainTextEdit, QTextEdit, QMessageBox, \
    QDialog, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QPointF, QLineF, QPoint, QSize


class RelationshipObject(QGraphicsRectItem):
    def __init__(self, x, y, text):
        self.r = 100
        self.h = 100
        super().__init__(0, 0, self.r, self.h)
        self.setPos(x, y)
        self.setRotation(45)
        self.setAcceptHoverEvents(True)
        self.x = x
        self.y = y

        self.name1 = QLabel(text)
        self.name1.setGeometry(0, 75, 105, 35)

        self.setBrush(QColor("white"))
        self.name1.setStyleSheet("QLabel { background-color : white; }")
        self.name1.setAlignment(Qt.AlignCenter)
        self.name1.setFrameStyle(0)

        # self.pLineEdit = QLineEdit(text)
        # self.pLineEdit.setFrame(False)
        # self.pLineEdit.setGeometry(1, 35, 149, 35)
        self.pMyItem = QGraphicsProxyWidget(self)
        self.pMyItem.setWidget(self.name1)

        #self.pLineEdit = QLineEdit(text)
        #self.pLineEdit.setFrame(False)
        #self.pLineEdit.setGeometry(0, 75, 105, 35)
        #self.pMyItem = QGraphicsProxyWidget(self)
        #self.pMyItem.setWidget(self.pLineEdit)
        self.pMyItem.setRotation(-45)

        self.entity = None
        self.lines = []

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
        self.x = updated_cursor_x
        self.y = updated_cursor_y
        for line in self.lines:
            line.changeRelPos(self.x, self.y)


    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))

    def setLine(self, line):
        self.lines.append(line)

    def getPos(self):
        return self.x, self.y + int((self.h/2))

    def setMyPosition(self, x, y):
        self.x = x
        self.y = y


class RectObject(QGraphicsRectItem):
    def __init__(self, x, y, text):
        self.r = 150
        self.h = 100
        super().__init__(0, 0, self.r, self.h)
        self.setPos(x, y)
        self.x = x
        self.y = y
        self.x1 = self.x + self.r
        self.y1 = self.y + self.h
        self.setAcceptHoverEvents(True)

        self.name1 = QLabel(text)
        self.name1.setGeometry(1, 1, 149, 99)
        self.name1.setStyleSheet("QLabel { background-color : white; }")
        self.name1.setAlignment(Qt.AlignCenter)
        self.name1.setFrameStyle(0)

        #self.pLineEdit = QLineEdit(text)
        #self.pLineEdit.setFrame(False)
        #self.pLineEdit.setGeometry(1, 35, 149, 35)
        self.pMyItem = QGraphicsProxyWidget(self)
        self.pMyItem.setWidget(self.name1)
        #self.pMyItem.setWidget(self.pLineEdit)
        self.lines = []
        self.relLines = []
        #self.line = None

    def setMyPosition(self, x, y):
        self.x = x
        self.y = y
        self.x1 = self.x + self.r
        self.y1 = self.y + self.h

    def addRelLine(self, line, rel):
        #self.relLines = line
        self.relLines.append(line)
        rel.setLine(line)
        line.setEntity(self)
        line.setRel(rel)
        self.drawLine()

    def addLine(self, line, att):
        #self.line = line
        self.lines.append(line)
        """
        self.line.setEntity(self)
        self.att.setLine(line)
        self.line.setAtt(att)
        self.drawLine()
        """
        att.setLine(line)
        line.setEntity(self)
        line.setAtt(att)
        self.drawLine()

    def drawLine(self):
        """
        if self.line:
            self.line.changePos(self.x1, self.y1-50)
        """
        for line in self.lines:
            line.changePos(self.x1, self.y1-50)

        """
        if self.relLines:
            print("pridana")

            self.relLines.changePos(self.x1, self.y1-50)
        """
        for relLine in self.relLines:
            relLine.changePos(self.x1, self.y1-50)

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()
        #orig_cursor_position = event.lastPos()
        #updated_cursor_position = event.pos()

        orig_position = self.scenePos()
        #orig_position = self.pos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
        self.x = updated_cursor_x
        self.y = updated_cursor_y
        self.x1 = updated_cursor_x + self.r
        self.y1 = updated_cursor_y + self.h
        self.drawLine()

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))

    def getPos(self):
        return self.x1, self.y1-50


class EllipseObject(QGraphicsEllipseItem):
    def __init__(self, x, y, text):
        self.r = 150
        self.h = 100
        super().__init__(0, 0, self.r, self.h)
        self.setPos(x, y)
        self.setAcceptHoverEvents(True)
        self.x = x
        self.y = y
        self.line = None

        self.text = text

        self.name1 = QLabel(text)
        self.name1.setGeometry(20, 20, 109, 59)

        self.setBrush(QColor("white"))
        self.name1.setStyleSheet("QLabel { background-color : white; }")
        self.name1.setAlignment(Qt.AlignCenter)
        self.name1.setFrameStyle(0)

        # self.pLineEdit = QLineEdit(text)
        # self.pLineEdit.setFrame(False)
        # self.pLineEdit.setGeometry(1, 35, 149, 35)
        self.pMyItem = QGraphicsProxyWidget(self)
        self.pMyItem.setWidget(self.name1)

        #self.pLineEdit = QLineEdit(text)
        #self.pLineEdit.setFrame(False)
        #self.pLineEdit.setGeometry(10, 35, 120, 35)
        #self.pMyItem = QGraphicsProxyWidget(self)
        #self.pMyItem.setWidget(self.pLineEdit)

    def mousePressEvent(self, event):
        print(self.text)
        print(self.x)
        print(self.y)

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
        self.x = updated_cursor_x
        self.y = updated_cursor_y
        if self.line:
            self.line.changeAttPos(self.x, self.y)

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))

    def getPos(self):
        return self.x, self.y + int((self.h/2))

    def setLine(self, line):
        self.line = line

    def setMyPosition(self, x, y):
        self.x = x
        self.y = y


class ConnectingLine(QGraphicsLineItem):
    def __init__(self, x, y, r, h):
        super().__init__(0, 0, r, h)
        self.setLine(x, y, r, h)
        self.att = None
        self.entity = None
        self.rel = None
        self.pen = QPen()
        self.pen.setWidth(1)
        self.setPen(self.pen)

    def changePos(self, x, y):
        if self.att:
            uni_x, uni_y = self.att.getPos()
            if uni_y - 50 <= y + 50 and y - 50 <= uni_y + 50 and x > uni_x:
                self.setLine(x - 150, y, uni_x + 150, uni_y)
            elif uni_y - 50 <= y + 50 and y - 50 <= uni_y + 50 and x < uni_x:
                self.setLine(x, y, uni_x, uni_y)
            elif y > uni_y + 50:
                self.setLine(x - 75, y - 50, uni_x + 75, uni_y + 50)
            elif y < uni_y - 50:
                self.setLine(x - 75, y + 50, uni_x + 75, uni_y - 50)
            else:
                print(x, y, uni_x, uni_y)
                self.setLine(x, y, uni_x, uni_y)
        elif self.rel:
            uni_x, uni_y = self.rel.getPos()
            if uni_y - 50 <= y + 50 and y - 50 <= uni_y + 50 and x > uni_x:
                self.setLine(x - 150, y, uni_x + 70, uni_y+20)
            elif uni_y - 50 <= y + 50 and y - 50 <= uni_y + 50 and x < uni_x:
                self.setLine(x, y, uni_x-70, uni_y+20)
            elif y > uni_y + 50:
                self.setLine(x - 75, y - 50, uni_x, uni_y + 90)
            elif y < uni_y - 50:
                self.setLine(x - 75, y + 50, uni_x, uni_y - 50)
            else:
                print(x, y, uni_x, uni_y)
                self.setLine(x, y, uni_x, uni_y)

        #self.setLine(x, y, uni_x, uni_y)

    def changeAttPos(self, att_x, att_y):
        x, y = self.entity.getPos()
        if y > att_y-50 and att_y+50 > y - 100 and att_x < x - 150:
            self.setLine(x-150, y, att_x+150,att_y+50)
        elif y > att_y-50 and att_y+50 > y - 100 and att_x > x:
            self.setLine(x, y, att_x, att_y+50)
        elif att_y < y-100:
            self.setLine(x-75, y-50, att_x+75,att_y+100)
        elif att_y > y:
            self.setLine(x-75,y+50,att_x+75,att_y)
        else:
            self.setLine(x, y, att_x, att_y+50)

    def changeRelPos(self, rel_x, rel_y):
        x, y = self.entity.getPos()
        #self.setLine(x, y, rel_x, rel_y+50)
        if y > rel_y-50 and rel_y+50 > y - 140 and rel_x < x - 150:
            self.setLine(x-150, y, rel_x+70,rel_y+70)
        elif y > rel_y-50 and rel_y+50 > y - 140 and rel_x > x:
            self.setLine(x, y, rel_x-70, rel_y+70)
        elif rel_y < y-100:
            self.setLine(x-75, y-50, rel_x,rel_y+140)
        elif rel_y > y:
            self.setLine(x-75,y+50,rel_x,rel_y)
        else:
            self.setLine(x, y, rel_x, rel_y+50)

    def setAtt(self, att):
        self.att = att

    def setEntity(self, entity):
        self.entity = entity

    def setRel(self, rel):
        self.rel = rel


class GraphicView(QGraphicsView):
    def __init__(self, x):
        super().__init__(x)
        self.move_flag = False
        self.start_point = None
        self.line_mouse_move = None
        self.xt = None
        self.mode = 0
        self.prev = None
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.maximumViewportSize()
        #self.setSceneRect(0, 0, 500, 500)

        self.moveObject = RectObject(0, 0, "Zviera")
        self.entity2 = RectObject(0, 0, "Clovek")
        self.moveObject2 = EllipseObject(0, 0, "telefonne cislo")
        self.att2 = EllipseObject(0, 0, "pohlavie")
        self.att3 = EllipseObject(0, 0, "vek")
        self.relationship = RelationshipObject(0, 0, "pracuje")

        self.line1 = ConnectingLine(300, 300, 300, -20)
        self.line2 = ConnectingLine(300, 300, 300, -20)
        self.relLine = ConnectingLine(300, 300, 300, -20)
        self.relLine2 = ConnectingLine(300, 300, 300, -20)

        self.moveObject.addLine(self.line1, self.moveObject2)
        self.moveObject.addLine(self.line2, self.att2)
        self.moveObject.addRelLine(self.relLine, self.relationship)
        self.entity2.addRelLine(self.relLine2, self.relationship)

        self.scene.addItem(self.relLine2)
        self.scene.addItem(self.att3)
        self.scene.addItem(self.entity2)
        self.scene.addItem(self.relLine)
        self.scene.addItem(self.att2)
        self.scene.addItem(self.line1)
        self.scene.addItem(self.line2)
        self.scene.addItem(self.relationship)
        self.scene.addItem(self.moveObject)
        self.scene.addItem(self.moveObject2)
        #self.scene.addItem(self.line)



    def mouseReleaseEvent(self, event):
        if self.mode == 0:
            self.start_point = None

    def mouseMoveEvent(self, event):
        if self.move_flag:
            if self.line_mouse_move is None:
                point = self.mapToScene(int(self.start_point.x), int(self.start_point.y))
                end_point = self.mapToScene(event.pos())
                self.line_mouse_move = QGraphicsLineItem(int(point.x()), int(point.y()), int(end_point.x()), int(end_point.y()))
                self.scene.addItem(self.line_mouse_move)
            else:
                end_point = self.mapToScene(event.pos())
                self.line_mouse_move.setLine(self.start_point.x, self.start_point.y, end_point.x(), end_point.y())
        elif self.mode == 0:
            #if self.start_point is not None:
             #   print(self.items())
              #  for i in self.items():
               #     print(type(i.x())) ###mam ine typy QtPoint a float riesit
                #    print(type(self.start_point.x()))
                 #   if i.x() == self.start_point.x():
                  #      print("aahah")
            #print("pos")
            #print(event.screenPos())
            #item = self.items(event.pos())
            #print(item)
            super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if self.mode == 4:
            item = self.items(event.pos())
            print(item)
            if item:
                self.move_flag = True
                if isinstance(item[0], QGraphicsProxyWidget):
                    item = item[1]
                elif isinstance(item[0], QGraphicsLineItem):
                    if len(item) > 2:
                        item = item[2]
                    else:
                        item = item[1]
                else:
                    item = item[0]
                print(item)
                self.start_point = item
                if item and self.prev:
                    self.move_flag = False
                    self.scene.removeItem(self.line_mouse_move)
                    self.line_mouse_move = None
                    self.start_point = None
                    if type(self.prev) != type(item):
                        connecting_line = ConnectingLine(300, 300, 300, -20)
                        if isinstance(item, EllipseObject) or isinstance(self.prev, EllipseObject):
                            if isinstance(self.prev, RectObject) and isinstance(item, EllipseObject):
                                tmp = item
                                item = self.prev
                                self.prev = tmp
                                item.addLine(connecting_line, self.prev)
                                self.scene.addItem(connecting_line)
                            elif isinstance(item, RectObject) and isinstance(self.prev, EllipseObject):
                                item.addLine(connecting_line, self.prev)
                                self.scene.addItem(connecting_line)
                        elif isinstance(item, RelationshipObject) or isinstance(self.prev, RelationshipObject):
                            if isinstance(self.prev, RectObject) and isinstance(item, RelationshipObject):
                                tmp = item
                                item = self.prev
                                self.prev = tmp
                                item.addRelLine(connecting_line, self.prev)
                                self.scene.addItem(connecting_line)
                            elif isinstance(item, RectObject) and isinstance(self.prev, RelationshipObject):
                                item.addRelLine(connecting_line, self.prev)
                                self.scene.addItem(connecting_line)
                        self.prev = None
                    else:
                        self.prev = None
                elif item:
                    self.prev = item
        elif self.mode == 5:
            item = self.items(event.pos())
            if item:
                if isinstance(item[0], QGraphicsProxyWidget):
                    item = item[1]
                elif isinstance(item[0], ConnectingLine):
                    item = item[0]
                else:
                    item = item[0]
                    #item = item.name1 #ziskat label
                #if isinstance(item, (EllipseObject, ConnectingLine, RectObject, RelationshipObject)):
                print(item)
                self.scene.removeItem(item)
        elif self.mode == 1:
            entity_object = RectObject(0, 0, "")
            point = self.mapToScene(event.pos())
            entity_object.setPos(point.x(), point.y())
            self.scene.addItem(entity_object)
            entity_object.setMyPosition(point.x(), point.y())

        elif self.mode == 2:
            att_object = EllipseObject(0, 0, "")
            point = self.mapToScene(event.pos())
            self.scene.addItem(att_object)
            att_object.setPos(point)
            att_object.setMyPosition(point.x(), point.y())
        elif self.mode == 3:
            rel_object = RelationshipObject(0, 0, "")
            point = self.mapToScene(event.pos())
            self.scene.addItem(rel_object)
            rel_object.setPos(point)
            rel_object.setMyPosition(point.x(), point.y())
        elif self.mode == 6:
            item = self.items(event.pos())
            if item:
                print(item)
                if isinstance(item[0], ConnectingLine):
                    return
                if isinstance(item[0], QGraphicsProxyWidget):
                    item = item[0]
                else:
                    if len(item)<2:
                        item = item[0]
                    else:
                        item = item[1]
                self.xt = PopUp()
                while self.xt.input_text is None:
                    continue
                if isinstance(item, QGraphicsProxyWidget):
                    item.widget().setText(self.xt.input_text)
                else:
                    item.pMyItem.widget().setText(self.xt.input_text)

        elif self.mode == 0:
            super().mousePressEvent(event)
            self.start_point = self.items(event.pos())

        else:
            super().mousePressEvent(event)

    def add_entity(self):
        self.mode = 1

    def add_connect(self):
        self.mode = 4

    def add_attribute(self):
        self.mode = 2

    def add_relationship(self):
        self.mode = 3

    def delete(self):
        self.mode = 5

    def rename(self):
        self.mode = 6

    def basic(self):
        self.mode = 0


class QTextBox(object):
    pass


class PopUp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zvoľte názov")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.setFixedSize(300, 100)
        self.input = QPlainTextEdit("ads\r\nwd\neew\n")
        self.input = QLineEdit()
        self.button = QPushButton("Zvoľ")
        self.button.clicked.connect(self.execute)
        self.input_text = None

        layout.addWidget(self.input)
        layout.addWidget(self.button)

        self.exec_()

    def execute(self):
        self.input_text = self.input.text()
        self.close()


class ButtonPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.hlayout = QHBoxLayout()
        self.hlayout.setSpacing(0)
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hlayout)

        self.button_widget = QWidget()
        self.button_layout = QVBoxLayout()
        self.button_layout.setSpacing(0)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_widget.setLayout(self.button_layout)

        self.hlayout.addWidget(self.button_widget)


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Data model generator")
        self.setGeometry(0, 0, 1280, 800)
        #self.setFixedSize(1280, 1000)

        self.mlayout = QVBoxLayout()
        self.mlayout.setSpacing(10)
        self.mlayout.setContentsMargins(0,5,0,0)
        self.widget = QWidget()
        self.widget.setLayout(self.mlayout)
        self.setCentralWidget(self.widget)

        self.view = GraphicView(self)
        self.mlayout.addWidget(self.view, 2)
        #self.view.setGeometry(0, 25, 1280, 650)

        self.mode_info = QLabel("Základný mód")
        #self.mode_info.setGeometry(0, 675, 1280, 50)
        self.mode_info.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(15)
        self.mode_info.setFont(font)
        self.mlayout.addWidget(self.mode_info)
        #self.mode_info.setStyleSheet("QLabel { background-color : red; }")

        self.exit_action, self.entity_action, self.attribute_action, self.relationship_action, self.connect_line, self.delete_action, self.rename_action, self.basic_action = self.toolbar_actions()
        self.toolbar = self.create_toolbar()

        self.start_button = QPushButton("Start")
        #self.start_button.setGeometry(0, 725, 125, 90)
        self.start_button.setMinimumSize(100, 70)
        self.mlayout.addWidget(self.start_button)
        self.delete_button = QPushButton("Delete")
        self.delete_button.setMinimumSize(100, 70)
        #self.delete_button.setGeometry(0, 815, 125, 90)
        self.delete_button.clicked.connect(self.delete_text)
        self.mlayout.addWidget(self.delete_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setMinimumSize(100, 70)
        #self.clear_button.setGeometry(0, 905, 125, 95)
        self.clear_button.clicked.connect(self.clear_view)
        self.mlayout.addWidget(self.clear_button)

        self.button_panel = ButtonPanel()
        self.button_panel.button_layout.addWidget(self.start_button)
        self.button_panel.button_layout.addWidget(self.delete_button)
        self.button_panel.button_layout.addWidget(self.clear_button)
        self.mlayout.addWidget(self.button_panel)

        self.text_area = QPlainTextEdit(self)
        font = QFont()
        font.setPointSize(12)
        self.text_area.setFont(font)
        self.text_area.setPlaceholderText("Zadajte text.")
        self.button_panel.hlayout.addWidget(self.text_area)
        #self.text_area.setGeometry(125, 725, 1155, 275)


    def clear_view(self):
        self.view.scene.clear()

    def delete_text(self):
        self.text_area.clear()

    def trigger_delete(self):
        self.mode_info.setText("Mód mazania")
        self.view.delete()

    def trigger_entity(self):
        self.mode_info.setText("Mód tvorby entít")
        self.view.add_entity()

    def trigger_connect(self):
        self.mode_info.setText("Mód spájania prvkov")
        self.view.add_connect()

    def trigger_attribute(self):
        self.mode_info.setText("Mód tvorby atribútov")
        self.view.add_attribute()

    def trigger_relationship(self):
        self.mode_info.setText("Mód tvorby vzťahov")
        self.view.add_relationship()

    def trigger_rename(self):
        self.mode_info.setText("Mód premenovania prvkov")
        self.view.rename()

    def trigger_basic(self):
        self.mode_info.setText("Základný mód")
        self.view.basic()

    def toolbar_actions(self):
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(qApp.quit)

        entity_action = QAction('Entita', self)
        entity_action.triggered.connect(self.trigger_entity)

        attribute_action = QAction('Atribút', self)
        attribute_action.triggered.connect(self.trigger_attribute)

        relationship_action = QAction('Vzťah', self)
        relationship_action.triggered.connect(self.trigger_relationship)

        connect_line = QAction('Pripojiť', self)
        connect_line.triggered.connect(self.trigger_connect)

        delete_action = QAction('Vymazať', self)
        delete_action.triggered.connect(self.trigger_delete)

        rename_action = QAction('Premenovať', self)
        rename_action.triggered.connect(self.trigger_rename)

        basic_action = QAction('Pozorovať', self)
        basic_action.setShortcut(Qt.Key_Escape)
        basic_action.triggered.connect(self.trigger_basic)

        return exit_action, entity_action, attribute_action, relationship_action, connect_line, delete_action, rename_action, basic_action

    def create_toolbar(self):
        toolbar = self.addToolBar('TB')
        toolbar.setMovable(False)
        toolbar.addAction(self.basic_action)
        toolbar.addAction(self.exit_action)
        toolbar.addAction(self.entity_action)
        toolbar.addAction(self.attribute_action)
        toolbar.addAction(self.relationship_action)
        toolbar.addAction(self.connect_line)
        toolbar.addAction(self.delete_action)
        toolbar.addAction(self.rename_action)
        return toolbar


app = QApplication(sys.argv)
win = MainWin()
win.show()
sys.exit(app.exec_())



#view = GraphicView()

#view.show()
#sys.exit(app.exec_())