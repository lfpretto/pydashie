from pydashie.libs.widget import DashingWidget
import datetime


class GraphWidget(DashingWidget):
    seedX = 0
    renderTemplate = ''

    def process(self, arItems):
        '''
        Calculate the necessary values for a List to be sampler
        :return:
        '''
        if arItems:
            if len(arItems) > 1:
                x = arItems[0]
                y = arItems[1]
            else:
                y = int(arItems[0])
                x = self.seedX #datetime.datetime.now().strftime('%H:%M')
            self.storage({'x': x, 'y': y})
            self._sendStorageAs('points')
            self.seedX += 1

