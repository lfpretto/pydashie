from samplers.sampler import DashingSampler

class PushSampler(DashingSampler):
    """ Sampler waits for a information to be pushed.
    """

    def received(self, strUrl, objData):
        """ Method is called when

        Args:
            objData: Data being pushed

        Returns:
            True if processed ok.
        """
        strConfig = self.get('url', None)
        if strConfig and strConfig == strUrl:
            return self._received(objData)
        else:
            return None

    def _received(self, objData):
        """

        Args:
            objData:

        Returns:

        """

        return self._process(objData)
