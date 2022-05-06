"""
self.parcel for locker
self.parcel = {
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
            'status': '<parcel status>'
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
    def __init__(self, tracking_number):
        self.parcel = requests.get("https://api-shipx-pl.easypack24.net/v1/tracking/%s" % tracking_number).json()
        
        try:
            self.parcel['tracking_details']
        except KeyError:
            raise ("Could not find parcel %s" % tracking_number)

    def get_tracking_details(self, index):
        entry = self.parcel['tracking_details'][index]
        info = {
            'date': entry['datetime'],
            'status': entry['status']
        }

        return info

    def get_current_status(self):
        status = self.parcel['tracking_details'][0]['status']

        return self.format_status(status)
        
    def get_tracking_history(self):
        history = []

        for i in range(0, len(self.parcel['tracking_details'])-1):
            history.append(self.get_tracking_details(len(self.parcel['tracking_details']) - i - 1))
        
        pretty_text = ""

        for entry in history:
            for item in entry:
                pretty_text = pretty_text + item.capitalize() + ": " + self.format_item(entry[item]) + "\n"
            
            pretty_text += "\n"
        
        return pretty_text

    def format_item(self, item):
        if "T" in item and ":" in item and "-" in item:
            return self.format_datetime(item)
        else:
            return self.format_status(item)

    def format_status(self, status):
        text = status.capitalize().split('_')
        pretty_text = ""

        for word in text:
            pretty_text = pretty_text + word + " "

        return pretty_text

    def format_datetime(self, datetime):
        dt = datetime.split("T")                # dt = ["2022-05-31", "21:37.000+2:00"]
        dt[1] = dt[1].split(".")[0]

        pretty_text = dt[0] + " " + dt[1]

        return pretty_text
    