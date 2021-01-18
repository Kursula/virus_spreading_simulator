from virus import Virus
from person import Person
import numpy as np
import time
from analysis import Analysis


def run_simulation(scenario : dict, t_step : float = 1) -> dict:
    """
    Runs the simulation process. 
    """        
    t0 = time.time()
    
    # Initial setup
    scenario['timesteps'] = []
    scenario['debug'] = []
    n_all = len(scenario['persons'])

    # Divide persons to compartments
    healthy = {}
    sick = {}
    healed = {}
    for id_code, person in scenario['persons'].items(): 
        if person.sick_now:
            sick[id_code] = person
        elif person.healed:
            healed[id_code] = person
        else:
            healthy[id_code] = person

    # Initialize callback status
    for cb in scenario['callbacks']: 
        cb['done'] = False

    # Run simulation 
    sim_time = 0
    healthy_idx = 0
    while sim_time < scenario['sim_hours']:
        n_healthy = len(healthy)
        healthy_list = list(healthy.values())
    
        # Update persons
        to_healed = []
        to_sick = []
        for id_code, person in sick.items():
            person.update_infection(sim_time)            
            if person.healed: 
                to_healed.append(id_code)
                continue 
                
            if person.expose_others:
                if n_healthy == 0: 
                    continue

                # Calculate number of healthy persons to expose
                n = person.n_exposed
                n *= float(n_healthy) / float(n_all)
                frac = n - int(n)
                n = int(n)
                if np.random.rand() < frac: 
                    n += 1
                    
                # Expose persons
                for _ in range(n): 
                    healthy_idx += 1
                    if healthy_idx >= n_healthy: 
                        healthy_idx = 0
                    exp_person = healthy_list[healthy_idx]    
                    new_infection = exp_person.expose(
                        infected_by=person.id_code, 
                        virus=scenario['virus'], 
                        timestamp=sim_time
                    )
                    # If exposure caused infection, store the contact information
                    if new_infection: 
                        person.report_infected_others(id_code=exp_person.id_code)
                        to_sick.append(exp_person.id_code)
                
        for id_code in to_healed: 
            healed[id_code] = sick.pop(id_code)
                
        for id_code in to_sick: 
            sick[id_code] = healthy.pop(id_code)
        
        scenario['timesteps'].append(sim_time)
        sim_time += t_step
        
        # Run timed callbacks
        for cb in scenario['callbacks']: 
            if (cb['trigger'] < sim_time) and (cb['done'] == False): 
                cb['function'](scenario)
                cb['done'] = True
        
    # Analyze the data
    analysis = Analysis()
    scenario = analysis.run_analysis(scenario)
        
    # Progress monitoring 
    t1 = time.time()
    print('Scenario {} done in {:0.1f} s.'.format(scenario['label'], t1 - t0))

    return scenario