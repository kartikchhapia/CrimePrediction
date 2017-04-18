import urllib, json
import pandas as pd



myKey = "AIzaSyAQODArFSeYSO-_S3F-OzyMggJNb5Xlwcc"
myKeyNYCCheck = "AIzaSyBESs0RkTlQ8wNL2kQxkPkIuxsijbMpkA4"

myKeyPlacesSearch = "AIzaSyB3oisflwK_MsKXJZ9HkPd2WgHfgSBlPYs"


countiesNYC = ["Queens", "Manhattan", "Staten Island", "Bronx", "Brooklyn", "Queens County", "New York"]


def storeNYCLocations(latStart, latEnd, lonStart, lonEnd, incrementFactorLat, incrementFactorLon):
    locationsInNYC = list()
    countLocationsInNYC = 0
    countLocationsOutsideNYC = 0
    totalCount = 0
    lon = lonStart
    
    while (lon <= lonEnd):
        lat = latStart
        while (lat <= latEnd):
            if (totalCount % 50 == 0):
               print "Count is ", totalCount
            latlong = str(lat)+","+str(lon)
            Myurl = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+latlong+"&key="+myKeyNYCCheck
            response = urllib.urlopen(Myurl)
            jsonRaw = response.read()
            jsonData = json.loads(jsonRaw)
            results = jsonData["results"]
            localityinNYC = False
            for result in results:
                #print "formatted address is ", result["formatted_address"]
                for county in countiesNYC:
                   if county + ", NY" in result["formatted_address"]:
                      localityinNYC = True
                      break
            if localityinNYC == False:
                print "Location not in NYC Latitude is ", lat, "Longtitude is ", lon
                countLocationsOutsideNYC = countLocationsOutsideNYC + 1
                for result in results:
                    print "formatted address is ", result["formatted_address"]
            else:
                locationsInNYC.append((lat,lon))
                countLocationsInNYC = countLocationsInNYC + 1
                

            lat = lat + incrementFactorLat
            totalCount = totalCount + 1
        lon = lon + incrementFactorLon
        print "Lon is ", lon
        
    print "Count of locations inside NYC is ",  countLocationsInNYC
    print "Count of locations outside NYC is ", countLocationsOutsideNYC
    return locationsInNYC 


def placeSearch(lat, lon, myType, radius):
     locationString = str(lat)+","+str(lon)
     myUrl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+locationString+"&radius="+str(radius)+"&types="+myType+"&sensor=false&key="+myKeyPlacesSearch
     response = urllib.urlopen(myUrl)
     jsonRaw = response.read()
     jsonData = json.loads(jsonRaw)
     return jsonData
    

def countPlaces(jsonData):
    results = jsonData["results"]
    #print "Length is ", len(results)
    return len(results)    


def countPlacesList(landmarks, lat, lon):
    count = 0

    for landmark in landmarks:
        jsonData = placeSearch(lat, lon, landmark, 1000)
        numberPlaces = countPlaces(jsonData)
        count = count + numberPlaces
    return count

    
    

if __name__ == "__main__":


    latStart =  40.538266
    latEnd   =  40.924345 
    
    lonStart =  -74.268462
    lonEnd   =  -73.683440
    
    divideRegions = 10
    
    incrementFactorLat = (latEnd - latStart)/divideRegions
    incrementFactorLon = (lonEnd - lonStart)/divideRegions


    landmarks = ["accounting",  "beauty_salon", "car_dealer", "car_rental", "car_repair", "car_wash", "cemetery","electrician", "embassy", "fire_station", "florist", "funeral_home", "hair_care", "insurance_agency", "laundry", "lawyer", "locksmith", "lodging","movie_rental", "moving_company", "painter","plumber",  "real_estate_agency", "roofing_contractor", "storage",  "travel_agency",  "spa", ]

    alcoholRelatedLandmarks = ["liquor_store", "bar", ]

    placesOfWorshipLandmarks = [ "church", "hindu_temple",  "mosque", "synagogue", ]

    shoppingLandmarks = ["electronics_store", "pharmacy", "hardware_store", "bicycle_store", "book_store", "home_goods_store", "department_store", "pet_store", "shoe_store", "shopping_mall", "clothing_store", "convenience_store",  "furniture_store", "jewelry_store", "store",  ]

    foodRelatedLandmarks = ["restaurant", "cafe", "bakery", "meal_delivery", "meal_takeaway",  ]

    publicTransportLandmarks = ["subway_station", "train_station", "transit_station", "bus_station", "taxi_stand", ]

    doctorLandmarks = ["dentist", "doctor",  "hospital",  "physiotherapist", "veterinary_care",  ]

    publicPlacesLandmarks = ["airport", "amusement_park", "aquarium", "art_gallery", "bowling_alley", "campground", "casino", "city_hall",  "courthouse", "gas_station", "gym", "library", "local_government_office",  "movie_theater", "museum",  "park", "parking",  "post_office", "rv_park", "stadium", "zoo",  ]
  
    policeStationLandmarks = ["police"]

    universityLandmarks = ["university"]

    schoolLandmarks = ["school"]

    bankLandmarks = ["atm", "bank"]

    nightClublandmarks = ["night_club"]

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
 
    fv_list = list()



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


    locationsInNYC = storeNYCLocations(latStart, latEnd, lonStart, lonEnd, incrementFactorLat, incrementFactorLon)

    #print "coordinates list is ", locationsInNYC
    #print "Length of list is ", len(locationsInNYC)
      

    dataPointsCount = 0
    for lat, lon in locationsInNYC[:10]:
   
        print "DataPoints count is ", dataPointsCount, "Remaining data points ", len(locationsInNYC) - dataPointsCount

        lat =  40.538266
        lon = -74.209959


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


    data =    [        ("Latitude " , latitudeList),
                       (  "Longitude" , longitudeList),
                       ("City" , cityList),
                       (  "Alcohol Places" , alcoholCountList),
                       (  "Places of Worship" , placesOfWorshipCountList),
                       (  "Places to shop" , shoppingCountList),
                       (  "Food Places" , foodCountList),
                       (  "Public Transport Places" , publicTransportCountList),
                       (  "Doctors " , doctorCountList),
                       (  "Public Places" , publicPlacesCountList),
                       (  "Police Station" , policeStationCountList),
                       (  "University " , universityCountList),
                       (  "Schools " , schoolCountList),
                       (  "Banks" , bankCountList),
                       (  "Night Clubs" , nightClubCountList),
              ]
                       
    df = pd.DataFrame.from_items(data)
    df.to_csv("test.csv", sep = ",")
