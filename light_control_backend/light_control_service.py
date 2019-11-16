import requests


class LightControlService(object):

    def __init__(self, config):
        self.config = config
    # in memoru non-thread-safe cache for current state of light system
    cache = {}



    def get_state(self):
        return self.cache

    '''
    structure:
    device_id
    lightLevelValue
    colourTemperatureValue
    '''
    def set_light(self, light_settings):
        device_id = light_settings["device_id"]
        clearedDealsList = None
        if "pipedriveDeals" in self.cache.keys():
            clearedDealsList = self.cache["pipedriveDeals"]
        else:
            url = "https://" + self.config.get('company_domain') + ".pipedrive.com/v1/deals?api_token=" + self.config.get(
                'api_token')
            result = requests.get(url)
            dealsList = result.json()["data"]
            list = self.preprocessDeals(dealsList)
            # todo sort by value*probability
            clearedDealsList = self.sorter.sort_deals(list)
            self.cache[device_id] = light_settings
        return clearedDealsList
