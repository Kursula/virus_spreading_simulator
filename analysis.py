import numpy as np
import time


class Analysis:
    
    def __init__(self):
        pass
    
    
    def run_analysis(self, scenario : dict) -> dict:
        self.process_ongoing_cases(scenario)
        self.average_r_value(scenario)
        self.total_sick_ratio(scenario)
        self.cumulative_infected_ratio(scenario)
        return scenario
        
        
    def process_ongoing_cases(self, scenario : dict) -> None: 
        for person in scenario['persons'].values():
            if not person.has_been_sick:
                continue
            if person.sick_end_time is None: 
                person.sick_end_time = np.inf

    
    def average_r_value(self, scenario : dict, min_case_count : int = 10) -> None:
        """
        Calculate average R value, i.e. the number of persons infected by a sick person. 
        The value is shown in the results for the duration of the person's sickness. 
        """
        
        # List of zeros for the results
        r_values = [[] for _ in scenario['timesteps']]

        # Calculate number of sick persons at each timestep
        for person in scenario['persons'].values():
            if not person.has_been_sick:
                continue
            inf_count = len(person.infected_others)
            for idx, ts in enumerate(scenario['timesteps']):
                if (person.sick_start_time <= ts) and (ts < person.sick_end_time):
                    r_values[idx].append(inf_count)

        scenario['r_value'] = []
        for r_list in r_values: 
            if len(r_list) < min_case_count: 
                r = 0 
            else: 
                r = np.mean(r_list)
            scenario['r_value'].append(r)
    
    
    def total_sick_ratio(self, scenario : dict) -> None:
        """
        Calculate ratio of population that is sick.
        """
        # List of zeros for the results
        total_sick = [0 for _ in scenario['timesteps']]
        
        # Calculate number of sick persons at each timestep
        for person in scenario['persons'].values():
            if person.has_been_sick:
                for idx, ts in enumerate(scenario['timesteps']):
                    if (person.sick_start_time <= ts) and (ts < person.sick_end_time):
                        total_sick[idx] += 1
        
        # Scale results to [0, 1] range
        n_person = len(scenario['persons'])
        scenario['sick_ratio'] = [x / n_person for x in total_sick]
            
    
    def cumulative_infected_ratio(self, scenario : dict) -> None: 
        """
        Calculates cumulative ratio of population that has had the infection.
        """
        # List of zeros for the results
        cumul_infected = [0 for _ in scenario['timesteps']]
        
        # Calculate cumulative number of sick persons at each timestep
        for person in scenario['persons'].values():
            if person.has_been_sick:
                for idx, ts in enumerate(scenario['timesteps']):
                    if (person.sick_start_time <= ts):
                        cumul_infected[idx] += 1
        
        # Scale results to [0, 1] range
        n_person = len(scenario['persons'])
        scenario['cumul_inf_ratio'] = [x / n_person for x in cumul_infected]

