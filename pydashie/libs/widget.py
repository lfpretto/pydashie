import datetime


class DashingWidget:
    def __init__(self, strId, objConnection, dcSettings=dict()):
        self._objSampler = None
        self._strId = strId
        self._objConnection = objConnection
        self._dcSettings = dcSettings
        self._nSamples = dcSettings.get('samples', 2)
        self._arStorage = list()

    def __del__(self):
        self.stop()




    def get(self, strId):
        if strId in ('row', 'col', 'x', 'y'):
            objLayout = self._dcSettings.get('layout', None)
            if objLayout:
                return objLayout.get(strId, 1)
            else:
                return '1'
        else:
            return self._dcSettings.get(strId, '')

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
        dcBody['id'] = self._strId
        dcBody['updatedAt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print dcBody
        return self._objConnection.send(dcBody)

    def _sendStorageAs(self, strKey):
        print self._arStorage
        self._send({strKey: self._arStorage})

    def start(self):
        '''
        Loads and Start the Sampler configured for this Widget
        :return:
        '''
        dcSamplerSettings = self._dcSettings.get('sampler', False)
        if dcSamplerSettings:
            strType = dcSamplerSettings.get('type', None)
            if not strType:
                print 'Invalid Type'
                return False
            try:
                import importlib
                objModule = importlib.import_module("pydashie.samplers." + strType)
                objSamplerClass = getattr(objModule, strType.title() + "Sampler")
            except Exception as e:
                print e
                return False
            else:
                self._objSampler  = objSamplerClass(self, dcSamplerSettings)
                return self._objSampler.start()
        return True

    def stop(self):
        '''
        Stops the Sampler configured for the Widget
        :return:
        '''
        if self._objSampler:
            try:
                return self._objSampler.stop()
            except:
                del self._objSampler
            if self._objSampler:
                return False
        return True

    def __str__(self):
        strIcon = self._dcSettings.get('icon', None)
        strHTML = ''
        strHTML += '<li data-row="" data-col="" data-sizex="" data-sizey="">'
        strHTML += '<div data-id="{{w.id}}" data-view="{{w.type.title()}}" data-title="{{w.title}}"></div>'
        if strIcon:
            strHTML += '<i class="icon-{{w.icon}} icon-background"></i>'
        strHTML += '</li>'
        return strHTML

    def getTags(self):
        return dict()



