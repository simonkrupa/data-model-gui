import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon, QFont, QColor, QPen, QPainter, QPolygonF
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, \
    QGraphicsLineItem, QGraphicsTextItem, QLabel, QGraphicsProxyWidget, QLineEdit, QMainWindow, QAction, qApp, \
    QListWidget, QListWidgetItem, QGraphicsItemGroup, QPushButton, QVBoxLayout, QPlainTextEdit, QTextEdit, QMessageBox, \
    QDialog, QWidget, QHBoxLayout, QActionGroup, QGraphicsPolygonItem, QScrollBar
from PyQt5.QtCore import Qt, QPointF, QLineF, QPoint, QSize, QRectF


class RelationshipObject(QGraphicsRectItem):
    def __init__(self, x, y, text):
        self.r = 106
        self.h = 106
        super().__init__(0, 0, self.r, self.h)
        self.setPos(x, y)
        self.setRotation(45)
        self.setAcceptHoverEvents(True)
        self.x = x
        self.y = y
        self.grid = False
        self.grid_x = None
        self.grid_y = None

        self.align_pen = QPen()
        self.align_pen.setWidth(3)
        self.align_pen.setColor(Qt.blue)
        self.name1 = QLabel(text)
        self.name1.setGeometry(-20, 60, 115, 80)
        self.name1.setWordWrap(True)

        self.setBrush(QColor("white"))
        self.name1.setStyleSheet("QLabel { background-color : rgba(200,100,120, 0%); }")
        self.name1.setAlignment(Qt.AlignCenter)
        self.name1.setFrameStyle(0)

        self.pMyItem = QGraphicsProxyWidget(self)
        self.pMyItem.setWidget(self.name1)

        self.pMyItem.setRotation(-45)

        self.entity = None
        self.lines = []

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + self.x
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + self.y

        if self.grid:
            g_x = self.grid_x%25
            act_x = updated_cursor_x%25
            g_y = self.grid_y % 25
            act_y = updated_cursor_y % 25
            if 5 >= act_x - g_x >= -5 and 5 >= act_y - g_y >= -5:
                self.setPos(QPointF(updated_cursor_x-(act_x-g_x), updated_cursor_y-(act_y-g_y)))
                self.x = updated_cursor_x
                self.y = updated_cursor_y
                self.setPen(self.align_pen)
            else:
                self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
                self.x = updated_cursor_x
                self.y = updated_cursor_y
                self.setPen(Qt.black)
        else:
            self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
            self.x = updated_cursor_x
            self.y = updated_cursor_y
            self.setPen(Qt.black)
        for line in self.lines:
            line.changeRelPos(self.x, self.y)


    def adjust_lines(self):
        for line in self.lines:
            line.changeRelPos(self.x, self.y)


    def mouseReleaseEvent(self, event):
        pass

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

        self.align_pen = QPen()
        self.align_pen.setWidth(5)
        self.align_pen.setColor(Qt.blue)

        self.tmp_x = None
        self.tmp_y = None

        self.grid = False
        self.grid_x = None
        self.grid_y = None

        self.name1 = QLabel(text)
        self.name1.setGeometry(1, 1, 149, 99)
        self.name1.setWordWrap(True)
        self.setBrush(QColor("white"))
        self.name1.setStyleSheet("QLabel { background-color : rgba(200,100,120, 0%); }")
        self.name1.setAlignment(Qt.AlignCenter)
        self.name1.setFrameStyle(0)

        self.pMyItem = QGraphicsProxyWidget(self)
        self.pMyItem.setWidget(self.name1)
        self.lines = []
        self.relLines = []

    def setMyPosition(self, x, y):
        self.x = x
        self.y = y
        self.x1 = self.x + self.r
        self.y1 = self.y + self.h

    def addRelLine(self, line, rel):
        self.relLines.append(line)
        rel.setLine(line)
        line.setEntity(self)
        line.setRel(rel)
        self.drawLine()

    def addLine(self, line, att):
        self.lines.append(line)
        att.setLine(line)
        line.setEntity(self)
        line.setAtt(att)
        self.drawLine()

    def drawLine(self):
        for line in self.lines:
            line.changePos(self.x1, self.y1-50)

        for relLine in self.relLines:
            relLine.changePos(self.x1, self.y1-50)

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()
        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + self.x
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + self.y

        if self.grid:
            g_x = self.grid_x % 25
            act_x = updated_cursor_x % 25
            g_y = self.grid_y % 25
            act_y = updated_cursor_y % 25
            if 10 >= act_x - g_x >= -10 and 10 >= act_y - g_y >= -10:
                self.setPos(QPointF(updated_cursor_x-(act_x-g_x), updated_cursor_y-(act_y-g_y)))
                self.tmp_x = updated_cursor_x-(act_x-g_x)
                self.tmp_y = updated_cursor_y-(act_y-g_y)
                self.x = updated_cursor_x
                self.y = updated_cursor_y
                self.x1 = updated_cursor_x + self.r
                self.y1 = updated_cursor_y + self.h
                self.setPen(self.align_pen)
            else:
                self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
                self.x = updated_cursor_x
                self.y = updated_cursor_y
                self.x1 = updated_cursor_x + self.r
                self.y1 = updated_cursor_y + self.h
                self.setPen(Qt.black)
        else:
            self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
            self.x = updated_cursor_x
            self.y = updated_cursor_y
            self.x1 = updated_cursor_x + self.r
            self.y1 = updated_cursor_y + self.h
            self.setPen(Qt.black)
        self.drawLine()



    def mouseReleaseEvent(self, event):
        pass

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

        self.grid = False
        self.grid_x = None
        self.grid_y = None

        self.align_pen = QPen()
        self.align_pen.setWidth(5)
        self.align_pen.setColor(Qt.blue)

        self.text = text

        self.name1 = QLabel(text)
        self.name1.setGeometry(0, 0, 150, 100)
        self.name1.setWordWrap(True)

        self.setBrush(QColor("white"))
        self.name1.setStyleSheet("QLabel { background-color : rgba(200,100,120, 0%); }")
        self.name1.setAlignment(Qt.AlignCenter)
        self.name1.setFrameStyle(0)

        self.pMyItem = QGraphicsProxyWidget(self)
        self.pMyItem.setWidget(self.name1)


    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + self.x
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + self.y

        act_x = updated_cursor_x % 25
        act_y = updated_cursor_y % 25
        if self.grid:
            g_x = self.grid_x % 25
            g_y = self.grid_y % 25
            if 10 >= act_x - g_x >= -10 and 10 >= act_y - g_y >= -10:
                self.setPos(QPointF(updated_cursor_x-(act_x-g_x), updated_cursor_y-(act_y-g_y)))
                self.x = updated_cursor_x
                self.y = updated_cursor_y
                self.setPen(self.align_pen)
            else:
                self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
                self.x = updated_cursor_x
                self.y = updated_cursor_y
                self.setPen(Qt.black)
        else:
            self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
            self.x = updated_cursor_x
            self.y = updated_cursor_y
            self.setPen(Qt.black)
        if self.line:
            self.line.changeAttPos(self.x, self.y)

    def mouseReleaseEvent(self, event):
        pass

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
                self.setLine(x, y, uni_x, uni_y)
        elif self.rel:
            uni_x, uni_y = self.rel.getPos()
            if uni_y - 50 <= y + 50 and y - 50 <= uni_y + 50 and x > uni_x:
                self.setLine(x - 150, y, uni_x + 75, uni_y + 23)
            elif uni_y - 50 <= y + 50 and y - 50 <= uni_y + 50 and x < uni_x:
                self.setLine(x, y, uni_x - 75, uni_y + 23)
            elif y > uni_y + 50:
                self.setLine(x - 75, y - 50, uni_x, uni_y + 97)
            elif y < uni_y - 50:
                self.setLine(x - 75, y + 50, uni_x, uni_y - 53)
            else:
                self.setLine(x, y, uni_x, uni_y)

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
        if y > rel_y-53 and rel_y+53 > y - 150 and rel_x < x - 150:
            self.setLine(x-150, y, rel_x+75,rel_y+75)
        elif y > rel_y-53 and rel_y+53 > y - 150 and rel_x > x:
            self.setLine(x, y, rel_x-75, rel_y+75)
        elif rel_y < y-100:
            self.setLine(x-75, y-50, rel_x,rel_y+150)
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

