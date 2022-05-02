from poczta_polska_enadawca.settings import PocztaPolskaSettingsObject
from poczta_polska_enadawca.ws_tracking_api import PocztaPolskaWSTrackingAPI

class PocztaPolska(object):
    def __init__(self):
        self.settings = PocztaPolskaSettingsObject()
        self.settings.POCZTA_POLSKA_WSTRACKING_API_USERNAME = 'sledzeniepp'
        self.settings.POCZTA_POLSKA_WSTRACKING_API_PASSWORD = 'PPSA'

        self.ppTrackingInstance = PocztaPolskaWSTrackingAPI(initZeep=False)
        self.ppTrackingInstance.set_config(self.settings)

        try:
            self.ppTrackingInstance.check_config()
        except UnboundLocalError:
            raise UnboundLocalError("Failed to set password/username")

        self.ppTrackingInstance.init_zeep()
    
    def CheckPackage(self, tracking_number):
        if type(tracking_number) != str:
            tracking_number = str(tracking_number)
        
        return self.ppTrackingInstance.service_call('sprawdzPrzesylke', tracking_number)

        