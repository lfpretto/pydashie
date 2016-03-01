import datetime
from repeated_timer import RepeatedTimer

class DashieSampler:
    def __init__(self, strName, objConnection, nInterval, settings=dict()):
        self._objConnection = objConnection
        self._strName = strName
        if nInterval > 0 :
            self._objTimer = RepeatedTimer(nInterval, self._sample)
        self._dcSettings = settings

    def getSetting(self, strKey, objDefault=None):
        return self._dcSettings.get(strKey, objDefault)

    def start(self, nInterval):
        pass

    def stop(self):
        '''
        Stop the Sampler from running in the interval
        :return:
        '''
        self._objTimer.stop()

    def sample(self):
        '''
        Child class implements this function
        '''
        return {}

    def _send(self, dcBody):
        dcBody['id'] = self._strName
        dcBody['updatedAt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0000')
        self._objConnection.send(dcBody)

    def _sample(self):
        objData = self.sample()
        if objData:
            self._send(objData)


if __name__ == "__main__":
    pass