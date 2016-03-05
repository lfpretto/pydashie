class DashingSampler:
    '''
    Run a sample periodicatly in a set interval.
    '''
    def __init__(self, objWidget, settings=dict()):
        self._dcSettings = settings
        self._objWidget = objWidget

    def __del__(self):
        self.stop()

    def _process(self, objData):
        self._objWidget.process(objData)

    def get(self, strKey, objDefault=None):
        '''
        Get the specific setting defined by the child calsses
        :param strKey: The name of the setting
        :param objDefault: the value to return if the setting doesnt exist
        :return:
        '''
        return self._dcSettings.get(strKey, objDefault)

    def set(self, strKey, objValue):
        '''
        Changes a setting
        :param strKey: The name of the setting
        :param objValue: the value of the setting
        :return:
        '''
        self._dcSettings[strKey] = objValue

    def _start(self):
        '''
        Used to Create another Extensible Class
        :return:
        '''
        pass

    def start(self):
        '''
        Child class implements this function
        This runs at the start of the sampler
        '''
        self._start()
        pass

    def _stop(self):
        '''
        Used to Create another Extensible Class
        :return:
        '''
        pass

    def stop(self):
        '''
        Child class implements this function
        This runs at the end of the sampler
        '''
        self._stop()
        pass
