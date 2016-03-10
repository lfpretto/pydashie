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
        self._strId = strId
        self._objConnection = objConnection
        if dcSettings:
            self._dcSettings = dcSettings
            self._dcSettings['view'] = dcSettings.get('type', 'number').title()
        else:
            self._dcSettings = dict()
        self._nSamples = dcSettings.get('samples', 0)
        self._arStorage = list()
        self._strHTML = ""

    def __del__(self):
        self.stop()

    def get(self, strId):
        """ Gets a Parameter from the Widget.

        Args:
            strId: The ID of the parameter

        Returns:
            The Value of the parameter
        """
        if strId in ('row', 'col', 'x', 'y', 'icon'):
            objLayout = self._dcSettings.get('layout', None)
            if objLayout:
                return objLayout.get(strId, 1)
            else:
                return '1'
        else:
            return self._dcSettings.get(strId, '')

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
        return self._send({strKey: self._arStorage})

    def start(self):
        """ Loads and Start the Sampler configured for this Widget
        Returns:
            True
        """
        bResult = self._runHTML()
        bResult = bResult & self._runSampler()
        return bResult

    def _runSampler(self):
        """ Runs the Widget SAMPLER based on the 'sampler' configs in the settings.
        Returns:
            True if successful, False otherwise
        """
        dcSamplerSettings = self._dcSettings.get('sampler', None)
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
                self._objSampler = objSamplerClass(self, dcSamplerSettings)
                return self._objSampler.start()
        return True

    def stop(self):
        """ Stops the Sampler configured for the Widget

        Returns:
             bool: True '_objSampler' deleted, False otherwise
        """
        if self._objSampler:
            try:
                return self._objSampler.stop()
            except Exception as e:
                print e
                del self._objSampler
            if self._objSampler:
                return False
        return True

    def _runHTML(self):
        """ Generates the HTML representation of the Widget.
            The string is can be accessed by the 'render' method.
        Returns:
            bool: True if no exceptions occurred, False otherwise
        """
        try:
            from jinja2 import Environment, FileSystemLoader
            strType = self._dcSettings["type"]
            strFile = os.path.join("widgets", strType, 'div.html')
            if os.path.isfile(strFile):
                env = Environment(loader=FileSystemLoader(os.path.dirname(strFile)))
                self._strHTML = env.get_template('div.html').render(**self._dcSettings)
            else:
                env = Environment(loader=FileSystemLoader('templates'))
                self._strHTML = env.get_template('div.html').render(**self._dcSettings)
        except Exception as e:
            print e
            return False
        else:
            return True

    def __str__(self):
        return str(self._strHTML)

    def render(self):
        """ Generates the HTML representation of the Widget.
        Returns:
            string: Containing the safe HTML representation of the widget.
                It will return an empty string if HTML is not generated.
        """
        return str(self._strHTML)




