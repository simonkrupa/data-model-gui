import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QLabel, QGraphicsProxyWidget, QLineEdit
from PyQt5.QtCore import Qt, QPointF, QLineF


class MovingObj():
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


class RectObject(QGraphicsRectItem, MovingObj):
    def __init__(self, x, y, r, h):
        super().__init__(0, 0, r, h)
        self.setPos(x, y)
        self.r = r
        self.h = h
        self.x = x
        self.setAcceptHoverEvents(True)

        self.pLineEdit = QLineEdit("Entity 1")
        self.pLineEdit.setFrame(False)
        self.pLineEdit.setGeometry(x-(int(h/2))+1, y-(int(h/5)), r-1, int(h/2)-10)
        self.pMyItem = QGraphicsProxyWidget(self)
        self.pMyItem.setWidget(self.pLineEdit)


class EllipseObject(QGraphicsEllipseItem, MovingObj):
    def __init__(self, x, y, r, h):
        super().__init__(0, 0, r, h)
        self.setPos(x, y)
        self.setAcceptHoverEvents(True)

        self.pLineEdit = QLineEdit("Attribute 1")
        self.pLineEdit.setFrame(False)
        self.pLineEdit.setGeometry(x-h+10, y-(int(r/2))+10, r-20, int(h/2)-15)
        self.pMyItem = QGraphicsProxyWidget(self)
        self.pMyItem.setWidget(self.pLineEdit)


class ConnectingLine(QGraphicsLineItem):
    def __init__(self, x, y, r, h):
        super().__init__(0, 0, r, h)
        self.setPos(x, y)



class GraphicView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)       
        self.setSceneRect(0, 0, 1200, 1000)

        self.moveObject = RectObject(50, 50, 150, 100)
        self.moveObject2 = EllipseObject(100, 100, 150, 100)

        #self.line = self.moveObject.connectAtt(self.moveObject2)
        self.line1 = ConnectingLine(300, 300, 300, 0)
        self.scene.addItem(self.line1)

        self.scene.addItem(self.moveObject)
        #self.scene.addItem(self.moveObject2)
        #self.scene.addItem(self.line)


app = QApplication(sys.argv)
view = GraphicView()

view.show()
sys.exit(app.exec_())