from datetime import datetime

UTC_FMT = '%Y-%m-%dT%H:%M:%SZ'

def str2datetime(s):
    return datetime.strptime(s, UTC_FMT)
