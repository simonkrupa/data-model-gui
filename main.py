import sys

from PyQt5.QtGui import QIcon, QFont, QColor, QPen, QPainter
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

        self.grid_group = None
        self.grid_flag = True
        self.align = False

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
            self.align = False
            self.start_point = None

    def mouseMoveEvent(self, event):
        if self.move_flag:
            if self.line_mouse_move is None:
                #point = self.mapToScene(int(self.start_point.x), int(self.start_point.y))
                point = QPoint(int(self.start_point.x), int(self.start_point.y))
                end_point = self.mapToScene(event.pos())
                #end_point = (event.pos())
                print(type(self.start_point))
                if isinstance(self.start_point, RelationshipObject):
                    if self.start_point.y >= int(end_point.y()):
                        self.line_mouse_move = QGraphicsLineItem(self.start_point.x, self.start_point.y,
                                                     int(end_point.x()),
                                                     int(end_point.y()))
                    elif self.start_point.y + 100 <= int(end_point.y()):
                        self.line_mouse_move = QGraphicsLineItem(self.start_point.x, self.start_point.y + 140,
                                                     int(end_point.x()),
                                                     int(end_point.y()))
                    elif int(end_point.y()) > self.start_point.y and self.start_point.y + 100 > int(
                            end_point.y()) and self.start_point.x < int(end_point.x()):
                        self.line_mouse_move = QGraphicsLineItem(self.start_point.x + 70, self.start_point.y + 70,
                                                     int(end_point.x()),
                                                     int(end_point.y()))
                    elif int(end_point.y()) > self.start_point.y and self.start_point.y + 100 > int(
                            end_point.y()) and self.start_point.x >= int(end_point.x()):
                        self.line_mouse_move = QGraphicsLineItem(self.start_point.x - 70, self.start_point.y + 70,
                                                     int(end_point.x()),
                                                     int(end_point.y()))
                    else:

                        self.line_mouse_move = QGraphicsLineItem(self.start_point.x, self.start_point.y, int(end_point.x()),
                                                     int(end_point.y()))
                else:
                    if self.start_point.y >= int(end_point.y()):
                        self.line_mouse_move = QGraphicsLineItem(int(self.start_point.x)+75, int(self.start_point.y), int(end_point.x()), int(end_point.y()))
                    elif self.start_point.y + 100 <= int(end_point.y()):
                        self.line_mouse_move = QGraphicsLineItem(int(self.start_point.x)+75, int(self.start_point.y)+100, int(end_point.x()),
                                                                 int(end_point.y()))
                    elif int(end_point.y()) > self.start_point.y and self.start_point.y + 100 > int(end_point.y()) and self.start_point.x < int(end_point.x()):
                        self.line_mouse_move = QGraphicsLineItem(int(self.start_point.x)+150, int(self.start_point.y)+50, int(end_point.x()),
                                                                 int(end_point.y()))
                    elif int(end_point.y()) > self.start_point.y and self.start_point.y + 100 > int(end_point.y()) and self.start_point.x >= int(end_point.x()):
                        self.line_mouse_move = QGraphicsLineItem(int(self.start_point.x), int(self.start_point.y)+50, int(end_point.x()),
                                                                 int(end_point.y()))
                    else:
                        print("smf")
                        self.line_mouse_move = QGraphicsLineItem(int(self.start_point.x()), int(self.start_point.y()), int(end_point.x()), int(end_point.y()))
                    print("xaxa")
                    print(end_point.x(), end_point.y())
                self.scene.addItem(self.line_mouse_move)
            else:
                end_point = self.mapToScene(event.pos())

                if self.prev:
                    if isinstance(self.start_point, RelationshipObject):
                        if self.start_point.y >= int(end_point.y()):
                            self.line_mouse_move.setLine(self.start_point.x , self.start_point.y,
                                                         int(end_point.x()),
                                                         int(end_point.y()))
                        elif self.start_point.y + 100 <= int(end_point.y()):
                            self.line_mouse_move.setLine(self.start_point.x, self.start_point.y + 140,
                                                         int(end_point.x()),
                                                         int(end_point.y()))
                        elif int(end_point.y()) > self.start_point.y and self.start_point.y + 100 > int(
                                end_point.y()) and self.start_point.x < int(end_point.x()):
                            self.line_mouse_move.setLine(self.start_point.x + 70, self.start_point.y + 70,
                                                         int(end_point.x()),
                                                         int(end_point.y()))
                        elif int(end_point.y()) > self.start_point.y and self.start_point.y + 100 > int(
                                end_point.y()) and self.start_point.x >= int(end_point.x()):
                            self.line_mouse_move.setLine(self.start_point.x -70, self.start_point.y + 70,
                                                         int(end_point.x()),
                                                         int(end_point.y()))
                        else:
                            self.line_mouse_move.setLine(self.start_point.x, self.start_point.y, int(end_point.x()),
                                                         int(end_point.y()))
                    else:
                        if self.start_point.y >= int(end_point.y()):
                            self.line_mouse_move.setLine(self.start_point.x+75, self.start_point.y, int(end_point.x()),
                                                                     int(end_point.y()))
                        elif self.start_point.y + 100 <= int(end_point.y()):
                            self.line_mouse_move.setLine(self.start_point.x+75, self.start_point.y + 100,
                                                                     int(end_point.x()),
                                                                     int(end_point.y()))
                        elif int(end_point.y()) > self.start_point.y and self.start_point.y + 100 > int(
                                end_point.y()) and self.start_point.x < int(end_point.x()):
                            self.line_mouse_move.setLine(self.start_point.x + 150, self.start_point.y + 50,
                                                                     int(end_point.x()),
                                                                     int(end_point.y()))
                        elif int(end_point.y()) > self.start_point.y and self.start_point.y + 100 > int(
                                end_point.y()) and self.start_point.x >= int(end_point.x()):
                            self.line_mouse_move.setLine(self.start_point.x, self.start_point.y + 50,
                                                                     int(end_point.x()),
                                                                     int(end_point.y()))
                        else:
                            print("ccc")
                            self.line_mouse_move.setLine(self.start_point.x, self.start_point.y, int(end_point.x()),
                                                                     int(end_point.y()))
                        print("meemem")
                        print(end_point.x(), end_point.y())
                    #self.line_mouse_move.setLine(self.start_point.x, self.start_point.y, end_point.x(), end_point.y())
                else:
                    self.scene.removeItem(self.line_mouse_move)
                    self.line_mouse_move = None
                    self.move_flag = False
                    return
        elif self.mode == 0:
            """if self.align:
                print(self.items(event.pos()))
                if self.items(event.pos()):
                    align_item = self.items(event.pos())
                    if isinstance(align_item[0], QGraphicsProxyWidget):
                        align_item = align_item[1]
                    elif isinstance(align_item[0], QGraphicsLineItem):
                        if len(align_item) > 2:
                            align_item = align_item[2]
                        elif len(align_item) == 1:
                            align_item = align_item[0]
                        else:
                            align_item = align_item[1]
                    line = None
                    line2 = None

                    print(align_item)
                    for item in self.items():
                        if line:
                            self.scene.removeItem(line)
                        if line2:
                            self.scene.removeItem(line2)
                        if item.x == align_item.x and item != align_item:
                            line = QGraphicsLineItem(item.x, item.y, align_item.x, align_item.y)
                            self.scene.addItem(line)
                        elif item.y == align_item.y and item != align_item:
                            line2 = QGraphicsLineItem(item.x, item.y, align_item.x, align_item.y)
                            self.scene.addItem(line2)
                    #self.scene.removeItem(line)
"""
            super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if self.mode == 4:
            item = self.items(event.pos())
            print(item)
            if item:
                self.move_flag = True
                print(type(item))
                if isinstance(item[0], QGraphicsProxyWidget):
                    item = item[1]
                elif isinstance(item[0], QGraphicsLineItem):
                    if len(item) > 2:
                        item = item[2]
                    elif len(item) == 1:
                        item = item[0]
                    else:
                        item = item[1]
                else:
                    item = item[0]
                print(item)
                self.start_point = item
                print(self.start_point)
                if item and self.prev:
                    self.move_flag = False
                    self.scene.removeItem(self.line_mouse_move)
                    self.line_mouse_move = None
                    self.start_point = None
                    if type(self.prev) != type(item):
                        connecting_line = ConnectingLine(self.prev.x, self.prev.y, 1, 1)
                        if isinstance(item, EllipseObject) or isinstance(self.prev, EllipseObject):
                            if isinstance(self.prev, RectObject) and isinstance(item, EllipseObject):
                                if not item.line:
                                    tmp = item
                                    item = self.prev
                                    self.prev = tmp
                                    item.addLine(connecting_line, self.prev)
                                    self.scene.addItem(connecting_line)
                            elif isinstance(item, RectObject) and isinstance(self.prev, EllipseObject):
                                if not self.prev.line:
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
                if isinstance(item, ConnectingLine):
                    if item.att:
                        item.att.line = None
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

                if isinstance(item, QGraphicsProxyWidget):
                    item.widget().setText(self.xt.input_text)
                else:
                    item.pMyItem.widget().setText(self.xt.input_text)

        elif self.mode == 0:
            if self.prev:
                self.prev = None
            if self.items(event.pos()):
                self.align = True

            print(event.pos())
            print(self.mapToScene(event.pos()))
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

    def grid(self):
        if self.grid_flag:
            ix = 0
            iy = 0
            pen = QPen(Qt.gray)
            self.grid_group = QGraphicsItemGroup()
            while iy < self.height():
                ly = QGraphicsLineItem(0, iy, self.width(), iy)
                ly.setPen(pen)
                self.grid_group.addToGroup(ly)
                iy = iy + 50
            while ix < self.width():
                lx = QGraphicsLineItem(ix, 0, ix, self.height())
                lx.setPen(pen)
                self.grid_group.addToGroup(lx)
                ix = ix + 50
            self.grid_group.setZValue(-1)
            self.scene.addItem(self.grid_group)
            self.grid_flag = False
        else:
            self.scene.removeItem(self.grid_group)
            self.grid_flag = True


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

        self.exit_action, self.entity_action, self.attribute_action, self.relationship_action, self.connect_line, self.delete_action, self.rename_action, self.basic_action, self.custom_action = self.toolbar_actions()
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

    def trigger_custom(self):
        self.mode_info.setText("Mód zarovnania")
        self.view.grid()

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

        custom_action = QAction('Custom', self)
        custom_action.triggered.connect(self.trigger_custom)

        return exit_action, entity_action, attribute_action, relationship_action, connect_line, delete_action, rename_action, basic_action, custom_action

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
        toolbar.addAction(self.custom_action)
        return toolbar


app = QApplication(sys.argv)
win = MainWin()
win.show()
sys.exit(app.exec_())



#view = GraphicView()

#view.show()
#sys.exit(app.exec_())