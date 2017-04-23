import urllib, json
from geopy.distance import great_circle
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import simplejson
import CensusDataExtract.utils
import cPickle as p



googleMapRequestCount = 0
invalidRequests = 0
myKey = "AIzaSyAQODArFSeYSO-_S3F-OzyMggJNb5Xlwcc"
myKeyNYCCheck = "AIzaSyBESs0RkTlQ8wNL2kQxkPkIuxsijbMpkA4"


countiesNYC = ["Queens", "Manhattan", "Staten Island", "Bronx", "Brooklyn", "Queens County", "New York"]


googlePlacesAPIKeyList = ["AIzaSyDoFqsEcIOCxSWGsBHS3aq1oC8eI4E_ut0", "AIzaSyAaLzdBOfqxhCQM7gE5dFVWFL4rbEkb7NM", "AIzaSyCMwA6hkSzcUXeoerGoTCjSk0c8mjFss3k", "AIzaSyDbhIuTzVJ6CzpEiNF6Vwa2PL3n7b8kbkY"]

keyIndex = 0


def locationInNYC(lat, lon):
    inNYC = False
    geolocator = Nominatim()
    lat_lon = str(lat) + ", "+str(lon)
    location = geolocator.reverse(lat_lon)

    if "NYC, New York," in location.address:
        inNYC = True

    return inNYC
    
    


def storeNYCLocations(latStart, latEnd, lonStart, lonEnd, incrementFactorLat, incrementFactorLon):
    breakCoordinatesLoopAfter = 320
    locationsInNYC = list()
    countLocationsInNYC = 0
    countLocationsOutsideNYC = 0
    totalCount = 0
    lon = lonStart
    
    while (lon <= lonEnd):
        lat = latStart
        while (lat <= latEnd):
            if (totalCount % 10 == 0):
               print "Locations stored: ", totalCount
            #localityinNYC = locationInNYC(lat, lon)
            localityinNYC = CensusDataExtract.utils.is_inside_county(lat, lon)
            if localityinNYC == False:

                countLocationsOutsideNYC = countLocationsOutsideNYC + 1
            else: 
                #print "Inside NYC"
                locationsInNYC.append((lat,lon))
                countLocationsInNYC = countLocationsInNYC + 1
                

            lat = lat + incrementFactorLat
            totalCount = totalCount + 1
        lon = lon + incrementFactorLon
        
    print "Count of locations inside NYC is ",  countLocationsInNYC
    print "Count of locations outside NYC is ", countLocationsOutsideNYC
    return locationsInNYC 



def placeSearch(lat, lon, myType, radius):
     global googleMapRequestCount
     global keyIndex
     global invalidRequests
     googleMapRequestCount = googleMapRequestCount + 1
     locationString = str(lat)+","+str(lon)
     
     myKeyPlacesSearch = googlePlacesAPIKeyList[keyIndex]    
     myKeyPlacesSearch =  "AIzaSyDUkE6BMgSiVgcpbIS9ztF8wVHDAZKlZZ8"
     myUrl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+locationString+"&radius="+str(radius)+"&types="+myType+"&sensor=false&key="+myKeyPlacesSearch
     response = urllib.urlopen(myUrl)
     jsonRaw = response.read()
     jsonData = json.loads(jsonRaw)
     #print "json Data is ", jsonData

     if "expired" in jsonData["status"].lower() or "api" in jsonData["status"].lower():
         print "Error, we have a query that is expired"
         invalidRequests = invalidRequests + 1


     return jsonData
    

def countPlaces(jsonData):
    results = jsonData["results"]
    #print "Length is ", len(results)
    return len(results)    


def countPlacesList(landmarks, lat, lon):
    count = 0

    for landmark in landmarks:
        #print "searching for landmark", landmark
        jsonData = placeSearch(lat, lon, landmark, distanceProximity)
        #print "jsonData is ", jsonData
        numberPlaces = countPlaces(jsonData)
        #print "number of places is ", numberPlaces
        count = count + numberPlaces
    return count

 


