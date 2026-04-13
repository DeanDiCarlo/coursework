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
        return {loc.state for loc in self.locations}
        
    def getCityNamesOfState(self, state):
        return {loc.cityName for loc in self.locations if loc.state == state}
  
    def getCommonCityNames(self, state1, state2):
        return self.getCityNamesOfState(state1) & self.getCityNamesOfState(state2)

    def _haversine(self, lat1, lon1, lat2, lon2):
        import math
        R = 3959.0
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = (math.sin(dLat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dLon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def getCloseZipCodes(self, zipCode, miles):
        target = None
        for loc in self.locations:
            if loc.zipCode == zipCode:
                target = loc
                break
        if target is None:
            return set()
        return {loc.zipCode for loc in self.locations
                if loc.zipCode != zipCode and
                self._haversine(target.lat, target.lon, loc.lat, loc.lon) <= miles}
        
    def getStateNamesKeyByInitialLetter(self):
        result = {chr(c): set() for c in range(ord('A'), ord('Z') + 1)}
        for state in self.getStateNames():
            result[state[0]].add(state)
        return result
        
    def getCityNamesMap(self):
        result = {}
        for loc in self.locations:
            if loc.state not in result:
                result[loc.state] = set()
            result[loc.state].add(loc.cityName)
        return result
        
    def statesWithMostZipCodes(self):
        counts = {}
        for loc in self.locations:
            counts[loc.state] = counts.get(loc.state, 0) + 1
        maxCount = max(counts.values())
        return {state for state, count in counts.items() if count == maxCount}

if __name__ == "__main__":
    places = Places("zipcodes.tsv")
    print(places.getStateNames())
    print(places.getCityNamesOfState("HI"))
    print(places.getCommonCityNames("MI", "OH"))
    print(places.getCloseZipCodes(45056, 6.0))
    print(places.getStateNamesKeyByInitialLetter())
    print(places.getCityNamesMap())
    print(places.statesWithMostZipCodes())