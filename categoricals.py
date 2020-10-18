import settings

CATEGORICAL_ARRAYS = {
    "channel": ['R', 'B', 'C'], # Retail, Broker, Correspondent
    "seller": [
        'OTHER',
        'AMERIHOME MORTGAGE COMPANY, LLC',
        'CALIBER HOME LOANS, INC.',
        'CITIMORTGAGE, INC.',
        'CMG MORTGAGE, INC',
        'DITECH FINANCIAL LLC',
        'EAGLE HOME MORTGAGE, LLC',
        'FAIRWAY INDEPENDENT MORTGAGE CORPORATION',
        'FIFTH THIRD BANK',
        'FINANCE OF AMERICA MORTGAGE LLC',
        'FLAGSTAR BANK, FSB',
        'FRANKLIN AMERICAN MORTGAGE COMPANY',
        'FREEDOM MORTGAGE CORP.',
        'GUILD MORTGAGE COMPANY',
        'HOMEBRIDGE FINANCIAL SERVICES, INC.',
        'IMPAC MORTGAGE CORP.',
        [
            'J.P. MORGAN MADISON AVENUE SECURITIES TRUST, SERIES 2015-1',
            'JPMORGAN CHASE BANK, NATIONAL ASSOCIATION'
        ],
        'LAKEVIEW LOAN SERVICING, LLC',
        'LOANDEPOT.COM, LLC',
        'MOVEMENT MORTGAGE, LLC',
        'NATIONSTAR MORTGAGE, LLC',
        'PENNYMAC CORP.',
        [
            'PMT CREDIT RISK TRANSFER TRUST 2015-2',
            'PMT CREDIT RISK TRANSFER TRUST 2016-1'
        ],
        'PMTT4',
        'PROVIDENT FUNDING ASSOCIATES, L.P.',
        [
            'QUICKEN LOANS INC.',
            'QUICKEN LOANS, LLC'
        ],
        'STEARNS LENDING, LLC',
        [
            'SUNTRUST BANK',
            'SUNTRUST MORTGAGE INC.',
            'TRUIST BANK (FORMERLY SUNTRUST BANK)'
        ],
        'U.S. BANK N.A.',
        [
            'UNITED SHORE FINANCIAL SERVICES, LLC D/B/A UNITED WHOLESALE MORTGAGE',
            'UNITED SHORE FINANCIAL SERVICES, LLC DBA UNITED WHOLESALE MORTGAGE'
        ],
        [
            'WELLS FARGO BANK, N.A.',
            'WELLS FARGO CREDIT RISK TRANSFER SECURITIES TRUST 2015'
        ]
    ],
    "first_time_homebuyer": ['U', 'Y', 'N'], # unknown, yes, no
    "loan_purpose": ['P', 'C', 'R', 'U'], # purchase, cash-out refinance, no cash-out refinance, refinance - not specified
    "property_type": ['SF', 'CO', 'CP', 'MH', 'PU'], # single-family, condo, co-op, manufactured housing, PUD
    "occupancy_status": ['P', 'S', 'I'], # principal residence, second home, investment property
    "property_state": [
        'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
        'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD',
        'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ',
        'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD',
        'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY'
    ],
    "product_type": ['FRM'] # fixed-rate mortgage
}

def get_index_maps():
    index_maps = {}
    for category in CATEGORICAL_ARRAYS:
        index_maps[category] = array_to_index_map(CATEGORICAL_ARRAYS[category])
    return index_maps

def array_to_index_map(array):
    index_map = {}
    for i, val in enumerate(array):
        if isinstance(val, list):
            for v in val:
                index_map[v] = i
        else:
            index_map[val] = i
    return index_map

CATEGORICAL_INDEX_MAP = get_index_maps()

def get_single_foreclosure_data(train, category, value):
    loans = train[(train[category]==CATEGORICAL_INDEX_MAP[category][value])]
    foreclosures = loans[(loans[settings.FORECLOSURE_TARGET]==True)]
    return loans.shape[0], foreclosures.shape[0]

def get_all_foreclosure_data(train, category):
    foreclosure_data = {}
    for value in CATEGORICAL_ARRAYS[category]:
        loans, foreclosures = get_single_foreclosure_data(train, category, value)
        foreclosure_data[value] = {'loan_count': loans, 'foreclosure_count': foreclosures, 'ratio': 1.0*foreclosures/loans}
    return foreclosure_data

def get_all_foreclosure_data_with_ranking(train, category):
    foreclosure_data = get_all_foreclosure_data(train, category)
    sorted_foreclosure_list = sorted(foreclosure_data.items(), key=lambda d: d[1]['ratio'])
    sorted_foreclosure_data = {}
    for index in range(len(sorted_foreclosure_list)):
        sorted_foreclosure_data[sorted_foreclosure_list[index][0]] = sorted_foreclosure_list[index][1]
        sorted_foreclosure_data[sorted_foreclosure_list[index][0]]['ranking'] = index
    return sorted_foreclosure_data
