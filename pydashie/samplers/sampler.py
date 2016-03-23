from pydashie.libs.widget import DashingWidget


class DashingSampler:
    """ Run a sample periodicatly in a set interval.
    """
    def __init__(self, objWidget, settings=dict()):
        self._arWidgets = list()
        self._dcSettings = settings
        self.addWidget(objWidget, 'value')

    def __del__(self):
        self.stop()

    def getSettings(self):
        """
        Returns:

        """
        return self._dcSettings

    def addWidget(self, objWidget, strKey=None):
        """ Add a Widget to list of linked Widgets

        Args:
            objWidget: The Widget object that is linked to the Sampler.
            strKey: The key from the data from the sampler that will be
                sent to the Widget.

        Returns:
            None
        """
        if isinstance(objWidget, DashingWidget):
            self._arWidgets.append({'object': objWidget, 'key': strKey})

    def _process(self, objData):
        """ Sends the data to the Widget.

        Args:
            objData: The Data to be sent to the Widget

        Returns:
            bool: True
        """
        for dcLink in self._arWidgets:
            objWidget = dcLink.get('object', None)
            strKey = dcLink.get('key', None)
            if strKey:
                objSample = objData.get(strKey, None)
            else:
                objSample = objData
            if objWidget and objSample:
                objWidget.process(objSample)
        return True

    def get(self, strKey, objDefault=None):
        """ Get the specific setting defined by the child calsses

        Args:
            strKey: The name of the setting
            objDefault: the value to return if the setting doesnt exist

        Returns:
            The value associated to the key or the objDefault if the key doenst exist.
        """
        return self._dcSettings.get(strKey, objDefault)

    def set(self, strKey, objValue):
        """ Changes a setting on the smapler configuration.

        Args:
            strKey: The name of the setting to be changed
            objValue: The new value for the setting

        Returns:
            None
        """
        self._dcSettings[strKey] = objValue

    def _start(self):
        """  Used to Create another Extensible Class
            This is ran when the sampler starts

        Returns:
            None
        """
        return True

    def start(self):
        """ Child class implements this function
            This runs at the start of the sampler

        Returns:
            True
        """
        return self._start()


    def _stop(self):
        """  Used to Create another Extensible Class
            This runs then the Sampler is deleted.

        Returns:
            None
        """
        return True

    def stop(self):
        """ Child class implements this function
            This runs at the end of the sampler

        Returns:
            True
        """
        return self._stop()
