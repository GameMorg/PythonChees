import sys
from PyQt5.QtCore import Qt, QRectF, QTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem


class Ball(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.x_speed = 5
        self.y_speed = 5

    def boundingRect(self):
        return QRectF(-10, -10, 20, 20)

    def paint(self, painter, option, widget):
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(-10, -10, 20, 20)

    def advance(self, phase):
        if not phase:
            return

        self.setPos(self.x() + self.x_speed, self.y() + self.y_speed)

        if self.x() <= -250 or self.x() >= 250:
            self.x_speed = -self.x_speed

        if self.y() <= -250 or self.y() >= 250:
            self.y_speed = -self.y_speed


class Paddle(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.rect = QRectF(-50, -5, 100, 10)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        return QRectF(-50, -5, 100, 10)

    def paint(self, painter, option, widget):
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(self.rect)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.setPos(event.scenePos().x(), self.y())


class Game(QGraphicsView):
    def __init__(self):
        super().__init__()
        scene = QGraphicsScene()
        scene.setSceneRect(-300, -300, 600, 600)
        self.setScene(scene)
        ball = Ball()

        paddle = Paddle()
        scene.addItem(ball)
        scene.addItem(paddle)
        paddle.setPos(0, -250)
        timer = QTimer(self)
        timer.timeout.connect(scene.advance)
        timer.start(int(1000 / 60))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())
