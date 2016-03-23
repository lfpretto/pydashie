""" Dashboard
"""
import os, json
from pydashie.libs.streams import ConnectionStreams


class DashingBoard:
    """ The Dashboard class controls all the widgets.
    """
    _dcWidgets = dict()

    def __init__(self, dcDefinitions):
        self._arWidgetSettings = dcDefinitions.get('widgets', list())
        self._arSamplerSettings = dcDefinitions.get('samplers', list())
        self._strId = dcDefinitions.get('id', 'test')
        self._strTitle = dcDefinitions.get('title', 'pyDashing')
        self._objStreams = ConnectionStreams()
        self._dcWidgets = dict()
        self._dcSamplers = dict()
        self._dcDefinitions = dcDefinitions
        self._arJavascript = list()
        self._arStyles = list()
        self._loadSamplers()
        self._loadWidgets()

    def __del__(self):
        self._unloadWidgets()

    def __str__(self):
        return json.dumps(self.getSettings())

    def getSettings(self):
        return {
            "id": self._strId,
            "title": self._strTitle,
            "widgets": list(self._dcWidgets[w].getSettings() for w in self._dcWidgets),
            "samplers": list(self._dcSamplers[w].getSettings() for w in self._dcSamplers)
        }

    def updateLayout(self, arLayout):
        '''
        Args:
            arLayout:

        Returns:

        '''
        bReturn = True
        for dcLayout in arLayout:
            strId = dcLayout.pop('id')
            objWidget = self._dcWidgets.get(strId, None)
            if objWidget:
                objWidget.updateLayout(dcLayout)
            else:
                bReturn = False
        self.refresh()
        return bReturn

    def refresh(self):
        """

        Returns:

        """
        objReload = {"id": 'dashing-internal-functions',
                     "action": "reload",
                     "updatedAt": 1}
        return self._objStreams.send(objReload, False)


    def stop(self):
        """
        Returns:

        """
        self._unloadSamplers()
        self._unloadWidgets()

    def push(self, strURL, objContent):
        """

        Args:
            strSamplerId:
            objData:

        Returns:

        """
        from pydashie.samplers.push import PushSampler
        for objSampler in self._dcSamplers.values():
            if isinstance(objSampler, PushSampler):
                objResponse = objSampler.received(strURL, objContent)
                if objResponse:
                    return objResponse
        return False

    def render(self, bDebug=False):
        pass

    def getWidget(self, strId=None):
        if strId:
            return self._dcWidgets.get(strId, None)
        else:
            return self._dcWidgets.values()

    def _linkWidget(self, objWidget, dcSamplerSettings):
        strId = dcSamplerSettings.get('id', None)
        strValue = dcSamplerSettings.get('key', None)
        if strId in self._dcSamplers:
            self._dcSamplers[strId].addWidget(objWidget, strValue)

    def _unloadWidgets(self):
        """
        Returns:

        """
        print self._dcWidgets
        while len(self._dcWidgets) > 0:
            strKey, objWidget = self._dcWidgets.popitem()  # [strKey]
            if not objWidget.stop():
                print 'Error Deleting', strKey, 'Sampler'
                del objWidget
        self._dcWidgets = dict()

    def _loadWidgets(self):
        """
        Returns:

        """
        for dcWidget in self._arWidgetSettings:
            if self.startWidget(dcWidget):
                strType = dcWidget.get('type')
                strPath = os.path.join('widgets', strType, strType)
                self._arJavascript.append(strPath + '.js')
                self._arStyles.append(strPath + '.css')
            else:
                print 'not Loaded'

    def startWidget(self, dcSettings):
        """
        Args:
            dcSettings:

        Returns:

        """
        strId = dcSettings.get('id', None)
        strType = dcSettings.get('type', 'Number')
        try:
            import importlib
            objModule = importlib.import_module("pydashie.widgets." + strType)
            objWidgetClass = getattr(objModule, strType.title() + "Widget")
            objWidget = objWidgetClass(strId, self._objStreams, dcSettings)
        except Exception as e:
            print e
            return False
        else:
            self._addWidget(strId, objWidget)
            dcSampler = dcSettings.get('sampler', None)
            if dcSampler:
                self._linkWidget(objWidget, dcSampler)
            return True

    def _addWidget(self, strID, objWidget):
        """
        Args:
            strID:
            objWidget:

        Returns:

        """
        if objWidget:
            if strID in self._dcWidgets:
                objCurrentWidget = self._dcWidgets[strID]
                del objCurrentWidget
            self._dcWidgets[strID] = objWidget
            return True
        return False



    def _unloadSamplers(self):
        """
        Returns:

        """
        while len(self._dcSamplers) > 0:
            strKey, objSampler = self._dcSamplers.popitem()
            if not objSampler.stop():
                print 'Error Deleting', strKey, 'Sampler'
                del objSampler
        self._dcSamplers = dict()

    def _loadSamplers(self):
        """
        Returns:

        """
        for dcSampler in self._arSamplerSettings:
          self.startSampler(dcSampler)


    def startSampler(self, dcSettings):
        """ Runs the Widget SAMPLER based on the 'sampler' configs in the settings.

        Returns:
            True if successful, False otherwise
        """
        strId = dcSettings.get('id', None)
        strType = dcSettings.get('type', None)
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
            objSampler = objSamplerClass(self, dcSettings)
            #return self._objSampler.start()
        if objSampler.start():
            self._addSampler(strId, objSampler)
            return True
        else:
            return False

    def _addSampler(self, strID, objSampler):
        """
        Args:
            strID:
            objWidget:

        Returns:

        """
        if objSampler:
            if strID in self._dcSamplers:
                objCurrentWidget = self._dcSamplers[strID]
                del objCurrentWidget
            self._dcSamplers[strID] = objSampler
            return True
        return False




