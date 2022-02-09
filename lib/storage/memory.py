"""
    Memory storage just a simple in-memory storage.
    It may be not too effective in huge number of entries
"""
from .interface import StorageInterface 
from cachetools import TTLCache,cached


import logging
logger = logging.getLogger(__name__)


class CacheSizeUnlimited:
    def __init__(self,name):
        self.name = name

    def __lt__(self,n):
            logger.debug("[STORAGE][%s]Request cache size : %d" % (self.name,n))
            return 0

#Store cache for hour and 10 seconds
click_cache = TTLCache(maxsize=CacheSizeUnlimited('CLICK'),ttl=3610)
domain_cache = TTLCache(maxsize=CacheSizeUnlimited('DOMAIN'),ttl=3610)

def get_domain_by_id(domain_id:int):
     result = next((k for k in domain_cache if domain_cache[k] == domain_id), None)
     if result is None:
         return None
     return result[1]


class MemoryStorage(StorageInterface):

    #Domain id sequental
    last_domain_id = 0


    @cached(cache=domain_cache)
    def get_domain_id(self,domain : str)  -> int  :
            self.last_domain_id = self.last_domain_id + 1
            logger.debug("[STORAGE] Create id for domain %s : %d" % (domain,self.last_domain_id))
            return self.last_domain_id

    def save_clicks(self, domain_id:int, timestamp: int, clicks: int):
        logger.debug("[STORAGE][%d]Save clicks for %d -  %d " % (timestamp, domain_id,clicks))
        data = click_cache.get(domain_id,[])
        data.append( (timestamp,clicks) )
        click_cache[domain_id] = data

    def get_clicks(self,period):
        for d in click_cache.keys():
            domain = get_domain_by_id(d)
            logger.debug("[STORAGE] Get clicks for domain %s" % domain )
            for c in click_cache[d]:
                yield (domain,c)
