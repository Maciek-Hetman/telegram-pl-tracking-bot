import requests as req

class TrackParcel(object):
    API_BASE_URL = "https://api.ordertracker.com"
    API_REFERENCE_URL = "public/trackinglinks"

    def __init__(self, trackingNumber):
        self.link = self.getTrackingLink(trackingNumber)
        self.data = self.getTrackingInfo(self.link)

        if not self.data:
            raise ("Cound not find tracking info for package %s" % trackingNumber)
        
        try:
            self.number = self.data['number']
            self.status = self.data['status']
            self.steps = self.data['steps']
            self.dit = self.data['daysInTransit']
        except KeyError:
            raise ("Error interpreting data for %s" % trackingNumber)
        
    def getTrackingLink(self, trackingNumber):
        r = req.get(f"{self.API_BASE_URL}/{self.API_REFERENCE_URL}?trackingstring={trackingNumber}")

        if not r.ok:
            return False
        
        return r.json()[0]['link']
    
    def getTrackingInfo(self, link):
        r = req.get(link)

        if not r.ok:
            return False
        
        return r.json()
    
    def getStatus(self):
        return self.status
    
    def getSteps(self):
        return self.steps
    
    def getDit(self):
        return self.dit
    