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
        return null;
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
        return null;
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
        return null;
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
        return null;
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
        return null;
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
        return null;
    }

    /// <summary>
    /// Returns the set of states that have the most zip codes. In many cases, this set will
    /// contain one state but if there is a ties, there could be multiple states in the set.
    /// </summary
    /// <returns>
    /// The state(s) that have the most zip codes.
    /// </returns>
    public HashSet<String> statesWithMostZipCodes() {
        return null;
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
