from pydashie.dashie_sampler import NumberSampler
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
            return json.loads(r.text)["value"]
        except Exception as e:
            print e
            return None