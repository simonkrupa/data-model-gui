import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, \
    QGraphicsLineItem, QGraphicsTextItem, QLabel, QGraphicsProxyWidget, QLineEdit, QMainWindow, QAction, qApp, \
    QListWidget, QListWidgetItem, QGraphicsItemGroup, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QPointF, QLineF


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

        self.pLineEdit = QLineEdit(text)
        self.pLineEdit.setFrame(False)
        self.pLineEdit.setGeometry(0, 75, 105, 35)
        self.pMyItem = QGraphicsProxyWidget(self)
        self.pMyItem.setWidget(self.pLineEdit)
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

        self.pLineEdit = QLineEdit(text)
        self.pLineEdit.setFrame(False)
        self.pLineEdit.setGeometry(1, 35, 149, 35)
        self.pMyItem = QGraphicsProxyWidget(self)
        self.pMyItem.setWidget(self.pLineEdit)
        self.lines = []
        self.relLines = []
        #self.line = None

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

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
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

        self.pLineEdit = QLineEdit(text)
        self.pLineEdit.setFrame(False)
        self.pLineEdit.setGeometry(10, 35, 120, 35)
        self.pMyItem = QGraphicsProxyWidget(self)
        self.pMyItem.setWidget(self.pLineEdit)

    def mousePressEvent(self, event):
        print(self.text)

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


class ConnectingLine(QGraphicsLineItem):
    def __init__(self, x, y, r, h):
        super().__init__(0, 0, r, h)
        self.setLine(x, y, r, h)
        self.att = None
        self.entity = None
        self.rel = None

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
    def __init__(self):
        super().__init__()
        self.flag = False
        self.prev = None
        self.delete_flag = False
        self.scene = QGraphicsScene()
        self.setScene(self.scene)       
        self.setSceneRect(0, 0, 500, 500)

        self.moveObject = RectObject(50, 50, "Zviera")
        self.entity2 = RectObject(700, 400, "Clovek")
        self.moveObject2 = EllipseObject(300, 100, "telefonne cislo")
        self.att2 = EllipseObject(600, 100, "pohlavie")
        self.att3 = EllipseObject(100, 100, "vek")
        self.relationship = RelationshipObject(500, 500, "pracuje")

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

    def mousePressEvent(self, event):
        if self.flag:
            self.delete_flag = False
            item = self.items(event.pos())
            if item:
                if isinstance(item[0], QGraphicsProxyWidget):
                    item = item[1]
                else:
                    item = item[0]
                if item and self.prev:
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
                        self.flag = False
                    else:
                        self.prev = None
                        self.flag = False
                elif item:
                    self.prev = item
        elif self.delete_flag:
            self.flag = False
            item = self.items(event.pos())
            if item:
                if isinstance(item[0], QGraphicsProxyWidget):
                    item = item[1]
                else:
                    item = item[0]
                #if isinstance(item, (EllipseObject, ConnectingLine, RectObject, RelationshipObject)):
                self.scene.removeItem(item)
                self.delete_flag = False
        else:
            super().mousePressEvent(event)

    def add_entity(self):
        entity_object = RectObject(5, 5, "")
        self.scene.addItem(entity_object)

    def add_connect(self):
        self.flag = True

    def add_attribute(self):
        att_object = EllipseObject(50, 50, "")
        self.scene.addItem(att_object)

    def add_relationship(self):
        rel_object = RelationshipObject(100, 100, "")
        self.scene.addItem(rel_object)

    def delete(self):
        self.delete_flag = True


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Data model generator")
        self.setGeometry(300,200,640,520)

        self.exit_action, self.entity_action, self.attribute_action, self.relationship_action, self.connect_line, self.delete_action = self.toolbar_actions()
        self.toolbar = self.create_toolbar()

        self.view = GraphicView()
        self.setCentralWidget(self.view)

    def trigger_delete(self):
        self.view.delete()

    def trigger_entity(self):
        self.view.add_entity()

    def trigger_connect(self):
        self.view.add_connect()

    def trigger_attribute(self):
        self.view.add_attribute()

    def trigger_relationship(self):
        self.view.add_relationship()

    def toolbar_actions(self):
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(qApp.quit)

        entity_action = QAction('Entity', self)
        entity_action.triggered.connect(self.trigger_entity)

        attribute_action = QAction('Attribute', self)
        attribute_action.triggered.connect(self.trigger_attribute)

        relationship_action = QAction('Relationship', self)
        relationship_action.triggered.connect(self.trigger_relationship)

        connect_line = QAction('Connect', self)
        connect_line.triggered.connect(self.trigger_connect)

        delete_action = QAction('Delete', self)
        delete_action.triggered.connect(self.trigger_delete)

        return exit_action, entity_action, attribute_action, relationship_action, connect_line, delete_action

    def create_toolbar(self):
        toolbar = self.addToolBar('TB')
        toolbar.setMovable(False)
        toolbar.addAction(self.exit_action)
        toolbar.addAction(self.entity_action)
        toolbar.addAction(self.attribute_action)
        toolbar.addAction(self.relationship_action)
        toolbar.addAction(self.connect_line)
        toolbar.addAction(self.delete_action)
        return toolbar


app = QApplication(sys.argv)
win = MainWin()

win.show()
sys.exit(app.exec_())



#view = GraphicView()

#view.show()
#sys.exit(app.exec_())