"""
self.package for locker
self.package = {
    'tracking_number': '<number>'
    'service': 'inpost_locker_standard'
    'type': 'inpost_locker_standard'
    'status': '<status like sent_from_source_branch>'
    'custom_attributes': {
        'size': '<size>'
        'target_machine_id': '<locker id>'
        'target_machine_detail': {
            'name': '<locker id again>'
            'opening_hours': '<usually 24/7>'
            'location_desription': '<desc in polish>'
            'location': {
                'latitude': '<coords>'
                'longitude': '<coords>'
            }
            'address': {
                'line1': '<street and number>'
                'line2': '<postal code and city>'
            }
            'type': ['parcel_locker']
            'location247': <bool>
        }
        'end_of_week_collection': <bool>
    }
    'tracking_details': [ 
        # That's list of entrys sorted from newest at index 0 to oldest
        {
            'status': '<package status>'
            'origin_status': '<idk what is this>'
            'agency': <idk>
            'datetime': '<time>'
        }
    ]
    'expected_flow': [<list idk>]
    'created_at': '<creation date>'
    'updated_at': '<update time>'
}
"""

import requests

class TrackInpostParcel(object):
    def __init__(self, trackingNumber):
        if type(trackingNumber) != str:
            trackingNumber = str(trackingNumber)
        
        self.package = requests.get("https://api-shipx-pl.easypack24.net/v1/tracking/%s" % trackingNumber).json()
    
    def getTrackingDetails(self, index):
        entry = self.package['tracking_details'][index]
        info = {
            'status': entry['status'],
            'datetime': entry['datetime']
        }

        return info

    def getStatus(self):
        return self.package['tracking_details'][0]['status']
    
    def getTrackingHistory(self):
        return self.package['tracking_details']
    
    def getLastUpdateTime(self):
        return self.package['updated_at']

    def getCreationTime(self):
        return self.package['created_at']

    def getTrackingNumber(self):
        return self.package['tracking_number']
    
    def getService(self): # This could be locker or courier
        return self.package['service']
    
    def getTargetLocation(self):
        return self.package['custom_attributes']['target_machine_detail']