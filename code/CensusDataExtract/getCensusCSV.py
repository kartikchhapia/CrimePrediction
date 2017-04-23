import numpy as np
import csv
import extract_data
import cPickle as p

def get_census_csv(pointList):
    """
    Iterates over all datapoints to get census data
    Takes dictionary census data for every row and stores as an array
    saves as csv
    """
    count = 0
    dictList = []
        
    for i in pointList :
        xDict = extract_data.get_census_data(i[0],i[1],year='2010')
        dictList.append(xDict)
        count += 1
        print 'num datapoints read:'+ str(count)

    valList = map(lambda x : x.values(), dictList)
    valList = np.array(valList)
    with open('censusListAnish.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(valList)
    print 'writing done'
    return valList


if __name__ == '__main__':
    locationsInNYC = p.load(open('../list_dumps/list_Anish.p', 'rb'))
    data = get_census_csv(locationsInNYC)