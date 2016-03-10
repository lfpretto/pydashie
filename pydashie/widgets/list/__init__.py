""" List Widget v1
"""
from pydashie.libs.widget import DashingWidget


class ListWidget(DashingWidget):
    """ Generates a Key Value list in a Widget
    """

    def process(self, dcList):
        """ Calculate the necessary values for a List to be sampler

        Args:
            dcList: Should be a LIST with objects containing a 'label' and a 'value'

        Returns:
            None
        """
        if dcList and isinstance(dcList, dict):
            self.storage(dcList)
            arItems = list()
            for label, value in dcList:
                arItems.append({'label': label, 'value': value})
            self._send({'items': arItems})
