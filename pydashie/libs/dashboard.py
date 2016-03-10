import os
from pydashie.libs.streams import ConnectionStreams


class DashingBoard:
    _dcWidgets = dict()

    def __init__(self, dcDefinitions):
        self._arWidgetSettings = dcDefinitions.get('widgets', list())
        self._strId = dcDefinitions.get('id', 'test')
        self._strTitle = dcDefinitions.get('title', 'pyDashing')
        self._objStreams = ConnectionStreams()
        self._dcWidgets = dict()
        self._dcDefinitions = dcDefinitions
        self._arJavascript = list()
        self._arStyles = list()
        self._loadWidgets()

    def __del__(self):
        self._unloadWidgets()

    def updateLayout(self, arLayout):
        nIndex = len(self._arWidgetSettings)-1
        for dcLayout in arLayout:
            if nIndex >= 0:
                self._arWidgetSettings[nIndex]['layout'] = {
                    "col": dcLayout.get("col", self._arWidgetSettings[nIndex]['layout'].get("col", 1)),
                    "row": dcLayout.get("row", self._arWidgetSettings[nIndex]['layout'].get("row", 1)),
                    "x": dcLayout.get("size_x", self._arWidgetSettings[nIndex]['layout'].get("x", 1)),
                    "y": dcLayout.get("size_y", self._arWidgetSettings[nIndex]['layout'].get("y", 1))
                }
                nIndex -= 1
            else:
                return False
        return True

    def stop(self):
        self._unloadWidgets()

    def push(self, strWidgetId, objData):
        objWidget = self._dcWidgets.get(strWidgetId)
        if objWidget:
            objResponse = objWidget.process(objData)
            if objResponse:
                return objResponse
            else:
                return True
        return False

    def _unloadWidgets(self):
        print self._dcWidgets
        while len(self._dcWidgets) > 0:
            strKey, objWidget = self._dcWidgets.popitem()  # [strKey]
            if not objWidget.stop():
                print 'Error Deleting', strKey, 'Sampler'
                del objWidget
        self._dcWidgets = dict()

    def _loadWidgets(self):
        for dcWidget in self._arWidgetSettings:
            print dcWidget
            if self._startWidget(dcWidget):
                strType = dcWidget.get('type')
                strPath = os.path.join('widgets', strType, strType)
                self._arJavascript.append(strPath + '.js')
                self._arStyles.append(strPath + '.css')
            else:
                print 'not Loaded'

    def _startWidget(self, dcSettings):
        strId = dcSettings.get('id', None)
        strType = dcSettings.get('type', 'Number')
        try:
            import importlib
            objModule = importlib.import_module("pydashie.widgets." + strType)
            objWidgetClass = getattr(objModule, strType.title() + "Widget")
        except Exception as e:
            print e
            return False
        objWidget = objWidgetClass(strId, self._objStreams, dcSettings)
        if objWidget.start():
            self._addWidget(strId, objWidget)
            return True
        else:
            print objWidget
            print 'not Started'
        return False

    def _addWidget(self, strID, objWidget):
        if objWidget:
            if strID in self._dcWidgets:
                objCurrentWidget = self._dcWidgets[strID]
                del objCurrentWidget
            self._dcWidgets[strID] = objWidget
            return True
        return False

    def renderHTML(self):
        pass

    def renderDashboard(self, bDebug=False):
        pass

    def getWidget(self, strId=None):
        if strId:
            return self._dcWidgets.get(strId, None)
        else:
            return self._dcWidgets.values()
