from pydashie.libs.widget import DashingWidget


class NumberWidget(DashingWidget):

    def process(self, nValue):
        '''
        Calculate the necessary values for a Number to be sampler
        :param nValue:
        :return:
        '''
        if nValue and isinstance(nValue, (int, long, float)):
            self.storage(nValue)
            dcItem = {
                'current': nValue,
                'last': self.last(),
                'more-info': 'Testing More Info'
            }
            if nValue > 50:
                dcItem['alarm'] = True
            else:
                dcItem['alarm'] = False
            return self._send(dcItem)
        return False
