from abc import ABC, abstractmethod


class DbInterface(ABC): 
    
    @abstractmethod
    def connect(self):
        pass
