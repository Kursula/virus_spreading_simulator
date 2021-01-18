import numpy as np


class Virus: 
    def __init__(self,
                 name : str, 
                 t_heal : float,
                 spreading_t_start : float,
                 spreading_coefficient : float, 
                 infection_coefficient : float):
        
        # Identifier for the virus
        self.name = name
        
        # Time to heal [hours] calculated from start of infection.
        self.t_heal = t_heal 

        # Time to start spreading virus. It ends when person is healed.
        self.spreading_t_start = spreading_t_start
            
        # Spreading coefficient. Values from 0 to 1. 0 means no sprearing, 1 means max spreading.
        self.spreading_coefficient = spreading_coefficient
        
        # Infection coefficient, i.e. how easily the person receiving the
        # virus will get infection. 0 means no infection, 1 means certain infection.
        self.infection_coefficient = infection_coefficient

        # Create look-up table for spreading probability vs time.
        self.create_spreading_prob_lut()
        
        
    def create_spreading_prob_lut(self) -> None: 
        self.probs = {}
        for t in range(self.t_heal):
            if t < self.spreading_t_start:
                self.probs[t] = 0
            else:
                self.probs[t] = self.spreading_coefficient
        
            
    def get_spreading_probability(self, disease_duration : float) -> float: 
        return self.probs[int(disease_duration)]
