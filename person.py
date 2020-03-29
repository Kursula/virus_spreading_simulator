import numpy as np
from virus import Virus


class Person: 
    def __init__(self, 
                 name : str,
                 age : float):
        self.name = name
        
        self.state = {
            # General params
            'loc' : [0., 0.],
            'age' : age,
            'sick_leave_allowed' : False,
            'prev_update_time' : 0, 
            'current_event' : None,
            
            # Disease params
            'vaccinated' : False,
            'resistant' : False,
            'virus' : None,
            'incubation' : False,
            'sick' : False,
            'sick_start_time' : None,
            'contagious' : False,
            'sneeze_per_h' : 0,
            'sneezed' : False, 
            'infected_others_ts' : [],
        }
                
        # Calendar events
        self.schedule = {}
        
        
    def add_event(self, 
                  event_hours : list,
                  event : any) -> None: 
        """
        Add new event to the person's calendar. 
        Event are set for full calendar hours. 
        """
        for hour in event_hours:
            self.schedule[int(hour)] = event

            
    def set_loc(self, loc : list) -> None:
        """
        Set location coordinates
        """
        self.state['loc'] = loc 
        
    
    def get_loc(self) -> list:
        return self.state['loc']
    
    
    def get_color(self) -> str: 
        """
        Marker color for map rendering.
        """
        if self.state['contagious']:
            color = 'red'
        elif self.state['sick'] or self.state['incubation']:
            color = 'gold'
        else:
            color = 'green'
        return color
    
    
    def get_radius(self) -> float:
        """
        Marker radius for map rendering.
        """
        if self.state['sneezed']: 
            return 50
        else:
            return 10

        
    def enable_sick_leave(self) -> None: 
        """
        Enable the person to stay at home when sick
        """
        self.state['sick_leave_allowed'] = True
        
    
    def vaccinate(self) -> None: 
        """
        Make the person immune against the virus
        """
        self.state['vaccinated'] = True
        
        
    def get_vaccination_status(self) -> list:
        """
        Returns vaccination status
        """
        return self.state['vaccinated']
        
        
    def infected_others(self, 
                        timestamp : float) -> None: 
        """
        Store timestamp when this person infected someone else. 
        """
        self.state['infected_others_ts'].append(timestamp)
        
        
    def infect(self, 
               virus : Virus, 
               timestamp : float) -> bool:
        """
        Infect the person with the virus. 
        Returns True when the person gets the infection. 
        """
        # Check if person is vaccinated
        if self.state['vaccinated']:
            return False
        
        # Check if person is resistant due to immunity obtained 
        # from earlier disease
        if self.state['resistant']:
            return False
        
        # Check if the person is already sick
        if self.state['sick'] or self.state['incubation']:
            return False
        
        # Make the person sick
        self.state['incubation'] = True
        self.state['virus'] = virus
        self.state['sick_start_time'] = timestamp
        return True
    
    
    def initial_setup(self):
        # Set the initial event at beginning of simulation
        new_event = self.schedule[0]            
        self.state['current_event'] = new_event        
        self.state['current_event'].get_in(self)      

                
    def update(self, 
               sim_time : float) -> dict: 
        """
        Update the person status, location, infection state machine, etc. 
        """
        self.state['sneezed'] = False
        
        # Go to the event listed in schedule
        sch_idx = int(sim_time % 24)
        new_event = self.schedule[sch_idx]                
        if new_event != self.state['current_event']:
            if self.state['sick']:
                if self.state['sick_leave_allowed']:
                    if self.state['current_event'].event_type == 'HOME':
                        # Do nothing and stay at home.
                        pass
                    else: # Do the scheduled events until the person ends up home
                        self.state['current_event'].get_out(self)
                        self.state['current_event'] = new_event   
                        self.state['current_event'].get_in(self)   
                else: # No sick leaves. Go to all planned events.
                    self.state['current_event'].get_out(self)
                    self.state['current_event'] = new_event   
                    self.state['current_event'].get_in(self)   
            else: # Not sick. Go to all planned events.
                self.state['current_event'].get_out(self)
                self.state['current_event'] = new_event   
                self.state['current_event'].get_in(self)   

        # Update disease state machine and clear some previous 
        # state values
        if self.state['sick'] or self.state['incubation']:
            disease_duration = sim_time - self.state['sick_start_time']  
            
            # Check if disease has passed the incubation period
            if disease_duration > self.state['virus'].t_incubation: 
                self.state['sick'] = True
                self.state['incubation'] = False
            
            # Check if virus is contagious
            t_cont = self.state['virus'].t_contagious
            if t_cont[0] <= disease_duration < t_cont[1]:
                self.state['contagious'] = True
                self.state['sneeze_per_h'] = self.state['virus'].sneeze_per_h
            else:
                self.state['contagious'] = False
                self.state['sneeze_per_h'] = 0 
                
            # Check if the person has healed from the disease
            if disease_duration >= self.state['virus'].t_heal: 
                self.state['sick'] = False 
                self.state['resistant'] = True 

        results = {
            'sick' : self.state['sick'],
            'sneezed' : False,
            'virus' : None,
            'event' : self.state['current_event'],
            'loc' : self.state['loc']
        }
        
        # Check if there is need to sneeze 
        if self.state['contagious']:
            t_delta = sim_time - self.state['prev_update_time']
            p_sneeze = t_delta * self.state['sneeze_per_h']
            if np.random.rand() < p_sneeze: 
                results['sneezed'] = True
                results['virus'] = self.state['virus']
                self.state['sneezed'] = True
        
        # Store the update timestamp
        self.state['prev_update_time'] = sim_time
        
        return results