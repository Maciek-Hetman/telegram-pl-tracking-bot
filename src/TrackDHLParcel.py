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
                    'description': '<shipment status>'      # Wtf no timestamp?
                },
                {
                    'description': <>
                }
            ]
        }
    ]
}
"""

import http.client
import urllib.parse
import json


class TrackDHLParcel(object):
    BASE_URL = "https://api-eu.dhl.com/track/shipments"
    
    def __init__(self, tracking_number, api_key):
        params = urllib.parse.urlencode({
            'trackingNumber': tracking_number.strip(),
        })
        headers = {
            'Accept': 'application/json',
            'DHL-API-Key': api_key
        }

        connection = http.client.HTTPSConnection("api-eu.dhl.com")
        connection.request("GET", "/track/shipments?" + params, "", headers)

        response = connection.getresponse()
        self.parcel = json.loads(response.read())

        connection.close()

    def get_tracking_details(self, index):
        return self.parcel['shipments'][0]['events'][index]['description']

    def get_current_status(self):
        return self.get_tracking_details(0)

    def get_tracking_history(self):
        history = []

        if len(self.parcel['shipments'][0]['events']) == 1:
            return self.get_current_status()
        else:
            for i in range(0, len(self.parcel['shipments'][0]['events'])-1):
                history.append(self.get_tracking_details(i))
            
            pretty_text = ""

            for entry in history:
                pretty_text = pretty_text + entry + "\n"
            
            return pretty_text
