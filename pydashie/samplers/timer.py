from samplers.sampler import DashingSampler
from threading import Timer

class TimerSampler(DashingSampler):
    """ Run a sample periodicatly in a set interval.
    """
    _objTimer = None

    def _sampler(self):
        """ Child class implements this function

        Returns:
            None
        """
        pass

    def start(self):
        """  Start the interval sampler

        Returns:
            bool True
        """
        self._start()
        nInterval = self.get('interval', 0)
        if nInterval > 0:
            self._objTimer = RepeatedTimer(nInterval, self._sampler)
        return True

    def stop(self):
        """  Stop the Sampler from running in the interval

        Returns:
            None
        """
        self._stop()
        if self._objTimer:
            self._objTimer.stop()
            del self._objTimer
            self._objTimer = None
        return True

    def setTimer(self, nInterval):
        """ Sets the interval time in seconds for the Timer.

        Args:
            nInterval: Number of seconds that the timer will trigger the
                sampler method.

        Returns:
            None
        """
        self.get('interval', nInterval)
        self.stop()
        if nInterval > 0:
            self._objTimer = RepeatedTimer(nInterval, self._sample)



class RepeatedTimer(object):
    """ Repeat a method after X secs
    """

    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        """ Method tha is ran on every timmer trigger.

        Returns:
            None
        """
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        """ Starts the Timer

        Returns:
            None
        """
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        """ Stops the Timer

        Returns:
            None
        """
        self._timer.cancel()
        self.is_running = False
