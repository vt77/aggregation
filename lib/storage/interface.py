from abc import ABC, abstractmethod

class StorageInterface(ABC):
    """
        Returns domain ID. If domain not exists it will be created 
    """
    @abstractmethod
    def get_domain_id(self,domain : str )  -> int  :
        pass

    """
       Saves clicks by domain ID and timestamp 
    """
    @abstractmethod
    def save_clicks(self, domain_id:int, timestamp: int, clicks: int):
        pass

    """
        Return generator of all clicks for all domains  
    """
    @abstractmethod
    def get_clicks(self):
        pass
