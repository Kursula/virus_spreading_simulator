import numpy as np

class AbstractEvent: 
    def __init__(self):
        self.name = None
        self.event_type = None
        self.loc = None
        self.size = None
        self.persons = {}

        
    def get_in(self, person):
        self.persons[person.name] = person
        
        #print(person.name, self.name,  ' in')
        
        # Set location within the event space
        x = self.loc[0] + np.random.rand() * self.size[0]
        y = self.loc[1] + np.random.rand() * self.size[1]
        person.set_loc([x, y])
        
        
    def get_out(self, person):
        self.persons.pop(person.name)
        #print(person.name, self.name,  ' out')

        
    def get_loc(self) -> list: 
        return self.loc 
    
    
    def get_size(self) -> list:
        return self.size
        
        
    def update(self, timestep): 
        pass
    

class Home(AbstractEvent):
    def __init__(self,                  
                 name : str, 
                 loc : list, 
                 size : list): 
        super().__init__()
        
        self.event_type = 'HOME'
        self.name = name
        self.loc = loc
        self.size = size

        
class Work(AbstractEvent):
    def __init__(self,                  
                 name : str, 
                 loc : list, 
                 size : list): 
        super().__init__()
        
        self.event_type = 'WORK'
        self.name = name
        self.loc = loc
        self.size = size


        