def calculateDistance(lat1, lon1, crimedata, crimedataLatLonList):

     felonyCount = 0
     misdemeanorCount = 0
     violationCount = 0

     for lat_lon in crimedataLatLonList:
         
         lat2, lon2 = getLatLonFromString(lat_lon)
     

         latlon1 = str(lat1) + "," + str(lon1)
         lat2 = str(lat2)
         lon2 = str(lon2)
         latlontuple1 = (lat1, lon1)
         latlontuple2 = (lat2, lon2)

         #print "l1, l2 is ", latlontuple1, latlontuple2
         
         distanceBetweenPoints = (great_circle(latlontuple1, latlontuple2).meters)
         #print "Distance is ", distanceBetweenPoints , " between coordinates ", lat1, lon1, lat2, lon2
         if distanceBetweenPoints < distanceProximity:
             latlonstring = "(" + lat2+","+lon2+")"
             indexList =  crimedata.Lat_Lon[crimedata.Lat_Lon == latlonstring].index.tolist()
             
             #print "CLOSE ", lat1, lon1, lat2, lon2
             for i in indexList:
                 if crimedata.at[i,'LAW_CAT_CD'] == "FELONY":
                     felonyCount        =  felonyCount         + 1

                 elif crimedata.at[i,'LAW_CAT_CD'] == "MISDEMEANOR":
                     misdemeanorCount   =  misdemeanorCount    + 1

                 elif crimedata.at[i,'LAW_CAT_CD'] == "VIOLATION":
                     violationCount     =  violationCount      + 1

                 else:
                     print "ERROR : unknown crimne found", crimedata[i,'LAW_CAT_CD']

     violationList.append    (violationCount)
     misdemeanorList.append  (misdemeanorCount)
     felonyList.append       (felonyCount)
     latList.append          (lat1)
     lonList.append          (lon1)
         

         
 


def getLatLonFromString(lat_lon_string):
     lat_lon_split = lat_lon_string.split(",")
     
     #latt1 = crimedataLatList[0]
     #lonn1 = crimedataLonList[1]

     lat = lat_lon_split[0][1:]
     lon = lat_lon_split[1][:-1]
  
     return lat, lon

         
def shouldExcludePoint(lat, lon):
    exrange = [[(40.579238, -74.074139), (40.515844, -74.003414)],
               [(40.566853, -74.087647), (40.543207, -73.942519)],
               [(40.626113, -73.883327), (40.602910, -73858269)]]
    if lat <= exrange[0][0][0] and lat >= exrange[0][1][0] and lon >= exrange[0][0][1] and lon <= exrange[0][1][1]:
        return True
    if lat <= exrange[1][0][0] and lat >= exrange[1][1][0] and lon >= exrange[1][0][1] and lon <= exrange[1][1][1]:
        return True
    if lat <= exrange[2][0][0] and lat >= exrange[2][1][0] and lon >= exrange[2][0][1] and lon <= exrange[2][1][1]:
        return True

