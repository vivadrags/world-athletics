from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'passwd': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}

# Request delay between API calls (in seconds)
REQUEST_DELAY = 1

# HTTP headers for requests
HEADER = {
    "User-Agent": "Mozilla/5.0"
}

# Month name to number mapping for date conversion
MONTH_DICT = {
    "JAN": "01", "FEB": "02", "MAR": "03", "APR": "04",
    "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08",
    "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"
}

# Event dictionary mapping event IDs to [event_name, url_name, category, gender]
EVENT_DICT = {
    "10230285": ["50m", "50-metres", "sprints", "Men"],
    "10230287": ["55m", "55-metres", "sprints", "Men"],
    "10229683": ["60m", "60-metres", "sprints", "Men"],
    "10229630": ["100m", "100-metres", "sprints", "Men"],
    "10229605": ["200m", "200-metres", "sprints", "Men"],
    "10229500": ["300m", "300-metres", "sprints", "Men"],
    "10229631": ["400m", "400-metres", "sprints", "Men"],
    
    "10230286": ["50m", "50-metres", "sprints", "Women"],
    "10230288": ["55m", "55-metres", "sprints", "Women"],
    "10229684": ["60m", "60-metres", "sprints", "Women"],
    "10229509": ["100m", "100-metres", "sprints", "Women"],
    "10229510": ["200m", "200-metres", "sprints", "Women"],
    "10229515": ["300m", "300-metres", "sprints", "Women"],
    "10229511": ["400m", "400-metres", "sprints", "Women"],

    "10229604": ["600m", "600-metres", "middlelong", "Men"],
    "10229501": ["800m", "800-metres", "middlelong", "Men"],
    "10229606": ["1000m", "1000-metres", "middlelong", "Men"],
    "10229502": ["1500m", "50-metres", "middlelong", "Men"],
    "10229503": ["Mile", "one-mile", "middlelong", "Men"],
    "10229632": ["2000m", "2000-metres", "middlelong", "Men"],
    "10229607": ["3000m", "3000-metres", "middlelong", "Men"],
    "10229608": ["2 Mile", "two-miles", "middlelong", "Men"],
    "10229609": ["5000m", "5000-metres", "middlelong", "Men"],
    "10229610": ["10000m", "10000-metres", "middlelong", "Men"],
    "10229613": ["2000mSC", "2000-metres-steeplechase", "middlelong", "Men"],
    "10229614": ["3000mSC", "3000-metres-steeplechase", "middlelong", "Men"],

    "10229602": ["600m", "600-metres", "middlelong", "Women"],
    "10229512": ["800m", "800-metres", "middlelong", "Women"],
    "10229516": ["1000m", "1000-metres", "middlelong", "Women"],
    "10229513": ["1500m", "50-metres", "middlelong", "Women"],
    "10229517": ["Mile", "one-mile", "middlelong", "Women"],
    "10229518": ["2000m", "2000-metres", "middlelong", "Women"],
    "10229519": ["3000m", "3000-metres", "middlelong", "Women"],
    "10229520": ["2 Mile", "two-miles", "middlelong", "Women"],
    "10229514": ["5000m", "5000-metres", "middlelong", "Women"],
    "10229521": ["10000m", "10000-metres", "middlelong", "Women"],
    "10229525": ["2000mSC", "2000-metres-steeplechase", "middlelong", "Women"],
    "10229524": ["3000mSC", "3000-metres-steeplechase", "middlelong", "Women"],

    "10230275": ["50mH", "50-metres-hurdles", "hurdles", "Men"],
    "10230289": ["55mH", "55-metres-hurdles", "hurdles", "Men"],
    "10230176": ["60mH", "60-metres-hurdles", "hurdles", "Men"],
    "10229611": ["110mH", "110-metres-hurdles", "hurdles", "Men"],
    "10229612": ["400mH", "400-metres-hurdles", "hurdles", "Men"],

    "10230274": ["50mH", "50-metres-hurdles", "hurdles", "Women"],
    "10230290": ["55mH", "55-metres-hurdles", "hurdles", "Women"],
    "10230177": ["60mH", "60-metres-hurdles", "hurdles", "Women"],
    "10229522": ["110mH", "100-metres-hurdles", "hurdles", "Women"],
    "10229523": ["400mH", "400-metres-hurdles", "hurdles", "Women"],

    "10229615": ["High Jump", "high-jump", "jumps", "Men"],
    "10229616": ["Pole Vault", "pole-vault", "jumps", "Men"],
    "10229617": ["Long Jump", "long-jump", "jumps", "Men"],
    "10229618": ["Triple Jump", "triple-jump", "jumps", "Men"],

    "10229526": ["High Jump", "high-jump", "jumps", "Women"],
    "10229527": ["Pole Vault", "pole-vault", "jumps", "Women"],
    "10229528": ["Long Jump", "long-jump", "jumps", "Women"],
    "10229529": ["Triple Jump", "triple-jump", "jumps", "Women"],

    "10229619": ["Shot Put", "shot-put", "throws", "Men"],
    "10229620": ["Discus", "discus-throw", "throws", "Men"],
    "10229621": ["Hammer", "hammer-throw", "throws", "Men"],
    "10229636": ["Javelin", "javelin-throw", "throws", "Men"],

    "10229530": ["Shot Put", "shot-put", "throws", "Women"],
    "10229531": ["Discus", "discus-throw", "throws", "Women"],
    "10229532": ["Hammer", "hammer-throw", "throws", "Women"],
    "10229533": ["Javelin", "javelin-throw", "throws", "Women"],

    "10229752": ["Mile", "1-mile-road", "road-running", "Men"],
    "204597": ["5k", "5-kilometres", "road-running", "Men"],
    "10229507": ["10k", "10-kilometres", "road-running", "Men"],
    "10229504": ["15k", "15-kilometres", "road-running", "Men"],
    "10229505": ["10 Miles", "10-miles-road", "road-running", "Men"],
    "10229506": ["20k", "20-kilometres", "road-running", "Men"],
    "10229633": ["Half Marathon", "half-marathon", "road-running", "Men"],
    "10229634": ["Marathon", "marathon", "road-running", "Men"],

    "10229753": ["Mile", "1-mile-road", "road-running", "Women"],
    "204598": ["5k", "5-kilometres", "road-running", "Women"],
    "10229537": ["10k", "10-kilometres", "road-running", "Women"],
    "10229538": ["15k", "15-kilometres", "road-running", "Women"],
    "10229539": ["10 Miles", "10-miles-road", "road-running", "Women"],
    "10229540": ["20k", "20-kilometres", "road-running", "Women"],
    "10229541": ["Half Marathon", "half-marathon", "road-running", "Women"],
    "10229534": ["Marathon", "marathon", "road-running", "Women"],

    "10229776": ["3000mRW", "3000-metres-race-walk", "race-walks", "Men"],
    "10229644": ["5000mRW", "5000-metres-race-walk", "race-walks", "Men"],
    "10229637": ["10000mRW", "10000-metres-race-walk", "race-walks", "Men"],
    "10229638": ["20000mRW", "20000-metres-race-walk", "race-walks", "Men"],
    "10229625": ["10kRW", "10-kilometres-race-walk", "race-walks", "Men"],
    "10229508": ["20kRW", "20-kilometres-race-walk", "race-walks", "Men"],
    "10229626": ["30kRW", "30-kilometres-race-walk", "race-walks", "Men"],
    "10229627": ["35kRW", "35-kilometres-race-walk", "race-walks", "Men"],
    "10229628": ["50kRW", "50-kilometres-race-walk", "race-walks", "Men"],

    "10229659": ["3000mRW", "3000-metres-race-walk", "race-walks", "Women"],
    "10229641": ["5000mRW", "5000-metres-race-walk", "race-walks", "Women"],
    "10229639": ["10000mRW", "10000-metres-race-walk", "race-walks", "Women"],
    "10229640": ["20000mRW", "20000-metres-race-walk", "race-walks", "Women"],
    "10229547": ["10kRW", "10-kilometres-race-walk", "race-walks", "Women"],
    "10229535": ["20kRW", "20-kilometres-race-walk", "race-walks", "Women"],
    "10229989": ["35kRW", "35-kilometres-race-walk", "race-walks", "Women"],
    "10229603": ["50kRW", "50-kilometres-race-walk", "race-walks", "Women"],

    "204593": ["4x100m", "4x100-metres-relay", "relays", "Men"],
    "204601": ["4x200m", "4x200-metres-relay", "relays", "Men"],
    "204595": ["4x400m", "4x400-metres-relay", "relays", "Men"],
    "204605": ["4x800m", "4x800-metres-relay", "relays", "Men"],
    "204606": ["4x1500m", "4x1500-metres-relay", "relays", "Men"],

    "204594": ["4x100m", "4x100-metres-relay", "relays", "Women"],
    "204603": ["4x200m", "4x200-metres-relay", "relays", "Women"],
    "204596": ["4x400m", "4x400-metres-relay", "relays", "Women"],
    "204607": ["4x800m", "4x800-metres-relay", "relays", "Women"],
    "204608": ["4x1500m", "4x1500-metres-relay", "relays", "Women"],

    "10230012": ["Shuttle Hurdle", "4x1500-metres-relay", "relays", "Mixed"],
    "10230010": ["2x2400m", "2x2x400-metres-relay", "relays", "Mixed"],
    "10229988": ["4x400m", "4x400-metres-relay", "relays", "Mixed"]
}

# List of field events (non-timed events)
FIELD_EVENTS = [
    "High Jump", "Long Jump", "Triple Jump", "Pole Vault",
    "Shot Put", "Discus", "Hammer", "Javelin", "Weight Throw"
]