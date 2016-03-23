
import requests
import json
from samplers.timer import TimerSampler


class RequestSampler(TimerSampler):
    def settings(self):
        return {
            'interval': 'The timer Interval',
            'url': 'The URL that will be requested.',
            'http': 'GET or POST',
            'postData': 'Object to be sent as json'
        }

    def _start(self):
        print("start request sampler")

    def _stop(self):
        print("stop request sampler")

    def _sampler(self):
        try:
            r = requests.get(self.get("url"))
            assert r.status_code == 200
            objResponse = json.loads(r.text)
            if objResponse:
                self._process(objResponse)
        except Exception as e:
            print(e)
            print('Error')
        return None
