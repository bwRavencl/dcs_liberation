from PySide2.QtCore import QPoint, QRect, QPointF, Qt
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent

import qt_ui.uiconstants as CONST
from game import db
from theater import TheaterGroundObject, ControlPoint


class QMapGroundObject(QGraphicsRectItem):

    def __init__(self, parent, x: float, y: float, w: float, h: float, cp: ControlPoint, model: TheaterGroundObject, buildings=[]):
        super(QMapGroundObject, self).__init__(x, y, w, h)
        self.model = model
        self.cp = cp
        self.parent = parent
        self.setAcceptHoverEvents(True)
        self.setZValue(2)
        self.buildings = buildings
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations, False)

        if len(self.model.groups) > 0:
            units = {}
            for g in self.model.groups:
                print(g)
                for u in g.units:
                    if u.type in units.keys():
                        units[u.type] = units[u.type]+1
                    else:
                        units[u.type] = 1
            tooltip = "[" + self.model.obj_name + "]" + "\n"
            for unit in units.keys():
                tooltip = tooltip + str(unit) + "x" + str(units[unit]) + "\n"
            self.setToolTip(tooltip[:-1])
        else:
            tooltip = "[" + self.model.obj_name + "]" + "\n"
            for building in buildings:
                if not building.is_dead:
                    tooltip = tooltip + str(building.dcs_identifier) + "\n"
            self.setToolTip(tooltip[:-1])


    def paint(self, painter, option, widget=None):
        #super(QMapControlPoint, self).paint(painter, option, widget)

        playerIcons = "_blue"
        enemyIcons = ""

        if self.parent.get_display_rule("go"):
            painter.save()

            cat = self.model.category
            if cat == "aa" and self.model.sea_object:
                cat = "ship"

            if not self.model.is_dead and not self.cp.captured:
                painter.drawPixmap(option.rect, CONST.ICONS[cat + enemyIcons])
            elif not self.model.is_dead:
                painter.drawPixmap(option.rect, CONST.ICONS[cat + playerIcons])
            else:
                painter.drawPixmap(option.rect, CONST.ICONS["destroyed"])
            painter.restore()

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        self.update()
        self.setCursor(Qt.PointingHandCursor)

    def mouseMoveEvent(self, event:QGraphicsSceneMouseEvent):
        self.update()
        self.setCursor(Qt.PointingHandCursor)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent):
        self.update()

