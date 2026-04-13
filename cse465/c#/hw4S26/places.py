class Location:
    def __init__(self, zipCode, cityName, state, lat, lon):
        self.zipCode = int(zipCode)
        self.cityName = cityName
        self.state = state
        self.lat = float(lat)
        self.lon =  float(lon)
  
class Places:

    # You should not need to alter this constructor.
    def __init__(self, fname):
        self.locations = []
        file = open(fname, "r")
        header = file.readline()
        for line in file:
            toks = line.split("\t")
            # if lat/lon is empty, skip this entry
            if toks[6] == '' or toks[7] == '':
                continue
            self.locations.append(Location(toks[1], toks[3], toks[4], toks[6], toks[7]))
    
    # You will fill in the following methods. Read the C# file to
    # learn what each method should do. When C# returns a Set, the Python
    # should also return a set. When the C# code returns a Dictionay, the
    # Python code should also return a dictionary. And so on.
    # You may add methods to this file but do not change the names or parameters of
    # these.
    def getStateNames(self):
        return None
        
    def getCityNamesOfState(self, state):
         return None
  
    def getCommonCityNames(self, state1, state2):
        return None

    def getCloseZipCodes(self, zipCode, miles):
        return None
        
    def getStateNamesKeyByInitialLetter(self):
        return None
        
    def getCityNamesMap(self):
        return None
        
    def statesWithMostZipCodes(self):
        return None

if __name__ == "__main__":
    places = Places("zipcodes.tsv")
    print(places.getStateNames())
    print(places.getCityNamesOfState("HI"))
    print(places.getCommonCityNames("MI", "OH"))
    print(places.getCloseZipCodes(45056, 6.0))
    print(places.getStateNamesKeyByInitialLetter())
    print(places.getCityNamesMap())
    print(places.statesWithMostZipCodes())