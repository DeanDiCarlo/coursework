using System;
using System.Collections.Generic;
using System.IO;

// If you get errors about null values/nullables, uncomment the following:
//#nullable disable

public class Location {
    public int zipCode;
    public String cityName;
    public String state;
    public double lat;
    public double lon;
    public Location(String zipCode, String cityName, String state, String lat, String lon) {
        this.zipCode = Int32.Parse(zipCode);
        this.cityName = cityName;
        this.state = state;
        this.lat = Double.Parse(lat);
        this.lon = Double.Parse(lon);
    }
}

public class Places {
    private List<Location> places;

    /**
     * You should not need to modify this constructor
     **/
    public Places(String fname) {
        StreamReader reader = new StreamReader(fname);
        if (reader == null) {
            Console.WriteLine("Problem with input file: " + fname);
            Environment.Exit(0);
        }
        places = new List<Location>();
        String header = reader.ReadLine();
        while (!reader.EndOfStream) {
            String line = reader.ReadLine();
            if (line == null)
                continue;
            String[] toks = line.Split("\t");
            if (toks[6] == "" || toks[7] == "")
                continue;
            places?.Add(new Location(toks[1], toks[3], toks[4], toks[6], toks[7]));
        }
        reader.Close();
    }

    /// <summary>
    /// Returns all state names in the entire database
    /// </summary>
    /// <returns>
    /// Set of strings, where the strings correspond to the names of all the states.
    /// </returns>
    public HashSet<String> getStateNames() {
        HashSet<String> states = new HashSet<String>();
        foreach (Location loc in places) {
            states.Add(loc.state);
        }
        return states;
    }

    /// <summary>
    /// Returns all city names that reside within a particular state.
    /// </summary
    /// <param name="state">
    /// The state to acquire city information.
    /// </param>
    /// <returns>
    /// Set of strings, where the strings correspond to all the cities that
    /// are part of the given state.
    /// </returns>
    public HashSet<String> getCityNamesOfState(String state) {
        HashSet<String> cities = new HashSet<String>();
        foreach (Location loc in places) {
            if (loc.state == state) {
                cities.Add(loc.cityName);
            }
        }
        return cities;
    }

    /// <summary>
    /// Returns the city names that appear in both of the given states.
    /// "OH" and "MI" would yield { OXFORD, FRANKLIN, ... }
    /// </summary
    /// <param name="state1">
    /// The first target state.
    /// </param>
    /// <param name="state2">
    /// The second target state.
    /// </param>
    /// <returns>
    /// Set of strings, where the strings correspond to all the cities that
    /// are part of both states.
    /// </returns>
    public HashSet<String> getCommonCityNames(String state1, String state2) {
        HashSet<String> cities1 = getCityNamesOfState(state1);
        HashSet<String> cities2 = getCityNamesOfState(state2);
        cities1.IntersectWith(cities2);
        return cities1;
    }

    /// <summary>
    /// Returns all the zip codes that close to another zip code, where closeness
    /// is defined by the parameter miles. The Haversine formula can be use
    /// to determine the distance between two positions. Read up on Haversine.
    /// </summary
    /// <param name="zipCode">
    /// zip code of target city. Use the first zip code that matches.
    /// </param>
    /// <param name="miles">
    /// The maximum number of miles away and still be considered close.
    /// </param>
    /// <returns>
    /// Set of zipCode that are close enough to the given zipCode. The given
    /// zipCode is NOT part of the result.
    /// </returns>

    public HashSet<int> getCloseZipCodes(int zipCode, double miles) {
        Location target = null;
        foreach (Location loc in places) {
            if (loc.zipCode == zipCode) {
                target = loc;
                break;
            }
        }
        HashSet<int> result = new HashSet<int>();
        if (target == null) return result;
        foreach (Location loc in places) {
            if (loc.zipCode == zipCode) continue;
            double dist = Haversine(target.lat, target.lon, loc.lat, loc.lon);
            if (dist <= miles) {
                result.Add(loc.zipCode);
            }
        }
        return result;
    }

    private double Haversine(double lat1, double lon1, double lat2, double lon2) {
        double R = 3959.0;
        double dLat = (lat2 - lat1) * Math.PI / 180.0;
        double dLon = (lon2 - lon1) * Math.PI / 180.0;
        double a = Math.Sin(dLat / 2) * Math.Sin(dLat / 2) +
                   Math.Cos(lat1 * Math.PI / 180.0) * Math.Cos(lat2 * Math.PI / 180.0) *
                   Math.Sin(dLon / 2) * Math.Sin(dLon / 2);
        double c = 2 * Math.Atan2(Math.Sqrt(a), Math.Sqrt(1 - a));
        return R * c;
    }

    /// <summary>
    /// Returns a map that is keyed by a letter. The values in the map are the
    /// those states that begin with that letter.The result will look like:
    /// 'A' --> { "AL", "AK", ... } 'B' --> {} ...
    /// </summary
    /// <returns>
    /// Mapping from states to set of city names.
    /// </returns>
    public Dictionary<char, HashSet<String>> getStateNamesKeyByInitialLetter() {
        Dictionary<char, HashSet<String>> map = new Dictionary<char, HashSet<String>>();
        for (char c = 'A'; c <= 'Z'; c++) {
            map[c] = new HashSet<String>();
        }
        foreach (String state in getStateNames()) {
            char initial = state[0];
            map[initial].Add(state);
        }
        return map;
    }

    /// <summary>
    /// Returns a map that is keyed to state name. The values in the map are the
    /// set of city names that reside in that particular state.The map looks
    /// like: "AL" --> { "MONTGOMERY", "MOBILE", ... }  "AK"-- > {"ANCHORAGE","BARROW", ...}
    /// ...
    /// </summary
    /// <returns>
    /// Mapping from states to set of city names.
    /// </returns>
    public Dictionary<String, HashSet<String>> getCityNamesMap() {
        Dictionary<String, HashSet<String>> map = new Dictionary<String, HashSet<String>>();
        foreach (Location loc in places) {
            if (!map.ContainsKey(loc.state)) {
                map[loc.state] = new HashSet<String>();
            }
            map[loc.state].Add(loc.cityName);
        }
        return map;
    }

    /// <summary>
    /// Returns the set of states that have the most zip codes. In many cases, this set will
    /// contain one state but if there is a ties, there could be multiple states in the set.
    /// </summary
    /// <returns>
    /// The state(s) that have the most zip codes.
    /// </returns>
    public HashSet<String> statesWithMostZipCodes() {
        Dictionary<String, int> counts = new Dictionary<String, int>();
        foreach (Location loc in places) {
            if (!counts.ContainsKey(loc.state)) {
                counts[loc.state] = 0;
            }
            counts[loc.state]++;
        }
        int maxCount = 0;
        foreach (int count in counts.Values) {
            if (count > maxCount) {
                maxCount = count;
            }
        }
        HashSet<String> result = new HashSet<String>();
        foreach (var pair in counts) {
            if (pair.Value == maxCount) {
                result.Add(pair.Key);
            }
        }
        return result;
    }

    public static void Main(string[] args) {
        Places places = new Places("zipcodes.tsv");
        Console.WriteLine(places.getStateNames());
        Console.WriteLine(places.getCityNamesOfState("HI"));
        Console.WriteLine(places.getCommonCityNames("MI", "OH"));
        Console.WriteLine(places.getCloseZipCodes(45056, 6.0));
        Console.WriteLine(places.getCityNamesMap());
        Console.WriteLine(places.getStateNamesKeyByInitialLetter());
        Console.WriteLine(places.statesWithMostZipCodes());
    }
}
