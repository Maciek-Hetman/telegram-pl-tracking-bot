"""
self.parcel_info = {
    'danePrzesylki': {                                  # Parcel info
        'dataNadania': <datetime.date object>           # Creation time
        'format': <None, or idk>
        'kodKrajuNadania': <string>                     # Origin country code
        'kodKrajuPrzezn': <string>                      # Destination country code
        'kodRodzPrzes': <string>                        # Parcel type code
        'krajNadania': <string>                         # Origin country
        'krajPrzezm': <string>                          # Destination country
        'masa': <None or something>                     # Weight
        'numer': <string>                               # Tracking number
        'proceduraSerwis': {
            'kod': <none or sth>
            'kopertaFirmowa': <none or sth>
            'nazwa': <none or sth>
            'przesylkiPowiazane': <none or sth>
        }
        'rodzPrzes': <string>                           # Parcel type
        'urzadNadania': {                               
            'daneSzczegolowe': {
                'dlGeogr': None,
                'godzinyPracy': None,
                'miejscowosc': None,
                'nrDomu': None,
                'nrLokalu': None,
                'pna': None,
                'szerGeogr': None,
                'ulica': None
            },
            'nazwa': 'PP PP-Wrocław D101'
        },
        'urzadPrzezn': {
            'daneSzczegolowe': {
                'dlGeogr': None,
                'godzinyPracy': None,
                'miejscowosc': None,
                'nrDomu': None,
                'nrLokalu': None,
                'pna': None,
                'szerGeogr': None,
                'ulica': None
            },
            'nazwa': 'UP Lublin 62'
        },
        'zakonczonoObsluge': True,                      # Is delivered?
        'zdarzenia': {
            'zdarzenie': [
                {
                    'czas': <string>,
                    'jednostka': {
                        'daneSzczegolowe': {
                            'dlGeogr': None,
                            'godzinyPracy': None,
                            'miejscowosc': None,
                            'nrDomu': None,
                            'nrLokalu': None,
                            'pna': None,
                            'szerGeogr': None,
                            'ulica': None
                        },
                        'nazwa': None
                    },
                    'kod': <string>,
                    'konczace': <bool>,                 # Ending?
                    'nazwa': <string>,                  # Description (IMPORTANT)
                    'przyczyna': {
                        'kod': None,
                        'nazwa': None
                    }
                },
                {another one}
            ]
        }
        'numer': <string>                               # Tracking number
        'status': <int>
    }
}
"""

from zeep import Client
from zeep.wsse.username import UsernameToken

class TrackParcelPP(object):
    def __init__(self, tracking_number):
        self.client = Client('https://tt.poczta-polska.pl/Sledzenie/services/Sledzenie?wsdl', wsse=UsernameToken('sledzeniepp', 'PPSA'))
        self.parcel_info = self.client.service.sprawdzPrzesylke(str(tracking_number))
    
    def get_tracking_details(self, index):
        entry = self.parcel_info['danePrzesylki']['zdarzenia']['zdarzenie'][index]

        info = {
            'date': entry['czas'],
            'status': entry['nazwa']
        }

        return info

    def get_current_status(self):
        return self.parcel_info['danePrzesylki']['zdarzenia']['zdarzenie'][0]['nazwa']
    
    def get_tracking_history(self):
        history = []

        for i in range(0, len(self.parcel_info['danePrzesylki']['zdarzenia']['zdarzenie'])-1):
            history.append(self.get_tracking_details(i))
        
        pretty_text = ""

        for entry in history:
            for item in entry:
                pretty_text = pretty_text + item.capitalize() + ": " + entry[item] + "\n"
            
            pretty_text += "\n"
        
        return pretty_text