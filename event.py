import numpy as np

class AbstractEvent: 
    def __init__(self):
        self.name = None
        self.event_type = None
        self.loc = None
        self.size = None
        self.persons = {}
        self.loc_shuffle_interval = 0
        self.prev_loc_shuffle_ts = 0

        
    def get_in(self, person) -> None:
        self.persons[person.name] = person
        
        # Set location within the event space
        x = self.loc[0] + np.random.rand() * self.size[0]
        y = self.loc[1] + np.random.rand() * self.size[1]
        person.set_loc([x, y])
        
    
    def shuffle_locs(self) -> None:
        for person in self.persons.values(): 
            # Set new location within the event space
            x = self.loc[0] + np.random.rand() * self.size[0]
            y = self.loc[1] + np.random.rand() * self.size[1]
            person.set_loc([x, y])
        
        
    def get_out(self, person):
        self.persons.pop(person.name)
        
        
    def get_loc(self) -> list: 
        return self.loc 
    
    
    def get_size(self) -> list:
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
                 loc : list, 
                 size : list, 
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
                 loc : list, 
                 size : list, 
                 loc_shuffle_interval : float = 3.0): 
        super().__init__()
        self.loc_shuffle_interval = loc_shuffle_interval
        self.event_type = 'WORK'
        self.name = name
        self.loc = loc
        self.size = size


        