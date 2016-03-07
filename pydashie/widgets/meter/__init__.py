from pydashie.libs.widget import DashingWidget

class MeterWidget(DashingWidget):
    def getTags(self):
        return {'data-min':"0", 'data-max': 200}

    def process(self, nValue):
        '''
        Calculate the necessary values for a Number to be sampler
        :return:
        '''
        if nValue and isinstance(nValue, (int, long, float)):
            self.storage(nValue)
            dcItem = {
                'value': nValue,
                'more-info': 'Testing info'
            }
            self._send(dcItem)