if __name__ == "__main__":
    

    crimeDataLocation = "../data/CrimeData/RawData/nyc/NYPD_Complaint_Data_Historic.csv"

    crimedata = pd.read_csv(crimeDataLocation, nrows = 10000)

    crimedata = crimedata.dropna(subset = ["Lat_Lon"])

    numberOfDataPointsWanted = 70

    latStart =  40.538266
    latEnd   =  40.66953285999991
    # My latend 40.67339364999991
    # [40.538266, 40.54212679, 40.545987579999995, 40.54984836999999, 40.55370915999999, 40.55756994999999,
    #  40.561430739999984, 40.56529152999998, 40.56915231999998, 40.57301310999998, 40.576873899999974, 40.58073468999997,
    #  40.58459547999997, 40.588456269999966, 40.592317059999964, 40.59617784999996, 40.60003863999996,
    #  40.603899429999956, 40.60776021999995, 40.61162100999995, 40.61548179999995, 40.619342589999945, 40.62320337999994,
    #  40.62706416999994, 40.63092495999994, 40.634785749999935, 40.63864653999993, 40.64250732999993, 40.64636811999993,
    #  40.650228909999925, 40.65408969999992, 40.65795048999992, 40.66181127999992, 40.665672069999914, 40.66953285999991]
    #Mylist

    lonStart =  -74.268462
    lonEnd   =  -73.683440
    
    divideRegions = 100
    
    incrementFactorLat = (40.924345  - 40.538266)/divideRegions
    incrementFactorLon = (lonEnd - lonStart)/divideRegions


    print "Increment lat is ", incrementFactorLat
    print "Incrememtn Factor lon is ", incrementFactorLon
    
    # For crimes and landmarks
    distanceProximity = 500

    # Not using these landmarks 
    landmarks                = ["accounting",  "beauty_salon", "car_dealer", "car_rental", "car_repair", "car_wash", "cemetery","electrician", "embassy", "fire_station", "florist", "funeral_home", "hair_care", "insurance_agency", "laundry", "lawyer", "locksmith", "lodging","movie_rental", "moving_company", "painter","plumber",  "real_estate_agency", "roofing_contractor", "storage",  "travel_agency",  "spa", ]


    # Using all the below landmarks
    alcoholRelatedLandmarks  = ["liquor_store", "bar", ]

    placesOfWorshipLandmarks = [ "church", "hindu_temple",  "mosque", "synagogue", ]

    shoppingLandmarks        = ["electronics_store", "pharmacy", "hardware_store", "bicycle_store", "book_store", "home_goods_store", "department_store", "pet_store", "shoe_store", "shopping_mall", "clothing_store", "convenience_store",  "furniture_store", "jewelry_store", "store",  ]

    foodRelatedLandmarks     = ["restaurant", "cafe", "bakery", "meal_delivery", "meal_takeaway",  ]

    publicTransportLandmarks = ["subway_station", "train_station", "transit_station", "bus_station", "taxi_stand", ]

    doctorLandmarks          = ["dentist", "doctor",  "hospital",  "physiotherapist", "veterinary_care",  ]

    publicPlacesLandmarks    = ["airport", "amusement_park", "aquarium", "art_gallery", "bowling_alley", "campground", "casino", "city_hall",  "courthouse", "gas_station", "gym", "library", "local_government_office",  "movie_theater", "museum",  "park", "parking",  "post_office", "rv_park", "stadium", "zoo",  ]
  
    policeStationLandmarks   = ["police"]

    universityLandmarks      = ["university"]

    schoolLandmarks          = ["school"]
    bankLandmarks            = ["atm", "bank"]

    nightClublandmarks       = ["night_club"]


    alcoholCount         = 0
    placesOfWorshipCount = 0
    shoppingCount        = 0
    foodCount            = 0
    publicTransportCount = 0
    doctorCount          = 0
    publicPlacesCount    = 0
    policeStationCount   = 0
    universityCount      = 0
    schoolCount          = 0
    bankCount            = 0
    nightClubCount       = 0 
 

    latitudeList              = list()
    longitudeList             = list()
    cityList                  = list()
    alcoholCountList          = list()
    placesOfWorshipCountList  = list()
    shoppingCountList         = list()
    foodCountList             = list()
    publicTransportCountList  = list()
    doctorCountList           = list()
    publicPlacesCountList     = list()
    policeStationCountList    = list()
    universityCountList       = list()
    schoolCountList           = list()
    bankCountList             = list()
    nightClubCountList        = list()


    violationList        = list()
    misdemeanorList      = list()
    felonyList           = list()
    latList              = list()
    lonList              = list()
    complaintNumberList  = list()



    # locationsInNYC = storeNYCLocations(latStart, latEnd, lonStart, lonEnd, incrementFactorLat, incrementFactorLon)
    #print "locations in NYC", locationInNYC


    # f = open('locationsInNYC.txt', 'w')
    # simplejson.dump(locationsInNYC, f)
    # f.close()
    # p.dump(locationsInNYC, open('list_aju.p', 'wb'))

    locationsInNYC = p.load(open('list_dumps/list_aju.p', 'rb'))
    validPoints = []

    for lat, lon in locationsInNYC:
        if not shouldExcludePoint(lat, lon):
            validPoints.append((lat, lon))
    print 'total',len(locationsInNYC)
    print 'valid',len(validPoints)

    locationsInNYC = validPoints
    locationsInNYC = locationsInNYC[2344:]
    

    #for lat, lon in locationsInNYC:

         

     #crimedataLatList = crimedata.Latitude.tolist()
     #crimedataLonList = crimedata.Longitude.tolist()



    print "coordinates list is ", locationsInNYC
    #print "Length of list is ", len(locationsInNYC)
      
    
    dataPointsCount = 0
    crimedataLatLonList = crimedata.Lat_Lon.tolist()
    

    for lat, lon in locationsInNYC:
   
        print "DataPoints count is ", dataPointsCount, "Remaining data points ", len(locationsInNYC) - dataPointsCount, "lat is ", lat, "lon is ", lon

        alcoholCount         =   countPlacesList(alcoholRelatedLandmarks, lat, lon)
        placesOfWorshipCount =   countPlacesList(placesOfWorshipLandmarks, lat, lon)     
        shoppingCount        =   countPlacesList(shoppingLandmarks, lat, lon)
        foodCount            =   countPlacesList(foodRelatedLandmarks, lat, lon)
        publicTransportCount =   countPlacesList(publicTransportLandmarks, lat, lon)
        doctorCount          =   countPlacesList(doctorLandmarks, lat, lon)
        publicPlacesCount    =   countPlacesList(publicPlacesLandmarks, lat, lon)
        policeStationCount   =   countPlacesList(policeStationLandmarks, lat, lon)
        universityCount      =   countPlacesList(universityLandmarks, lat, lon)
        schoolCount          =   countPlacesList(schoolLandmarks, lat, lon)
        bankCount            =   countPlacesList(bankLandmarks, lat, lon)
        nightClubCount       =   countPlacesList(nightClublandmarks, lat, lon)  


        #print "shopping count is ", shoppingCount, "public places count is ", publicPlacesCount 


        
        latitudeList.append             (lat)
        longitudeList.append            (lon)
        cityList.append                 ("New York City")
        alcoholCountList.append         (alcoholCount)         
        placesOfWorshipCountList.append (placesOfWorshipCount) 
        shoppingCountList.append        (shoppingCount)        
        foodCountList.append            (foodCount)            
        publicTransportCountList.append (publicTransportCount) 
        doctorCountList.append          (doctorCount)          
        publicPlacesCountList.append    (publicPlacesCount)    
        policeStationCountList.append   (policeStationCount)   
        universityCountList.append      (universityCount)
        schoolCountList.append          (schoolCount)          
        bankCountList.append            (bankCount)            
        nightClubCountList.append       (nightClubCount) 
 
        dataPointsCount = dataPointsCount + 1 
 
        # calculateDistance(lat, lon, crimedata, crimedataLatLonList)

        print "Counts are ", alcoholCount, placesOfWorshipCount, shoppingCount, foodCount, publicPlacesCount, doctorCount, publicPlacesCount, policeStationCount, universityCount, schoolCount, bankCount, nightClubCount


        data =    [        (  "Latitude "               , latitudeList),
                       (  "Longitude"               , longitudeList),
                       # (  "Lat"                     , latList),
                       # (  "Lon"                     , lonList),
                       (  "City"                    , cityList),
                       (  "Alcohol Places"          , alcoholCountList),
                       (  "Places of Worship"       , placesOfWorshipCountList),
                       (  "Places to shop"          , shoppingCountList),
                       (  "Food Places"             , foodCountList),
                       (  "Public Transport Places" , publicTransportCountList),
                       (  "Doctors"                 , doctorCountList),
                       (  "Public Places"           , publicPlacesCountList),
                       (  "Police Station"          , policeStationCountList),
                       (  "University "             , universityCountList),
                       (  "Schools "                , schoolCountList),
                       (  "Banks"                   , bankCountList),
                       (  "Night Clubs"             , nightClubCountList),
                       # (  "VIOLATION CRIMES"        , violationList),
                       # (  "FELONY CRIMES"           , felonyList),
                       # (  "MISDEMEANOR CRIMES"      , misdemeanorList),
              ]
                       
        df = pd.DataFrame.from_items(data)
        df.to_csv("../data/TestDataSet/test_aju.csv", sep = ",")
        p.dump(df, open('df.p', 'wb'))

    print "Total Google Map requests is ", googleMapRequestCount
    print "Total invalid query requests is ", invalidRequests

