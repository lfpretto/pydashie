from pydashie.dashie_sampler import NumberSampler, ListSampler, ChartSampler, MeterSampler
import requests
import json


class GetRequestNumber(NumberSampler):
    def settings(self):
        return {
            'url': 'The URL that will be requested.',
        }

    def sample(self):
        try:
            r = requests.get(self.getSetting("url"))
            assert r.status_code == 200
            return self.processResponse(r.text)
        except Exception as e:
            print e
            return None

    def processResponse(self, strResponse):
        try:
            objResponse = json.loads(strResponse)
            return objResponse.get("value", None)
        except Exception as e:
            return None

class GetRequestMeter(MeterSampler):
    def settings(self):
        return {
            'url': 'The URL that will be requested.',
        }

    def sample(self):
        try:
            r = requests.get(self.getSetting("url"))
            assert r.status_code == 200
            return self.processResponse(r.text)
        except Exception as e:
            print e
            return None

    def processResponse(self, strResponse):
        try:
            objResponse = json.loads(strResponse)
            return objResponse.get("value", None)
        except Exception as e:
            print e
            return None


class GetRequestList(ListSampler):
    def settings(self):
        return {
            'url': 'The URL that will be requested.',
        }

    def sample(self):
        try:
            print 'Calling URL'
            r = requests.get(self.getSetting("url"))
            assert r.status_code == 200
            return self.processResponse(r.text)
        except Exception as e:
            print e
            return None

    def processResponse(self, strResponse):
        try:
            objResponse = json.loads(strResponse)
            objResponse.get("value", None)
        except Exception as e:
            return None

class GetRequestChart(ChartSampler):
    def settings(self):
        return {
            'url': 'The URL that will be requested.',
        }

    def sample(self):
        try:
            print 'Calling URL'
            r = requests.get(self.getSetting("url"))
            assert r.status_code == 200
            return self.processResponse(r.text)
        except Exception as e:
            print e
            return None

    def processResponse(self, strResponse):
        try:
            objResponse = json.loads(strResponse)
            objResponse.get("Value", None)
        except Exception as e:
            return None