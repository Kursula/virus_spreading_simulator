import numpy as np

class Virus: 
    def __init__(self,
                 name : str, 
                 t_incubation : float,
                 t_contagious : list, 
                 t_heal : float,
                 sneeze_dist : float,
                 sneeze_per_h : float):
        # Identifier for the virus
        self.name = name
        
        # Time from infection to start of the disease
        self.t_incubation = t_incubation 

        # Time range where virus is contagious [start_hour, end_hour]
        self.t_contagious = t_contagious
        
        # Time to heal [hours] calculated from start of infection
        self.t_heal = t_heal 
        
        # Distance [meters] from sneezing person that still infects
        self.sneeze_dist = sneeze_dist
        
        # Sneezing probability density [sneezing count / hour]
        self.sneeze_per_h = sneeze_per_h
        
        
    def get_safe_dist(self) -> float: 
        return self.sneeze_dist
    
    
def spread_virus(virus : any,
                 sneeze_loc : list,
                 sneezing_person : any,
                 event : any, 
                 sim_time : float) -> None: 
    """
    This is run when a sick person sneezes and spreads the virus. 
    Anyone close than the virus sneeze_dist will get infection unless
    they are vaccinated or resistant against the virus. 
    Only the persons in the same event can get the infection. 
    """
    safe_dist = virus.get_safe_dist()
    
    # Calculate distance from sneezing location to every person 
    # in the same event.
    person_locs = []
    names = []
    for name, person in event.persons.items(): 
        person_locs.append(person.get_loc())
        names.append(name)
            
    names = np.array(names)
    person_locs = np.array(person_locs)
    distances = np.linalg.norm(person_locs - np.array(sneeze_loc), axis=1)
    infected = distances < safe_dist
    infected_persons = names[infected]
    for person_name in infected_persons:
        # Infect the person who was too close to sneezing person
        inf_result = event.persons[person_name]\
            .infect(virus=virus, timestamp=sim_time)
        
        # If sneezing caused infection, store the timestamp to the sneezing 
        # person data
        if inf_result: 
            sneezing_person.infected_others(timestamp=sim_time)