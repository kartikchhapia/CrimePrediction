import time
import pandas as pd
import extract_data
from config import THROTTLE
from tqdm import tqdm


def get_census_csv(locations):
    """
    Iterates over all datapoints to get census data
    Takes dictionary census data for every row and stores as an array
    saves as csv
    """
    census_dict_list = []
    chunk_size = 8
    it = iter(locations)
    with tqdm(total=len(locations)) as pbar:
        for lat, lon in it:
            time.sleep(THROTTLE)
            i = 0
            coords = [(lat, lon)]
            try:
                while i < chunk_size - 1:
                    coords.append(next(it))
                    i += 1
            except StopIteration:
                print 'No more elements'
            census_dicts = extract_data.get_census_data_async(coords)
            census_dict_list.extend(census_dicts)
            pbar.update(chunk_size)
        df_cen = pd.DataFrame.from_dict(census_dict_list)
        return df_cen


if __name__ == '__main__':
    df = pd.read_csv('../../data/TestDataSet/crime_landmarks.csv', index_col=0)
    # locs = myData[1:530, 1:3] #531 : all
    locations = df[['Lat', 'Lon']].values.tolist()
    df_cen = get_census_csv(locations)
    df_res = pd.concat([df, df_cen], axis=1)
    df_res.to_csv('../../data/TestDataSet/crime_landmarks_census.csv')