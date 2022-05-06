import requests

"""
self.req = {
    'shipments': [
        {
            'id': '<tracking_number>',
            'service': '<service type>',
            'origin': {
                'address': {
                    'addressLocality': '<wtf>'
                },
                'servicePoint': {
                    'url': '<dhl country profile page or sth>',
                    'label': '<idk what label is this>'
                }
            },
            'destination': {
                'address': {
                    'addressLocality': <>
                },
                'servicePoint': {
                    'url': <>,
                    'label': <>
                }
            },
            'status': {
                'description': '<status description>'
            },
            'details': {
                'proofOfDeliverySignedAvailable': <bool>
            },
            'events': [
                {
                    'descritpion': '<shipment status>'      # Wtf no timestamp?
                },
                {
                    'description': <>
                }
            ]
        }
    ]
}
"""

class TrackDHLParcel(object):
    BASE_URL = "https://api-eu.dhl.com/track/shipments"
    
    def __init__(self, tracking_number, api_key):
        header = {'DHL-API-Key': api_key}
        req_url = self.BASE_URL + "?trackingNumber=" + tracking_number
        
        self.parcel = requests.get(req_url, headers=header).json()
    
    def get_tracking_details(self, index):
        return self.parcel['shipments']['events'][index]['description']

    def get_current_status(self):
        return self.parcel['shipments']['status']['description']
    
    def get_tracking_history(self):
        history = []

        for i in range(0, len(self.parcel['shipments']['events'])-1):
            history.append(self.get_tracking_details(i))
        
        pretty_text = ""

        for entry in history:
            pretty_text = pretty_text + entry['description'] + "\n"
        
        return pretty_text