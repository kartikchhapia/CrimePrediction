# Wait this amount in seconds before each request
THROTTLE = 0.4

# Manhattan, Bronx, Brooklyn, Queens, Richmond county

CENSUS_BLOCK_CONV_URL = 'http://data.fcc.gov/api/block/2010/find?latitude={}&longitude={}&format=json'
POINT_QUERY_URL = 'http://census.ire.org/geo/1.0/boundary/?contains={},{}&sets=tracts'
CENSUS_QUERY_URL = 'http://censusdata.ire.org/{}/{}.jsonp'

# Table_ids and geo_ids are comma separated
ACS_QUERY_URL = 'https://api.censusreporter.org/1.0/data/show/acs2015_5yr?table_ids={}&geo_ids=14000US{}'

COUNTY_CODES = {
    'new_york': '061',
    'richmond': '085',
    'bronx': '005',
    'kings': '047',
    'queens': '081'
}

DECENNIAL_COLS = {
    'total_population': ['P1', 'P001001'],  # Total population
    'race_white': ['P3', 'P003002'],  # Race: White Alone
    'race_black': ['P3', 'P003003'],  # Race: Black or African American alone
    'race_american_indian_alaska': ['P3', 'P003004'],  # Race: American Indian and Alaska Native alone
    'race_asian': ['P3', 'P003005'],  # Race: Asian alone
    'race_hawaiian': ['P3', 'P003006'],  # Race: Native Hawaiian and Other Pacific Islander alone
    'race_some_other': ['P3', 'P003007'],  # Race: Some Other Race alone
    'race_two_or_more': ['P3', 'P003008'],   # Race: Two or more
    'sex_by_age_m_under_5_years': ['P12', 'P012003'],
    'sex_by_age_m_5_to_9_years': ['P12', 'P012004'],
    'sex_by_age_m_10_to_14_years': ['P12', 'P012005'],
    'sex_by_age_m_15_to_17_years': ['P12', 'P012006'],
    'sex_by_age_m_18_and_19_years': ['P12', 'P012007'],
    'sex_by_age_m_20_years': ['P12', 'P012008'],
    'sex_by_age_m_21_years': ['P12', 'P012009'],
    'sex_by_age_m_22_to_24_years': ['P12', 'P012010'],
    'sex_by_age_m_25_to_29_years': ['P12', 'P012011'],
    'sex_by_age_m_30_to_34_years': ['P12', 'P012012'],
    'sex_by_age_m_35_to_39_years': ['P12', 'P012013'],
    'sex_by_age_m_40_to_44_years': ['P12', 'P012014'],
    'sex_by_age_m_45_to_49_years': ['P12', 'P012015'],
    'sex_by_age_m_50_to_54_years': ['P12', 'P012016'],
    'sex_by_age_m_55_to_59_years': ['P12', 'P012017'],
    'sex_by_age_m_60_and_61_years': ['P12', 'P012018'],
    'sex_by_age_m_62_to_64_years': ['P12', 'P012019'],
    'sex_by_age_m_65_and_66_years': ['P12', 'P012020'],
    'sex_by_age_m_67_to_69_years': ['P12', 'P012021'],
    'sex_by_age_m_70_to_74_years': ['P12', 'P012022'],
    'sex_by_age_m_75_to_79_years': ['P12', 'P012023'],
    'sex_by_age_m_80_to_84_years': ['P12', 'P012024'],
    'sex_by_age_m_85_years_and_over': ['P12', 'P012025'],
    'sex_by_age_f_under_5_years': ['P12', 'P012027'],
    'sex_by_age_f_5_to_9_years': ['P12', 'P012028'],
    'sex_by_age_f_10_to_14_years': ['P12', 'P012029'],
    'sex_by_age_f_15_to_17_years': ['P12', 'P012030'],
    'sex_by_age_f_18_and_19_years': ['P12', 'P012031'],
    'sex_by_age_f_20_years': ['P12', 'P012032'],
    'sex_by_age_f_21_years': ['P12', 'P012033'],
    'sex_by_age_f_22_to_24_years': ['P12', 'P012034'],
    'sex_by_age_f_25_to_29_years': ['P12', 'P012035'],
    'sex_by_age_f_30_to_34_years': ['P12', 'P012036'],
    'sex_by_age_f_35_to_39_years': ['P12', 'P012037'],
    'sex_by_age_f_40_to_44_years': ['P12', 'P012038'],
    'sex_by_age_f_45_to_49_years': ['P12', 'P012039'],
    'sex_by_age_f_50_to_54_years': ['P12', 'P012040'],
    'sex_by_age_f_55_to_59_years': ['P12', 'P012041'],
    'sex_by_age_f_60_and_61_years': ['P12', 'P012042'],
    'sex_by_age_f_62_to_64_years': ['P12', 'P012043'],
    'sex_by_age_f_65_and_66_years': ['P12', 'P012044'],
    'sex_by_age_f_67_to_69_years': ['P12', 'P012045'],
    'sex_by_age_f_70_to_74_years': ['P12', 'P012046'],
    'sex_by_age_f_75_to_79_years': ['P12', 'P012047'],
    'sex_by_age_f_80_to_84_years': ['P12', 'P012048'],
    'sex_by_age_f_85_years_and_over': ['P12', 'P012049'],
    'ho_husband_wife': ['P18', 'P018003'],
    'm_ho_no_wife': ['P18', 'P018005'],
    'f_ho_no_hus': ['P18', 'P018006'],
    'ho_alone': ['P18', 'P018008'],
    'ho_not_alone': ['P18', 'P018009'],
    'families': ['P35', 'P035001'],
    'hous_units': ['H1', 'H001001'],
    'hous_occupied': ['H3', 'H003002'],
    'hous_vacant': ['H3', 'H003003'],
    'owned_mortgage_loan': ['H4', 'H004002'],
    'owned_free_clear': ['H4', 'H004003'],
    'renter_occupied': ['H4', 'H004004']
}

#TODO:
# Education
ACS_COLS= {
    'median_income': ['B06011', 'B06011001'],
    'gini_income_inequality': ['B19083', 'B19083001'],
    "in_labor_force": ["B23025", "B23025002"],
    "civilian_labor_force": ["B23025", "B23025003"],
    "employed": ["B23025", "B23025004"],
    "unemployed": ["B23025", "B23025005"],
    "armed_forces": ["B23025", "B23025006"],
    "not_in_labor_force": ["B23025", "B23025007"]
}