# Bangalore monitoring stations data
# Official KSPCB (Karnataka State Pollution Control Board) monitoring stations

BANGALORE_STATIONS = [
    {
        "id": "bapuji_nagar",
        "name": "Bapuji Nagar",
        "coordinates": {"latitude": 12.9650, "longitude": 77.5850},
        "address": "Bapuji Nagar, Bangalore",
        "type": "residential"
    },
    {
        "id": "btm_layout",
        "name": "BTM Layout",
        "coordinates": {"latitude": 12.9165, "longitude": 77.6101},
        "address": "BTM Layout, Bangalore",
        "type": "residential"
    },
    {
        "id": "bwssb_kadabesanahalli",
        "name": "BWSSB Kadabesanahalli",
        "coordinates": {"latitude": 12.9344, "longitude": 77.6783},
        "address": "Kadabesanahalli, Bangalore",
        "type": "residential"
    },
    {
        "id": "city_railway_station",
        "name": "City Railway Station/Majestic",
        "coordinates": {"latitude": 12.9767, "longitude": 77.5718},
        "address": "City Railway Station, Bangalore",
        "type": "traffic"
    },
    {
        "id": "hebbal",
        "name": "Hebbal",
        "coordinates": {"latitude": 13.0358, "longitude": 77.5970},
        "address": "Hebbal, Bangalore",
        "type": "residential"
    },
    {
        "id": "hombegowda_nagar",
        "name": "Hombegowda Nagar",
        "coordinates": {"latitude": 12.9600, "longitude": 77.6100},
        "address": "Hombegowda Nagar, Bangalore",
        "type": "residential"
    },
    {
        "id": "jayanagar_5th_block",
        "name": "Jayanagar 5th Block",
        "coordinates": {"latitude": 12.9250, "longitude": 77.5838},
        "address": "Jayanagar 5th Block, Bangalore",
        "type": "residential"
    },
    {
        "id": "jigani_industrial_area",
        "name": "Jigani Industrial Area",
        "coordinates": {"latitude": 12.7800, "longitude": 77.6350},
        "address": "Jigani Industrial Area, Bangalore",
        "type": "industrial"
    },
    {
        "id": "kasturi_nagar_rto",
        "name": "Kasturi Nagar RTO",
        "coordinates": {"latitude": 13.0108, "longitude": 77.6544},
        "address": "Kasturi Nagar RTO, Bangalore",
        "type": "traffic"
    },
    {
        "id": "kaviika_mysore_road",
        "name": "KAVIKA Mysore Road",
        "coordinates": {"latitude": 12.9591, "longitude": 77.5236},
        "address": "KAVIKA Mysore Road, Bangalore",
        "type": "traffic"
    },
    {
        "id": "nimhans",
        "name": "NIMHANS",
        "coordinates": {"latitude": 12.9428, "longitude": 77.5963},
        "address": "NIMHANS, Bangalore",
        "type": "residential"
    },
    {
        "id": "nisarga_bhavan",
        "name": "Nisarga Bhavan/Basaveshwaranagar",
        "coordinates": {"latitude": 12.9869, "longitude": 77.5385},
        "address": "Nisarga Bhavan, Bangalore",
        "type": "residential"
    },
    {
        "id": "peenya_industrial_area",
        "name": "Peenya Industrial Area",
        "coordinates": {"latitude": 13.0297, "longitude": 77.5202},
        "address": "Peenya Industrial Area, Bangalore",
        "type": "industrial"
    },
    {
        "id": "rv_engineering_college",
        "name": "RV Engineering College, Kengeri",
        "coordinates": {"latitude": 12.9237, "longitude": 77.4989},
        "address": "RV Engineering College, Kengeri, Bangalore",
        "type": "residential"
    },
    {
        "id": "silk_board",
        "name": "Silk Board",
        "coordinates": {"latitude": 12.9176, "longitude": 77.6226},
        "address": "Silk Board, Bangalore",
        "type": "traffic"
    }
]

