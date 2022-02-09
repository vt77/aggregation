
from storage.interface import StorageInterface

class DomainProcessor():

    def __init__(self,storage : StorageInterface):
        self.storage = storage
        
    def add(self, timestamp:int, domain:str, clicks: int ) -> None:
        domain_id = self.storage.get_domain_id(domain)
        self.storage.save_clicks( domain_id, timestamp, clicks )

    def get(self,period):
        return self.storage.get_clicks(period)
