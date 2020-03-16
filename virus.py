import numpy as np

class Virus: 
    def __init__(self,
                 name : str, 
                 t_contagious : list, 
                 t_heal : float,
                 sneeze_dist : float,
                 sneeze_per_h : float):
        # Identifier for the virus
        self.name = name
        
        # Time range where virus is contagious [start_hour, end_hour]
        self.t_contagious = t_contagious
        
        # Time to heal [hours] calculated from start of infection
        self.t_heal = t_heal 
        
        # Distance from sneezing person that still infects
        self.sneeze_dist = sneeze_dist
        
        # Sneezing probability density [sneezing count / hour]
        self.sneeze_per_h = sneeze_per_h
        
        
    def get_safe_dist(self) -> float: 
        return self.sneeze_dist
    
    
def spread_virus(sneeze_output : list,
                 sneeze_loc : list,
                 event : any, 
                 sim_time : float) -> None: 
    
    for virus in sneeze_output: 
        safe_dist = virus.get_safe_dist()
        
        person_locs = []
        names = []
        for name, person in event.persons.items(): 
            person_locs.append(person.get_loc())
            names.append(name)
            
        names = np.array(names)
        person_locs = np.array(person_locs)
        distances = np.linalg.norm(person_locs - np.array(sneeze_loc), axis=1)
        infected = distances <= safe_dist
        
        for idx, inf in enumerate(infected):
            if inf: 
                event.persons[names[idx]].infect(virus=virus, 
                                                 timestamp=sim_time)