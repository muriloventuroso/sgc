import os
import re


def get_mongo_url():
    if 'MONGODB_URI' in os.environ:
        url = os.environ['MONGODB_URI']
        m = re.match(r"^mongodb:\/\/(?:(?:(\w+)?:(\w+)?@)|:?@?)((?:[\w.-])+)(?::(\d+))?(?:\/([\w-]+))?(?:\?([\w-]+=[\w-]+(?:&[\w-]+=[\w-]+)*)?)?$", url)
        if m:
            return {'USERNAME': m.group(1), 'PASSWORD': m.group(2), 'HOST': m.group(3), 'PORT': int(m.group(4)), 'NAME': m.group(5)}
    return {}