class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.visibility = False
        self.x_max = None
        self.x_min = None
        self.y_max = None
        self.y_min = None

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF) -> None:
        painter.setOpacity(0.1)
        r = rect.toRect()
        self.x_min = r.left() - r.left() % 25 - 25
        self.y_min = r.top() - r.top() % 25 - 25
        self.x_max = r.right() - r.right() % 25 + 25
        self.y_max = r.bottom() - r.bottom() % 25 + 25
        if self.visibility:
            for x in range(self.x_min, self.x_max, 25):
                painter.drawLine(x, r.top(), x, r.bottom())
            for y in range(self.y_min, self.y_max, 25):
                painter.drawLine(r.left(), y, r.right(), y)


class GraphicView(QGraphicsView):
    def __init__(self, x):
        super().__init__(x)

        self.grid_group = None
        self.grid_flag = True
        self.align = False

        self.scroll_bar = QScrollBar()
        self.grid_point_x = None
        self.grid_point_y = None

        self.move_flag = False
        self.start_point = None
        self.line_mouse_move = None
        self.xt = None
        self.mode = 0
        self.prev = None
        self.scene = GraphicsScene()
        self.setScene(self.scene)
        self.maximumViewportSize()

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

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF) -> None:
        super().drawBackground(painter, rect)

    def drawObjects(self, entities, relationships):
        self.entityObjects = []
        self.entities = entities
        i = 50
        j = 100
        j2 = 50
        for entity in entities:
            entityObject = RectObject(i, 200, entity.word)
            self.entityObjects.append(entityObject)
            i = i+200
            self.scene.addItem(entityObject)
            for att in entity.attributes:
                attObject = EllipseObject(j, j2, att)
                line = ConnectingLine(300, 300, 300, -20)
                entityObject.addLine(line, attObject)
                j = j + 180
                self.scene.addItem(line)
                self.scene.addItem(attObject)

        i = 100
        for relationship in relationships:
            relationshipObject = RelationshipObject(i, 400, relationship.word)
            for entity in relationship.entities:
                for entityObject in self.entityObjects:
                    if entity.word == entityObject.text:
                        line = ConnectingLine(300, 300, 300, -20)
                        entityObject.addRelLine(line, relationshipObject)
                        self.scene.addItem(line)
            i = i+200
            self.scene.addItem(relationshipObject)


    def mouseReleaseEvent(self, event):
        for item in self.items():
            if isinstance(item, (RelationshipObject, RectObject, EllipseObject)):
                item.setPen(Qt.black)
        if self.mode == 7:
            items = self.items(event.pos())
            for item in items:
                if isinstance(item, RelationshipObject):
                    for line in item.lines:
                        line.changeRelPos(item.pos().x(), item.pos().y())
                if isinstance(item, (EllipseObject, RectObject)):
                    if isinstance(item, EllipseObject):
                        if item.line:
                            item.line.changeAttPos(item.pos().x(), item.pos().y())
                    if isinstance(item, RectObject):
                        if item.lines and item.tmp_x:
                            item.setPos(item.tmp_x, item.tmp_y)
                            item.setMyPosition(item.tmp_x, item.tmp_y)
                        if item.relLines and item.tmp_x:
                            item.setPos(item.tmp_x, item.tmp_y)
                            item.setMyPosition(item.tmp_x, item.tmp_y)
                            for l in item.relLines:
                                l.rel.adjust_lines()
                        for i in self.items():
                            if isinstance(i, EllipseObject):
                                if i.line:
                                    i.line.changeAttPos(i.pos().x(), i.pos().y())
                            if isinstance(i, RelationshipObject):
                                for line in i.lines:
                                    line.changeRelPos(i.pos().x(), i.pos().y())

        if self.mode == 0:
            self.align = False
            self.start_point = None

    def mouseMoveEvent(self, event):
        if self.move_flag:
            if self.line_mouse_move is None:
                point = QPoint(int(self.start_point.x), int(self.start_point.y))
                end_point = self.mapToScene(event.pos())
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
                        self.line_mouse_move = QGraphicsLineItem(int(self.start_point.x()), int(self.start_point.y()), int(end_point.x()), int(end_point.y()))
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
                            self.line_mouse_move.setLine(self.start_point.x, self.start_point.y + 150,
                                                         int(end_point.x()),
                                                         int(end_point.y()))
                        elif int(end_point.y()) > self.start_point.y and self.start_point.y + 100 > int(
                                end_point.y()) and self.start_point.x < int(end_point.x()):
                            self.line_mouse_move.setLine(self.start_point.x + 75, self.start_point.y + 75,
                                                         int(end_point.x()),
                                                         int(end_point.y()))
                        elif int(end_point.y()) > self.start_point.y and self.start_point.y + 100 > int(
                                end_point.y()) and self.start_point.x >= int(end_point.x()):
                            self.line_mouse_move.setLine(self.start_point.x - 75, self.start_point.y + 75,
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
                            self.line_mouse_move.setLine(self.start_point.x, self.start_point.y, int(end_point.x()),
                                                                     int(end_point.y()))
                else:
                    self.scene.removeItem(self.line_mouse_move)
                    self.line_mouse_move = None
                    self.move_flag = False
                    return
        elif self.mode == 0:
            super().mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if self.mode == 4:
            item = self.items(event.pos())
            if item:
                self.move_flag = True
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
                self.start_point = item
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
                if isinstance(item, ConnectingLine):
                    if item.att:
                        item.att.line = None
                if isinstance(item, EllipseObject):
                    if item.line:
                        self.scene.removeItem(item.line)
                elif isinstance(item, RectObject):
                    if item.lines:
                        for i in item.lines:
                            self.scene.removeItem(i)
                    if item.relLines:
                        for r in item.relLines:
                            self.scene.removeItem(r)
                elif isinstance(item, RelationshipObject):
                    if item.lines:
                        for i in item.lines:
                            self.scene.removeItem(i)
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
                    if self.xt.success == 0:
                        print(self.xt.result())
                        item.widget().setText(self.xt.input_text)
                        item.widget().setAlignment(Qt.AlignCenter)
                else:
                    if self.xt.success == 0:
                        item.pLineEdit.setText(self.xt.input_text)
                        item.pLineEdit.setAlignment(Qt.AlignCenter)

        elif self.mode == 0:
            if self.prev:
                self.prev = None
            if self.items(event.pos()):
                self.align = True

            super().mousePressEvent(event)
            self.start_point = self.items(event.pos())
        elif self.mode == 7:
            super().mousePressEvent(event)
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
        r = self.scene.items()
        for item in r:
            if isinstance(item, (RectObject, EllipseObject, RelationshipObject)):
                item.grid = False
        if not self.grid_flag:
            self.grid()

    def call_aligning(self):
        self.mode = 7
        r = self.scene.items()
        for item in r:

            if isinstance(item, (RectObject, EllipseObject, RelationshipObject)):
                item.grid = True
                item.grid_x = self.scene.x_min
                item.grid_y = self.scene.y_min

    def grid(self):
        if self.scene.visibility:
            self.scene.visibility = False
            self.scene.update()
        else:
            self.scene.visibility = True
            self.scene.update()

    def t_align(self):
        if self.grid_flag:
            print("aaa")
        else:
            items = self.scene.items()
            for item in items:
                if isinstance(item, RelationshipObject):
                    self.grid_point_y.y()
                    new_x = item.pos().x() + (self.grid_point_x.x() % 25 - item.pos().x() % 25)
                    new_y = item.pos().y() + (self.grid_point_y.y() % 25 - item.pos().y() % 25)
                    item.setPos(new_x, new_y)
                    item.setMyPosition(new_x, new_y)
                    item.adjust_lines()
                if isinstance(item, (EllipseObject, RectObject)):
                    new_x = item.pos().x() + (self.grid_point_x.x() % 25 - item.pos().x() % 25)
                    new_y = item.pos().y() + (self.grid_point_y.y() % 25 - item.pos().y() % 25)
                    item.setPos(new_x, new_y)
                    item.setMyPosition(new_x, new_y)
                    if isinstance(item, RectObject):
                        if item.lines:
                            item.drawLine()
                        if item.relLines:
                            for l in item.relLines:
                                l.adjust_lines()



class QTextBox(object):
    pass


class PopUp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zvoľte názov")

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.success = 1
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
        if self.result() == 0:
            self.success = 0
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

        self.setWindowTitle("Generátor dátového modelu")
        self.setGeometry(0, 0, 1280, 800)

        self.mlayout = QVBoxLayout()
        self.mlayout.setSpacing(10)
        self.mlayout.setContentsMargins(0,5,0,0)
        self.widget = QWidget()
        self.widget.setLayout(self.mlayout)
        self.setCentralWidget(self.widget)

        self.view = GraphicView(self)
        self.mlayout.addWidget(self.view, 2)

        self.action_group = None
        self.last_checked = None

        self.mode_info = QLabel("Základný mód")
        self.mode_info.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(15)
        self.mode_info.setFont(font)
        self.mlayout.addWidget(self.mode_info)

        self.entity_action, self.attribute_action, self.relationship_action, self.connect_line, self.delete_action, self.rename_action, self.basic_action, self.custom_action, self.aligning_action, self.clear_action = self.toolbar_actions()
        self.toolbar = self.create_toolbar()

        self.start_button = QPushButton("Štart")
        # self.start_button.clicked.connect(self.start_data_model)
        self.start_button.setMinimumSize(100, 100)
        self.mlayout.addWidget(self.start_button)
        self.delete_button = QPushButton("Vymazať text")
        self.delete_button.setMinimumSize(100, 100)
        self.delete_button.clicked.connect(self.delete_text)
        self.mlayout.addWidget(self.delete_button)


        self.button_panel = ButtonPanel()
        self.button_panel.button_layout.addWidget(self.start_button)
        self.button_panel.button_layout.addWidget(self.delete_button)
        self.mlayout.addWidget(self.button_panel)

        self.text_area = QPlainTextEdit(self)
        font = QFont()
        font.setPointSize(12)
        self.text_area.setFont(font)
        self.text_area.setPlaceholderText("Zadajte text.")
        self.button_panel.hlayout.addWidget(self.text_area)

    # def start_data_model(self):
    #     # dmg = DataModelGenerator()
    #     # entities, relationships = dmg.generate_model(self.text_area.toPlainText())
    #     # self.view.drawObjects(entities, relationships)

    def quit_app(self):
        app.quit()

    def clear_view(self):
        self.view.scene.clear()

    def delete_text(self):
        self.text_area.clear()

    def trigger_delete(self):
        self.mode_info.setText("Mód mazania")
        if self.action_group.checkedAction() == self.delete_action:
            if self.last_checked == self.delete_action:
                self.delete_action.setChecked(False)
                if self.move_action_group.checkedAction() == self.aligning_action:
                    self.trigger_aligning()
                else:
                    self.trigger_basic()
            else:
                self.last_checked = self.delete_action
                self.view.delete()

    def trigger_entity(self):
        self.mode_info.setText("Mód tvorby entít")
        if self.action_group.checkedAction() == self.entity_action:
            if self.last_checked == self.entity_action:
                self.entity_action.setChecked(False)
                if self.move_action_group.checkedAction() == self.aligning_action:
                    self.trigger_aligning()
                else:
                    self.trigger_basic()
            else:
                self.last_checked = self.entity_action
                self.view.add_entity()

    def trigger_connect(self):
        self.mode_info.setText("Mód spájania prvkov")
        if self.action_group.checkedAction() == self.connect_line:
            if self.last_checked == self.connect_line:
                self.connect_line.setChecked(False)
                if self.move_action_group.checkedAction() == self.aligning_action:
                    self.trigger_aligning()
                else:
                    self.trigger_basic()
            else:
                self.last_checked = self.connect_line
                self.view.add_connect()

    def trigger_attribute(self):
        self.mode_info.setText("Mód tvorby atribútov")
        if self.action_group.checkedAction() == self.attribute_action:
            if self.last_checked == self.attribute_action:
                self.attribute_action.setChecked(False)
                if self.move_action_group.checkedAction() == self.aligning_action:
                    self.trigger_aligning()
                else:
                    self.trigger_basic()
            else:
                self.last_checked = self.attribute_action
                self.view.add_attribute()

    def trigger_relationship(self):
        self.mode_info.setText("Mód tvorby vzťahov")
        if self.action_group.checkedAction() == self.relationship_action:
            if self.last_checked == self.relationship_action:
                self.relationship_action.setChecked(False)
                if self.move_action_group.checkedAction() == self.aligning_action:
                    self.trigger_aligning()
                else:
                    self.trigger_basic()
            else:
                self.last_checked = self.relationship_action
                self.view.add_relationship()

    def trigger_rename(self):
        self.mode_info.setText("Mód premenovania prvkov")
        if self.action_group.checkedAction() == self.rename_action:
            if self.last_checked == self.rename_action:
                self.rename_action.setChecked(False)
                if self.move_action_group.checkedAction() == self.aligning_action:
                    self.trigger_aligning()
                else:
                    self.trigger_basic()
            else:
                self.last_checked = self.rename_action
                self.view.rename()

    def trigger_basic(self):
        self.mode_info.setText("Základný mód")
        self.last_checked = self.basic_action
        if self.action_group.checkedAction():
            self.action_group.checkedAction().setChecked(False)
        self.view.basic()

    def trigger_custom(self):
        if not self.view.scene.visibility:
            self.custom_action.setChecked(True)
            self.view.grid()
        else:
            self.custom_action.setChecked(False)
            self.view.grid()

    def trigger_align(self):
        self.view.t_align()

    def trigger_aligning(self):
        self.mode_info.setText(("Mód zarovnávania"))
        if self.move_action_group.checkedAction() == self.aligning_action:
            if self.last_checked == self.aligning_action:
                self.basic_action.setChecked(True)
                self.trigger_basic()
            else:
                self.last_checked = self.aligning_action
                self.view.call_aligning()
                if self.view.grid_group:
                    self.view.grid_group.setVisible(False)
            if self.action_group.checkedAction():
                self.action_group.checkedAction().setChecked(False)

    def toolbar_actions(self):

        clear_action = QAction('Vymazať scénu', self)
        clear_action.triggered.connect(self.clear_view)

        entity_action = QAction('Entita', self)
        entity_action.triggered.connect(self.trigger_entity)
        entity_action.setCheckable(True)

        attribute_action = QAction('Atribút', self)
        attribute_action.triggered.connect(self.trigger_attribute)
        attribute_action.setCheckable(True)

        relationship_action = QAction('Vzťah', self)
        relationship_action.triggered.connect(self.trigger_relationship)
        relationship_action.setCheckable(True)

        connect_line = QAction('Pripojiť', self)
        connect_line.triggered.connect(self.trigger_connect)
        connect_line.setCheckable(True)

        delete_action = QAction('Vymazať', self)
        delete_action.triggered.connect(self.trigger_delete)
        delete_action.setCheckable(True)

        rename_action = QAction('Premenovať', self)
        rename_action.triggered.connect(self.trigger_rename)
        rename_action.setCheckable(True)

        basic_action = QAction('Presúvať', self)
        basic_action.setShortcut(Qt.Key_Escape)
        basic_action.triggered.connect(self.trigger_basic)
        basic_action.setCheckable(True)
        basic_action.setChecked(True)

        custom_action = QAction('Mriežka', self)
        custom_action.triggered.connect(self.trigger_custom)
        custom_action.setCheckable(True)

        aligning_action = QAction('Zarovnávanie', self)
        aligning_action.triggered.connect(self.trigger_aligning)
        aligning_action.setCheckable(True)

        return entity_action, attribute_action, relationship_action, connect_line, delete_action, rename_action, basic_action, custom_action, aligning_action, clear_action

    def create_toolbar(self):
        toolbar = self.addToolBar('TB')
        toolbar.setMovable(False)

        toolbar.addAction(self.entity_action)
        toolbar.addAction(self.attribute_action)
        toolbar.addAction(self.relationship_action)
        toolbar.addAction(self.connect_line)
        toolbar.addAction(self.delete_action)
        toolbar.addAction(self.clear_action)
        toolbar.addAction(self.rename_action)
        toolbar.addSeparator()

        toolbar.addAction(self.basic_action)
        toolbar.addAction(self.aligning_action)
        toolbar.addSeparator()

        toolbar.addAction(self.custom_action)

        self.move_action_group = QActionGroup(toolbar)
        self.move_action_group.addAction(self.aligning_action)
        self.move_action_group.addAction(self.basic_action)

        self.action_group = QActionGroup(toolbar)
        self.action_group.setExclusive(True)
        self.action_group.addAction(self.entity_action)
        self.action_group.addAction(self.attribute_action)
        self.action_group.addAction(self.relationship_action)
        self.action_group.addAction(self.connect_line)
        self.action_group.addAction(self.delete_action)
        self.action_group.addAction(self.rename_action)
        return toolbar


app = QApplication(sys.argv)
win = MainWin()
win.show()
sys.exit(app.exec_())


