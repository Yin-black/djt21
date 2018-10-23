import memcache

mc = memcache.Client(['127.0.0.1:11211'])

def set_key(key=None,value=None,time = 60*5):
    if key and value:
        mc.set(key,value,time =time)
        return True
    return False

def get_key(key=None):
    if key:
        return mc.get(key)
    return None

def del_key(key=None):
    if key:
        mc.delete(key)
        return True
    return False