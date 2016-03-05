from pydashie.libs.widget import DashingWidget

class ListWidget(DashingWidget):
    def process(self, dcList):
        '''
        Calculate the necessary values for a List to be sampler
        :return:
        '''
        if dcList and isinstance(dcList, dict):
            self.storage(dcList)
            arItems = list()
            for label, value in dcList:
                arItems.append({'label':label, 'value':value})
            self._send({'items': arItems})