from pydashie.libs.widget import DashingWidget


class GraphWidget(DashingWidget):
    seedX = 0

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
                y = arItems[0]
                x = self.seedX
            self.storage({'x': x, 'y': y})
            self.seedX += 1
            return {'points': self._arStorage}

