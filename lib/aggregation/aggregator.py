
from serilizer.json import JSONSerilizable
import heapq

from datetime import datetime
import time

import logging
logger = logging.getLogger(__name__)

class DomainAggregator(JSONSerilizable):

    next_rebuild = None
    top_data = {}

    def __init__(self,count:int,period:int):
        logger.debug("[AGGREGATOR]Create count %d, period %d" % (count,period))
        self.period = period
        self.count = count
        # In this case rebuild will be done on next period.
        # Not too good for hourly stats
        # And stats still may be partial on start
        self.next_rebuild = self.frame_start() + period
        logger.debug("[AGGREGATOR]Next rebuild %s" % (datetime.utcfromtimestamp(self.next_rebuild).strftime('%H:%M')))

    def frame_start(self):
        return int( int(time.time()) / self.period ) * self.period

    def want_rebuild(self) -> bool :
        return self.next_rebuild <= self.frame_start()

    def rebuild(self,domains):
        frame_end = self.frame_start() 
        frame_start = frame_end - self.period
        counters = {}
        for domain_name,data in domains:
            (date_stamp,clicks) = data
            if date_stamp > frame_start and date_stamp < frame_end:
                   count =  counters.get(domain_name,0)
                   counters[domain_name] = count + clicks
        self.top_data = { p:counters[p] for p in heapq.nlargest(self.count,counters,key=lambda x : counters.get(x) ) } 
        self.next_rebuild  = frame_end + self.period
        
    """
        Handle JSONSerilizable to make it flask serilizable
    """
    def toJSON(self):
        #TODO: Not implemented
        return  {}

    """
        Handle dict() used in Response
    """
    def __iter__(self):
        yield 'domains',self.top_data