def get_station_by_id(station_id):
    """Get station details by ID"""
    for station in BANGALORE_STATIONS:
        if station['id'] == station_id:
            return station
    return None

def get_stations_by_type(station_type):
    """Get all stations of a specific type"""
    return [station for station in BANGALORE_STATIONS if station['type'] == station_type]

def get_all_station_coordinates():
    """Get coordinates of all stations for mapping"""
    return [
        {
            'id': station['id'],
            'name': station['name'],
            'lat': station['coordinates']['latitude'],
            'lon': station['coordinates']['longitude'],
            'type': station['type']
        }
        for station in BANGALORE_STATIONS
    ]

def search_stations(query):
    """Search stations by name or address"""
    query_lower = query.lower()
    results = []

    for station in BANGALORE_STATIONS:
        if (query_lower in station['name'].lower() or
            query_lower in station['address'].lower()):
            results.append(station)

    return results

# Comprehensive Bangalore areas database for location search
BANGALORE_AREAS = {
    # Residential Areas
    "Koramangala": {"lat": 12.9352, "lon": 77.6245},
    "Indiranagar": {"lat": 12.9783, "lon": 77.6408},
    "Whitefield": {"lat": 12.9698, "lon": 77.7500},
    "HSR Layout": {"lat": 12.9081, "lon": 77.6476},
    "Marathahalli": {"lat": 12.9591, "lon": 77.6974},
    "BTM Layout": {"lat": 12.9165, "lon": 77.6101},
    "Jayanagar": {"lat": 12.9250, "lon": 77.5838},
    "Rajajinagar": {"lat": 12.9889, "lon": 77.5542},
    "Malleshwaram": {"lat": 13.0030, "lon": 77.5640},
    "Basavanagudi": {"lat": 12.9417, "lon": 77.5750},
    "Frazer Town": {"lat": 12.9980, "lon": 77.6140},
    "Seshadripuram": {"lat": 12.9930, "lon": 77.5800},
    "Ulsoor": {"lat": 12.9810, "lon": 77.6280},
    "Richmond Town": {"lat": 12.9660, "lon": 77.6070},
    "Shivajinagar": {"lat": 12.9850, "lon": 77.6050},
    "Cunningham Road": {"lat": 12.9850, "lon": 77.5960},
    "Sadashivanagar": {"lat": 13.0070, "lon": 77.5800},
    "Vijayanagar": {"lat": 12.9719, "lon": 77.5290},
    "Rajajinagar": {"lat": 12.9889, "lon": 77.5542},
    "Mahalakshmi Layout": {"lat": 13.0130, "lon": 77.5510},
    "Nagarbhavi": {"lat": 12.9570, "lon": 77.5120},
    "Jalahalli": {"lat": 13.0780, "lon": 77.5480},
    "Vidyaranyapura": {"lat": 13.0770, "lon": 77.5570},
    "Yelahanka": {"lat": 13.1007, "lon": 77.5963},
    "Sahakara Nagar": {"lat": 13.0620, "lon": 77.5800},
    "Hebbal": {"lat": 13.0358, "lon": 77.5970},
    "Kasturi Nagar": {"lat": 13.0108, "lon": 77.6544},
    "R.T. Nagar": {"lat": 13.0220, "lon": 77.5960},
    "Ganga Nagar": {"lat": 13.0200, "lon": 77.5800},
    "Jeevanbhimanagar": {"lat": 12.9650, "lon": 77.6550},
    "New Thippasandra": {"lat": 12.9730, "lon": 77.6530},
    "Murugeshpalya": {"lat": 12.9560, "lon": 77.6540},
    "Hennur": {"lat": 13.0250, "lon": 77.6400},
    "Kalyan Nagar": {"lat": 13.0220, "lon": 77.6400},
    "HRBR Layout": {"lat": 13.0300, "lon": 77.6300},
    "Horamavu": {"lat": 13.0270, "lon": 77.6600},
    "Banaswadi": {"lat": 13.0140, "lon": 77.6510},
    "Ramamurthy Nagar": {"lat": 13.0120, "lon": 77.6770},
    "Kalkere": {"lat": 13.0300, "lon": 77.6700},
    "Rachenahalli": {"lat": 13.0200, "lon": 77.6900},
    "Jakkur": {"lat": 13.0780, "lon": 77.6060},
    "Yelahanka New Town": {"lat": 13.1000, "lon": 77.5800},
    "Kodigehalli": {"lat": 13.0700, "lon": 77.5800},
    "Bagalakunte": {"lat": 13.0800, "lon": 77.5100},
    "Chikkabanavara": {"lat": 13.0800, "lon": 77.5000},
    "Hesaraghatta": {"lat": 13.1400, "lon": 77.4900},
    "Soladevanahalli": {"lat": 13.0200, "lon": 77.4800},
    "Hennur Cross": {"lat": 13.0300, "lon": 77.6500},
    "B Channasandra": {"lat": 12.9200, "lon": 77.6800},
    "Thogur": {"lat": 12.7800, "lon": 77.6350},
    "Doddaballapur": {"lat": 13.2900, "lon": 77.5400},
    "Nelamangala": {"lat": 13.0900, "lon": 77.3900},
    "Magadi": {"lat": 12.9600, "lon": 77.2200},
    "Ramanagara": {"lat": 12.7200, "lon": 77.2800},
    "Channapatna": {"lat": 12.6500, "lon": 77.2000},
    "Kanakapura": {"lat": 12.5500, "lon": 77.4200},
    "Hoskote": {"lat": 13.0700, "lon": 77.7900},
    "Devanahalli": {"lat": 13.2500, "lon": 77.7100},
    "Bidadi": {"lat": 12.8000, "lon": 77.3900},
    "Anekal": {"lat": 12.7100, "lon": 77.6900},
    "Attibele": {"lat": 12.7800, "lon": 77.7700},
    "Sarjapur": {"lat": 12.8600, "lon": 77.7800},
    "Sarjapur Road": {"lat": 12.9200, "lon": 77.6800},
    "Bellandur": {"lat": 12.9300, "lon": 77.6700},
    "Marathahalli-Sarjapur Outer Ring Road": {"lat": 12.9500, "lon": 77.7000},
    "Kadugodi": {"lat": 12.9900, "lon": 77.7600},
    "Hoodi": {"lat": 12.9900, "lon": 77.7200},
    "Brookefield": {"lat": 12.9700, "lon": 77.7200},
    "Mahadevapura": {"lat": 12.9900, "lon": 77.6900},
    "Garudachar Palya": {"lat": 12.9800, "lon": 77.6900},
    "Devarabeesanahalli": {"lat": 12.9300, "lon": 77.7200},
    "Kundalahalli": {"lat": 12.9700, "lon": 77.7200},
    "Marathahalli Bridge": {"lat": 12.9600, "lon": 77.7000},
    "Panathur": {"lat": 12.9400, "lon": 77.7100},
    "Varthur": {"lat": 12.9400, "lon": 77.7400},
    "Gunjur": {"lat": 12.9200, "lon": 77.7400},
    "Whitefield Main Road": {"lat": 12.9700, "lon": 77.7500},
    "ITPL": {"lat": 12.9800, "lon": 77.7500},
    "Pattandur Agrahara": {"lat": 12.9500, "lon": 77.7600},
    "Channasandra": {"lat": 12.9200, "lon": 77.6800},
    "Kaikondrahalli": {"lat": 12.9100, "lon": 77.6800},
    "Sarjapur Main Road": {"lat": 12.8600, "lon": 77.7800},
    "HSR Layout Sector 1": {"lat": 12.9100, "lon": 77.6500},
    "HSR Layout Sector 2": {"lat": 12.9050, "lon": 77.6450},
    "HSR Layout Sector 3": {"lat": 12.9000, "lon": 77.6400},
    "HSR Layout Sector 4": {"lat": 12.8950, "lon": 77.6350},
    "HSR Layout Sector 5": {"lat": 12.8900, "lon": 77.6300},
    "HSR Layout Sector 6": {"lat": 12.8850, "lon": 77.6250},
    "HSR Layout Sector 7": {"lat": 12.8800, "lon": 77.6200},
    "Bommanahalli": {"lat": 12.9000, "lon": 77.6200},
    "Begur": {"lat": 12.8700, "lon": 77.6300},
    "Hongasandra": {"lat": 12.8800, "lon": 77.6400},
    "Garebhavipalya": {"lat": 12.8700, "lon": 77.6500},
    "Singasandra": {"lat": 12.8800, "lon": 77.6500},
    "Kudlu Gate": {"lat": 12.8900, "lon": 77.6500},
    "Bommasandra": {"lat": 12.8200, "lon": 77.6900},
    "Electronic City Phase 1": {"lat": 12.8399, "lon": 77.6770},
    "Electronic City Phase 2": {"lat": 12.8500, "lon": 77.6700},
    "Konappana Agrahara": {"lat": 12.8700, "lon": 77.6800},
    "Hosa Road": {"lat": 12.8700, "lon": 77.6600},
    "Parappana Agrahara": {"lat": 12.8500, "lon": 77.6800},
    "Naganathapura": {"lat": 12.8700, "lon": 77.6900},
    "Doddathoguru": {"lat": 12.8100, "lon": 77.6900},
    "Ananth Nagar": {"lat": 12.9500, "lon": 77.5800},
    "JP Nagar": {"lat": 12.9100, "lon": 77.5800},
    "JP Nagar Phase 1": {"lat": 12.9100, "lon": 77.5800},
    "JP Nagar Phase 2": {"lat": 12.9100, "lon": 77.5750},
    "JP Nagar Phase 3": {"lat": 12.9100, "lon": 77.5700},
    "JP Nagar Phase 4": {"lat": 12.9100, "lon": 77.5650},
    "JP Nagar Phase 5": {"lat": 12.9100, "lon": 77.5600},
    "JP Nagar Phase 6": {"lat": 12.9100, "lon": 77.5550},
    "JP Nagar Phase 7": {"lat": 12.9100, "lon": 77.5500},
    "JP Nagar Phase 8": {"lat": 12.9100, "lon": 77.5450},
    "JP Nagar Phase 9": {"lat": 12.9100, "lon": 77.5400},
    "Bannerghatta Road": {"lat": 12.8900, "lon": 77.6000},
    "Bilekahalli": {"lat": 12.8900, "lon": 77.6100},
    "Arekere": {"lat": 12.8800, "lon": 77.5900},
    "Sarvabhouma Nagar": {"lat": 12.9200, "lon": 77.5200},
    "Banashankari": {"lat": 12.9200, "lon": 77.5700},
    "Banashankari Stage I": {"lat": 12.9200, "lon": 77.5700},
    "Banashankari Stage II": {"lat": 12.9200, "lon": 77.5650},
    "Banashankari Stage III": {"lat": 12.9200, "lon": 77.5600},
    "Padmanabhanagar": {"lat": 12.9200, "lon": 77.5600},
    "Chikkalasandra": {"lat": 12.9100, "lon": 77.5500},
    "Uttarahalli": {"lat": 12.9050, "lon": 77.5450},
    "Kengeri": {"lat": 12.9200, "lon": 77.4800},
    "Rajarajeshwari Nagar": {"lat": 12.9200, "lon": 77.5100},
    "Kenchanahalli": {"lat": 12.9000, "lon": 77.5200},
    "Nagadevanahalli": {"lat": 12.8800, "lon": 77.5200},
    "Gottigere": {"lat": 12.8500, "lon": 77.5800},
    "Hulimavu": {"lat": 12.8700, "lon": 77.6000},
    "Madiwala": {"lat": 12.9200, "lon": 77.6200},
    "Koramangala 1st Block": {"lat": 12.9250, "lon": 77.6300},
    "Koramangala 2nd Block": {"lat": 12.9300, "lon": 77.6250},
    "Koramangala 3rd Block": {"lat": 12.9350, "lon": 77.6200},
    "Koramangala 4th Block": {"lat": 12.9300, "lon": 77.6300},
    "Koramangala 5th Block": {"lat": 12.9350, "lon": 77.6150},
    "Koramangala 6th Block": {"lat": 12.9400, "lon": 77.6100},
    "Koramangala 7th Block": {"lat": 12.9450, "lon": 77.6050},
    "Koramangala 8th Block": {"lat": 12.9500, "lon": 77.6000},
    "Ejipura": {"lat": 12.9450, "lon": 77.6250},
    "Tavarekere": {"lat": 12.9200, "lon": 77.6100},
    "Jakkasandra": {"lat": 12.9200, "lon": 77.6200},
    "Srinagar": {"lat": 12.9700, "lon": 77.5800},
    "Shantinagar": {"lat": 12.9600, "lon": 77.6000},
    "Wilson Garden": {"lat": 12.9500, "lon": 77.5950},
    "Lalbagh": {"lat": 12.9507, "lon": 77.5848},
    "Ashok Nagar": {"lat": 12.9700, "lon": 77.6000},
    "Cunningham Road": {"lat": 12.9850, "lon": 77.5960},
    "Vasanth Nagar": {"lat": 12.9900, "lon": 77.5900},
    "Austin Town": {"lat": 12.9650, "lon": 77.6100},
    "Langford Town": {"lat": 12.9600, "lon": 77.6000},
    "Richmond Town": {"lat": 12.9660, "lon": 77.6070},
    "Bowring Hospital": {"lat": 12.9700, "lon": 77.6000},
    "Tasker Town": {"lat": 12.9700, "lon": 77.6100},
    "Commercial Street": {"lat": 12.9800, "lon": 77.6100},
    "Cottonpet": {"lat": 12.9800, "lon": 77.6000},
    "Chamarajpet": {"lat": 12.9600, "lon": 77.5700},
    "Sultanpet": {"lat": 12.9600, "lon": 77.5600},
    "Viveknagar": {"lat": 12.9600, "lon": 77.5500},
    "Halasuru": {"lat": 12.9800, "lon": 77.6200},
    "Murphy Town": {"lat": 12.9700, "lon": 77.6300},
    "Domlur": {"lat": 12.9600, "lon": 77.6400},
    "Richards Town": {"lat": 12.9900, "lon": 77.6100},
    "Race Course Road": {"lat": 12.9800, "lon": 77.5800},
    "Residency Road": {"lat": 12.9750, "lon": 77.6100},
    "St. Marks Road": {"lat": 12.9750, "lon": 77.6000},
    "Museum Road": {"lat": 12.9750, "lon": 77.6150},
    "Cubbon Road": {"lat": 12.9750, "lon": 77.5950},
    "Vidhana Soudha": {"lat": 12.9800, "lon": 77.5900},
    "Raj Bhavan": {"lat": 12.9800, "lon": 77.5900},
    "High Grounds": {"lat": 12.9800, "lon": 77.5900},
    "Albert Victor Road": {"lat": 12.9750, "lon": 77.5800},
    "Kasturba Road": {"lat": 12.9750, "lon": 77.6000},
    "Hudson Circle": {"lat": 12.9700, "lon": 77.6000},
    "Lalbagh Road": {"lat": 12.9500, "lon": 77.5850},
    "Double Road": {"lat": 12.9450, "lon": 77.5800},
    "Bugle Rock": {"lat": 12.9400, "lon": 77.5800},
    "Dharmaram College": {"lat": 12.9400, "lon": 77.5700},
    "Christ University": {"lat": 12.9350, "lon": 77.6050},
    "Hosur Road": {"lat": 12.9200, "lon": 77.6200},
    "Mysore Road": {"lat": 12.9500, "lon": 77.5300},
    "Tumkur Road": {"lat": 13.0300, "lon": 77.5600},
    "Bellary Road": {"lat": 13.0800, "lon": 77.5600},
    "Old Madras Road": {"lat": 13.0800, "lon": 77.5800},
    "Varthur Road": {"lat": 12.9400, "lon": 77.7400},
    "Sarjapur Road": {"lat": 12.9200, "lon": 77.6800},
    "Marathahalli Road": {"lat": 12.9600, "lon": 77.7000},
    "Whitefield Road": {"lat": 12.9700, "lon": 77.7500},
    "Kadugodi Road": {"lat": 12.9900, "lon": 77.7600},
    "Hoodi Circle": {"lat": 12.9900, "lon": 77.7200},
    "Mahadevapura Junction": {"lat": 12.9900, "lon": 77.6900},
    "Marathahalli Bridge": {"lat": 12.9600, "lon": 77.7000},
    "Panathur Junction": {"lat": 12.9400, "lon": 77.7100},
    "Varthur Junction": {"lat": 12.9400, "lon": 77.7400},
    "Gunjur Junction": {"lat": 12.9200, "lon": 77.7400},
    "Whitefield Main Road Junction": {"lat": 12.9700, "lon": 77.7500},
    "ITPL Junction": {"lat": 12.9800, "lon": 77.7500},
    "Pattandur Agrahara Junction": {"lat": 12.9500, "lon": 77.7600},
    "Channasandra Junction": {"lat": 12.9200, "lon": 77.6800},
    "Kaikondrahalli Junction": {"lat": 12.9100, "lon": 77.6800},
    "Sarjapur Main Road Junction": {"lat": 12.8600, "lon": 77.7800},
    "HSR Layout Ring Road": {"lat": 12.9100, "lon": 77.6500},
    "Bommanahalli Junction": {"lat": 12.9000, "lon": 77.6200},
    "Begur Junction": {"lat": 12.8700, "lon": 77.6300},
    "Hongasandra Junction": {"lat": 12.8800, "lon": 77.6400},
    "Garebhavipalya Junction": {"lat": 12.8700, "lon": 77.6500},
    "Singasandra Junction": {"lat": 12.8800, "lon": 77.6500},
    "Kudlu Gate Junction": {"lat": 12.8900, "lon": 77.6500},
    "Bommasandra Junction": {"lat": 12.8200, "lon": 77.6900},
    "Electronic City Junction": {"lat": 12.8400, "lon": 77.6770},
    "Konappana Agrahara Junction": {"lat": 12.8700, "lon": 77.6800},
    "Hosa Road Junction": {"lat": 12.8700, "lon": 77.6600},
    "Parappana Agrahara Junction": {"lat": 12.8500, "lon": 77.6800},
    "Naganathapura Junction": {"lat": 12.8700, "lon": 77.6900},
    "Doddathoguru Junction": {"lat": 12.8100, "lon": 77.6900},
    "Ananth Nagar Junction": {"lat": 12.9500, "lon": 77.5800},
    "JP Nagar Ring Road": {"lat": 12.9100, "lon": 77.5800},
    "Bannerghatta Road Junction": {"lat": 12.8900, "lon": 77.6000},
    "Bilekahalli Junction": {"lat": 12.8900, "lon": 77.6100},
    "Arekere Junction": {"lat": 12.8800, "lon": 77.5900},
    "Sarvabhouma Nagar Junction": {"lat": 12.9200, "lon": 77.5200}
}
