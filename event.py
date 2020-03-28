import numpy as np


class AbstractEvent: 
    """
    Base class for all event and location types like homes and schools. 
    
    The most critical parameter to set is the size, which defines the event place 
    dimensions in meters. The persons within the event will be randomly located
    inside that space. 
    
    The parameter loc_shuffle_interval [hours] tells that how often the persons in this 
    event will change their locations. 
    
    Location parameters are only used when rendering the simulation scenario. From 
    the simulation functionality point of view those play no role. 
    """
    def __init__(self):
        self.name = None
        self.event_type = None
        self.loc = None
        self.size = None
        self.persons = {}
        self.loc_shuffle_interval = 0
        self.prev_loc_shuffle_ts = 0

        
    def get_in(self, person) -> None:
        """
        Get person in to this event.
        """
        self.persons[person.name] = person
        
        # Set location within the event space
        x = self.loc[0] + np.random.rand() * self.size[0]
        y = self.loc[1] + np.random.rand() * self.size[1]
        person.set_loc([x, y])
        
    
    def get_out(self, person):
        """
        Get person out of this event.
        """
        self.persons.pop(person.name)

        
    def shuffle_locs(self) -> None:
        """
        Shuffle the person locations within the event. Shuffling will 
        increase the social contacts and increases virus spreading. 
        """
        for person in self.persons.values(): 
            # Set new location within the event space
            x = self.loc[0] + np.random.rand() * self.size[0]
            y = self.loc[1] + np.random.rand() * self.size[1]
            person.set_loc([x, y])
                                
        
    def get_loc(self) -> list: 
        """
        Returns event location for visualisation etc. purposes. 
        """
        return self.loc 
    
    
    def get_size(self) -> list:
        """
        Returns event (building) size in meters.
        """
        return self.size
        
        
    def update(self, sim_time) -> None: 
        """
        Run any updates in the event state.
        """
        # Shuffle person locations withing the place/building
        if sim_time >= self.prev_loc_shuffle_ts + self.loc_shuffle_interval:
            self.shuffle_locs()
            self.prev_loc_shuffle_ts = sim_time
            

class Home(AbstractEvent):
    def __init__(self,                  
                 name : str, 
                 size : list, 
                 loc : list = [0, 0], 
                 loc_shuffle_interval : float = 3.0): 
        super().__init__()
        self.loc_shuffle_interval = loc_shuffle_interval
        self.event_type = 'HOME'
        self.name = name
        self.loc = loc
        self.size = size

        
class Work(AbstractEvent):
    def __init__(self,                  
                 name : str, 
                 size : list, 
                 loc : list = [0, 0], 
                 loc_shuffle_interval : float = 3.0): 
        super().__init__()
        self.loc_shuffle_interval = loc_shuffle_interval
        self.event_type = 'WORK'
        self.name = name
        self.loc = loc
        self.size = size


class School(AbstractEvent):
    def __init__(self,                  
                 name : str, 
                 size : list, 
                 loc : list = [0, 0], 
                 loc_shuffle_interval : float = 1.0): 
        super().__init__()
        self.loc_shuffle_interval = loc_shuffle_interval
        self.event_type = 'SCHOOL'
        self.name = name
        self.loc = loc
        self.size = size
        

class Shop(AbstractEvent):
    def __init__(self,                  
                 name : str, 
                 size : list, 
                 loc : list = [0, 0], 
                 loc_shuffle_interval : float = 0.5): 
        super().__init__()
        self.loc_shuffle_interval = loc_shuffle_interval
        self.event_type = 'SHOP'
        self.name = name
        self.loc = loc
        self.size = size