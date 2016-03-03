import datetime
from repeated_timer import RepeatedTimer

class DashieSampler:
    def __init__(self, strName, objConnection, nInterval, settings=dict(), nSamples=2):
        self._dcSettings = settings
        self._strName = strName
        self._objConnection = objConnection

        self._nSamples = nSamples
        self._arStorage = list()
        self._objTimer = None
        self.start(nInterval)

    def __del__(self):
        self.stop()

    def last(self):
        '''
        Gets the last value sampled
        :return:
        '''
        if len(self._arStorage) > 1:
            return self._arStorage[-2]
        else:
            return None

    def storage(self, objValue):
        '''
        Store the value on the storage
        :param objValue: the Value to be Storaged
        :return: None
        '''
        self._arStorage.append(objValue)
        if len(self._arStorage) > self._nSamples:
            self._arStorage.pop(0)
        return None

    def getSetting(self, strKey, objDefault=None):
        '''
        Get the specific setting defined by the child calsses
        :param strKey: The name of the setting
        :param objDefault: the value to return if the setting doesnt exist
        :return:
        '''
        return self._dcSettings.get(strKey, objDefault)

    def start(self, nInterval):
        '''
        Start the interval sampler
        :param nInterval:
        :return:
        '''
        if nInterval > 0:
            self._objTimer = RepeatedTimer(nInterval, self._sample)

    def stop(self):
        '''
        Stop the Sampler from running in the interval
        :return:
        '''
        if self._objTimer:
            self._objTimer.stop()
            del self._objTimer
            self._objTimer = None

    def sample(self):
        '''
        Child class implements this function
        '''
        return None

    def process(self, objData):
        '''
        Process the Data To the Widdget
        :param objData:
        :return:
        '''
        if objData:
            self.storage(objData)
            self._send(objData)

    def _send(self, dcBody):
        '''
        Send data to the open connections. The 'updatedAt' tag is generated automaticaly.
        :param dcBody: A Dictonary with the data that will be sent
        :return:
        '''
        dcBody['id'] = self._strName
        dcBody['updatedAt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0000')
        return self._objConnection.send(dcBody)

    def _sample(self):
        '''
        Send the provided sample.
        :return:
        '''
        objData = self.sample()
        self.process(objData)

class NumberSampler(DashieSampler):
    def process(self, nValue):
        '''
        Calculate the necessary values for a Number to be sampler
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
            else: dcItem['alarm'] = False
            return self._send(dcItem)
        return False


class ListSampler(DashieSampler):
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


class ChartSampler(DashieSampler):
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


class MeterSampler(DashieSampler):
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


if __name__ == "__main__":
    pass