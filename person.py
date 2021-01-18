import numpy as np
from virus import Virus


class Person: 
    def __init__(self, 
                 id_code : int,
                 contacts_in_quarantine : float = 0, 
                 contacts_in_normal_life : float = 4, 
                 contacts_in_lockdown : float = 1, 
                 quarantine_when_sick : bool = False, 
                 immune : bool = False, 
                 masked : bool = False, 
                 mask : any = None):
        
        self.id_code = id_code
        self.contacts_in_quarantine = contacts_in_quarantine
        self.contacts_in_normal_life = contacts_in_normal_life 
        self.contacts_in_lockdown = contacts_in_lockdown
        self.quarantine_when_sick = quarantine_when_sick
        self.immune = immune
        self.masked = masked
        self.mask = mask
        
        self.lockdown = False
        self.virus = None
        self.sick_now = False
        self.sick_start_time = None
        self.sick_end_time = None
        self.healed = False
        self.has_been_sick = False
        self.expose_others = False
        self.n_exposed = 0
        self.infected_by = None
        self.infected_others = []
        
        
    def expose(self, 
               infected_by : int, 
               virus : Virus, 
               timestamp : float) -> bool:
        """
        Infect the person with the virus. 
        Returns True when the person gets the infection. 
        """
        # Check if person is immune due to or sick now
        if self.immune or self.sick_now:
            return False

        # Check if the person is lucky and does not get the infection
        inf_prob = virus.infection_coefficient
        if self.masked: 
            inf_prob = self.mask.filter_inhale(inf_prob)
        if np.random.rand() > inf_prob:
            return False
        
        self.infect(infected_by, virus, timestamp)
        return True
    
        
    def infect(self, 
               infected_by : int, 
               virus : Virus, 
               timestamp : float):
        """
        Infect the person with the virus. 
        Returns True when the person gets the infection. 
        """
        # Make the person sick
        self.sick_now = True
        self.virus = virus
        self.sick_start_time = timestamp
        self.infected_by = infected_by
        self.has_been_sick = True

    
    def report_infected_others(self, id_code : int) -> None: 
        # Store name of the person who got infection from this. 
        self.infected_others.append(id_code)
                
                
    def update_infection(self, sim_time : float) -> dict: 
        """
        Update the infection state machine, etc. 
        """
        # Update disease state machine and clear some previous state values

        # Check if the person has healed from the disease
        disease_duration = sim_time - self.sick_start_time
        if disease_duration >= self.virus.t_heal: 
            self.healed = True
            self.sick_now = False 
            self.virus = None
            self.immune = True 
            self.sick_end_time = sim_time
            self.expose_others = False
            return

        # Spread the virus
        spreading_prob = self.virus.get_spreading_probability(disease_duration)
        if self.masked: 
            spreading_prob = self.mask.filter_exhale(spreading_prob)
        if np.random.rand() < spreading_prob:
            self.expose_others = True
            if self.quarantine_when_sick:
                self.n_exposed = np.random.rand() * self.contacts_in_quarantine
            elif self.lockdown:
                self.n_exposed = np.random.rand() * self.contacts_in_lockdown
            else:
                self.n_exposed = np.random.rand() * self.contacts_in_normal_life
        else:
            self.expose_others = False