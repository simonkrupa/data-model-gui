import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QLabel, QGraphicsProxyWidget, QLineEdit
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

        self.pLineEdit = QLineEdit(text)
        self.pLineEdit.setFrame(False)
        self.pLineEdit.setGeometry(10, 35, 120, 35)
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
        self.rel = None

    def changePos(self, x, y):
        if self.att:
            uni_x, uni_y = self.att.getPos()
        elif self.rel:
            uni_x, uni_y = self.rel.getPos()
        self.setLine(x, y, uni_x, uni_y)

    def changeAttPos(self, att_x, att_y):
        x, y = self.entity.getPos()
        self.setLine(x, y, att_x, att_y+50)

    def changeRelPos(self, rel_x, rel_y):
        x, y = self.entity.getPos()
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

        self.scene = QGraphicsScene()
        self.setScene(self.scene)       
        self.setSceneRect(0, 0, 1200, 1000)

        self.moveObject = RectObject(50, 50, "Zviera")
        self.entity2 = RectObject(700, 400, "Clovek")
        self.moveObject2 = EllipseObject(300, 100, "telefonne cislo")
        self.att2 = EllipseObject(600, 100, "pohlavie")
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
        self.scene.addItem(self.entity2)
        self.scene.addItem(self.relLine)
        self.scene.addItem(self.att2)
        self.scene.addItem(self.line1)
        self.scene.addItem(self.line2)
        self.scene.addItem(self.relationship)
        self.scene.addItem(self.moveObject)
        self.scene.addItem(self.moveObject2)
        #self.scene.addItem(self.line)


app = QApplication(sys.argv)
view = GraphicView()

view.show()
sys.exit(app.exec_())