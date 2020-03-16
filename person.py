import numpy as np
from virus import Virus


class Person: 
    def __init__(self, 
                 name : str,
                 age : float):
        self.name = name
        
        self.state = {
            'loc' : [0., 0.],
            'age' : age,
            'vaccinated' : [],
            'sick_stay_home' : False,
            'alive' : True,
            'sick' : False,
            'prev_update_time' : 0, 
            'current_event' : None,
            'sneeze_per_h' : 0,
            'sneezed' : False
        }
        
        # Disease states and history
        self.virus_status = {}
        
        # Life events
        self.schedule = {}
        
        
    def add_event(self, 
                  event_hours : list,
                  event : any) -> None: 
        """
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
        color = 'green'
        for virus in self.virus_status.values():
            if virus['contagious']:
                return 'red'
            if virus['infected']:
                color = 'gold'
        return color
    
    
    def get_radius(self) -> float:
        if self.state['sneezed']: 
            return 50
        else:
            return 10

    def enable_sick_leave(self) -> None: 
        self.state['sick_stay_home'] = True
        
    
    def vaccinate(self, virus_name : str) -> None: 
        self.state['vaccinated'].append(virus_name)
        
        
    def get_vaccination_status(self) -> list:
        return self.state['vaccinated']
        
        
    def infect(self, 
               virus : Virus, 
               timestamp : float) -> None:
        
        # Check if person is vaccinated against this virus
        if virus.name in self.state['vaccinated']:
            return None
        
        # Check if this is new infection 
        if virus.name not in self.virus_status.keys():
            self.virus_status[virus.name] = {
                'virus' : virus,
                'infected' : True, 
                'contagious' : False,
                'resistant' : False,
                'healed' : False,
                'start_time' : timestamp
            }
        
        # Check if the person is resistant to this virus
        elif self.virus_status[virus.name]['resistant'] == True: 
            return 
        
        
    def sneeze(self): 
        output = []
        self.state['sneezed'] = True
        for virus in self.virus_status.values():
            if virus['contagious']: 
                output.append(virus['virus'])    
        return output
    
                
    def update(self, 
               sim_time : float) -> dict: 
        
        results = {
            'sick' : False,
            'sneezed' : False,
            'sneeze_output' : None
        }
        self.state['sneezed'] = False
        
        # Go to the event listed in schedule
        sch_idx = int(sim_time % 24)
        new_event = self.schedule[sch_idx]
        if new_event != self.state['current_event']:
            
            # Check if should stay home when sick
            if self.state['sick']\
                and self.state['sick_stay_home']\
                and self.state['current_event'].event_type == 'HOME':
                pass
            else:
                # Get out of the previous event
                if self.state['current_event'] is not None: 
                    self.state['current_event'].get_out(self)

                # Get in to the new event
                new_event.get_in(self)
                self.state['current_event'] = new_event
            
        results['event'] = self.state['current_event']
        results['loc'] = self.state['loc']
        
        # Update infection state machine
        self.state['sneeze_per_h'] = 0
        self.state['sick'] = False 
        for virus in self.virus_status.values():
            # Check sickness status
            if virus['infected']: 
                results['sick'] = True
                self.state['sick'] = True 
            else: 
                continue
                
            inf_time = sim_time - virus['start_time']        
            # Check if virus is contagious
            t_cont = virus['virus'].t_contagious
            if t_cont[0] <= inf_time < t_cont[1]:
                virus['contagious'] = True
                self.state['sneeze_per_h'] = max(self.state['sneeze_per_h'], 
                                                 virus['virus'].sneeze_per_h)
            else:
                virus['contagious'] = False
                
            # Check if the person has already healed
            if inf_time >= virus['virus'].t_heal: 
                virus['infected'] = False 
                virus['resistant'] = True 
        
            # Check if virus is lethal 
            # TODO 
        
        # Check if there is need to sneeze 
        t_delta = sim_time - self.state['prev_update_time']
        p_sneeze = t_delta * self.state['sneeze_per_h']
        if np.random.rand() < p_sneeze: 
            sneeze_output = self.sneeze()
            results['sneezed'] = True
            results['sneeze_output'] = sneeze_output

        # Store the update timestamp
        self.state['prev_update_time'] = sim_time
        
        return results