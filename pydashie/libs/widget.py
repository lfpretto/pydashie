""" Widget Base Class definition
"""
import datetime
import os


class DashingWidget:
    """ Base class for the Widgets
        The child classes should implement the 'process' method, if any special
        processing of the information needs to be done
    """

    def __init__(self, strId, objConnection, dcSettings):
        self._objSampler = None
        self._objConnection = objConnection
        self._strId = strId
        self._strTitle = dcSettings.get('title', "")
        self._strType = dcSettings.get('type', 'number')
        self._dcSettings = dcSettings.get('settings', dict())
        self._dcSampler = dcSettings.get('sampler', None)
        self._dcLayout = dcSettings.get('layout', dict())
        self._nSamples = dcSettings.get('samples', 0)
        self._arStorage = list()
        self._strHTML = ""
        self._runHTML()

    def __del__(self):
        self.stop()

    def __str__(self):
        return str(self._strHTML)

    def get(self, strId):
        """ Gets a Parameter from the Widget.

        Args:
            strId: The ID of the parameter

        Returns:
            The Value of the parameter
        """
        print(self._dcLayout)
        return self._dcLayout.get(strId, '')

    def last(self):
        """ Gets the last value sampled

        Returns:
            The Last value or
            None if it doesnt exist
        """
        if len(self._arStorage) > 1:
            return self._arStorage[-2]
        else:
            return None

    def storage(self, objValue):
        """ Store the value on the storage

        Args:
            objValue: the Value to be Stored
                The object will be stored as it is in a list.

        Returns:
            bool: True if stored or false if no storage configured
        """
        if self._nSamples > 0:
            self._arStorage.append(objValue)
            if len(self._arStorage) > self._nSamples:
                self._arStorage.pop(0)
            return True
        return False

    def process(self, objData):
        """Process the data to be sent to the widget

        Args:
            objData: the object that will be converted to json and send to the interface.

        Returns:
            None
        """
        if objData:
            self.storage(objData)
            self._send(objData)

    def _send(self, dcBody):
        """  Send data to the open connections.
            The 'updatedAt' tag is generated automatically with the current date.
            The 'id' tag is generated with the Widget's Id.

        Args:
            dcBody: A dict with the data that will be sent.
                This dict represents the json object that is sent to the interface.

        Returns:
            bool: True if send successful, false otherwise
        """
        dcBody['id'] = self._strId
        dcBody['updatedAt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self._objConnection.send(dcBody)

    def _sendStorageAs(self, strKey):
        """ Sends the all stored values as an array.
            The length of the array is set by the 'samples' setting.
            The 'storage' method is used to store and ojbect on this array.

        Args:
            strKey: The name of the key that will contain
            the storage list on the json sent to the interface.

        Returns:
            bool: True if send successful, false otherwise
        """
        if len(self._arStorage) > 1:
            return self._send({strKey: self._arStorage})
        return False

    def _runHTML(self):
        """ Generates the HTML representation of the Widget.
            The string is can be accessed by the 'render' method.

        Returns:
            bool: True if no exceptions occurred, False otherwise
        """
        try:
            from jinja2 import Environment, FileSystemLoader
            strFile = os.path.join("widgets", self._strType, 'div.html')
            if os.path.isfile(strFile):
                env = Environment(loader=FileSystemLoader(os.path.dirname(strFile)))
            else:
                env = Environment(loader=FileSystemLoader('templates'))
            self._strHTML = env.get_template('div.html').render(id=self._strId,
                                                                view=self._strType.title(),
                                                                title=self._strTitle,
                                                                **self._dcSettings)
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def render(self):
        """ Generates the HTML representation of the Widget.

        Returns:
            string: Containing the safe HTML representation of the widget.
                It will return an empty string if HTML is not generated.
        """
        return str(self._strHTML)

    def updateLayout(self, dcLayout):
        """ Update the layout parameters of the widget in memory

        Args:
            dcLayout: The structure key and value of the paramters of the layout

        Returns:
            bool: True if layout updated, False otherwise
        """
        if isinstance(dcLayout, dict):
            for strId in dcLayout:
                self._dcLayout[strId] = dcLayout[strId]
            return True
        return False

    def getLayout(self):
        """ Gets the Layout settings of the widget

        Returns:
            dict(): Key and value of the layout parameters.
        """
        return self._dcLayout

    def getSettings(self):
        """ Returns the structured settings of the widget

        Returns:
            dict(): containing the structure of the widget settings.
        """
        return {
            "_html": self._strHTML,
            "id": self._strId,
            "type": self._strType,
            "title": self._strTitle,
            "settings": self._dcSettings,
            "layout": self._dcLayout,
            "sampler": self._dcSampler,
            "samples": self._nSamples
        }
