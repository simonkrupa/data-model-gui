import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QLabel, QGraphicsProxyWidget, QLineEdit
from PyQt5.QtCore import Qt, QPointF, QLineF


class RelationshipObject(QGraphicsRectItem):
    def __init__(self, x, y, r, h):
        super().__init__(0, 0, r, h)
        self.setPos(x, y)
        self.setRotation(45)
        self.setAcceptHoverEvents(True)

        self.pLineEdit = QLineEdit("Relationship 1")
        self.pLineEdit.setFrame(False)
        self.pLineEdit.setGeometry(0, 75, 105, 35)
        self.pMyItem = QGraphicsProxyWidget(self)
        self.pMyItem.setWidget(self.pLineEdit)
        self.pMyItem.setRotation(-45)

        self.entity = None

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))


    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))



class RectObject(QGraphicsRectItem):
    def __init__(self, x, y, r, h):
        super().__init__(0, 0, r, h)
        self.setPos(x, y)
        self.r = r
        self.h = h
        self.x = x
        self.y = y
        self.x1 = self.x + self.r
        self.y1 = self.y + self.h
        self.setAcceptHoverEvents(True)

        self.pLineEdit = QLineEdit("Entity 1")
        self.pLineEdit.setFrame(False)
        self.pLineEdit.setGeometry(x-(int(h/2))+1, y-(int(h/5)), r-1, int(h/2)-10)
        self.pMyItem = QGraphicsProxyWidget(self)
        self.pMyItem.setWidget(self.pLineEdit)
        self.line = None
        self.att = None

    def addLine(self, line, att):
        self.line = line
        self.att = att
        self.line.setEntity(self)
        self.att.setLine(line)
        self.line.setAtt(att)
        self.drawLine()

    def drawLine(self):
        if self.line:
            self.line.changePos(self.x1, self.y1-50)

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
    def __init__(self, x, y, r, h):
        super().__init__(0, 0, r, h)
        self.setPos(x, y)
        self.setAcceptHoverEvents(True)
        self.x = x
        self.y = y
        self.h = h
        self.line = None

        self.pLineEdit = QLineEdit("Attribute 1")
        self.pLineEdit.setFrame(False)
        self.pLineEdit.setGeometry(10, h-65, r-20, 35)
        self.pMyItem = QGraphicsProxyWidget(self)
        self.pMyItem.setWidget(self.pLineEdit)

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

    def changePos(self, x, y):
        att_x, att_y = self.att.getPos()
        print(x, y, att_x, att_y)
        self.setLine(x, y, att_x, att_y)

    def changeAttPos(self, att_x, att_y):
        x, y = self.entity.getPos()
        self.setLine(x, y, att_x, att_y+50)

    def setAtt(self, att):
        self.att = att

    def setEntity(self, entity):
        self.entity = entity

class GraphicView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)       
        self.setSceneRect(0, 0, 1200, 1000)

        self.moveObject = RectObject(50, 50, 150, 100)
        self.moveObject2 = EllipseObject(300, 100, 150, 100)
        self.relationship = RelationshipObject(500, 500, 100, 100)

        self.line1 = ConnectingLine(300, 300, 300, -20)

        self.moveObject.addLine(self.line1, self.moveObject2)

        self.scene.addItem(self.line1)
        self.scene.addItem(self.relationship)
        self.scene.addItem(self.moveObject)
        self.scene.addItem(self.moveObject2)
        #self.scene.addItem(self.line)


app = QApplication(sys.argv)
view = GraphicView()

view.show()
sys.exit(app.exec_())