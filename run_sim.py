from virus import Virus, spread_virus
import numpy as np
import sys
import time

def run_simulation(scenario : dict) -> dict:
    """
    This function executes the simulation process. 
    """        
    t0 = time.time()
    persons = scenario['persons']
    events = scenario['events']
    virus = scenario['virus']
    sim_hours = scenario['sim_hours']
    timesteps = []
    sick_ratios = []
    n_person = len(persons)

    # Find the max timestemp that can be used without compromising results
    temp = [ev.loc_shuffle_interval for ev in events]
    t_step = min(temp)
    # Person calendar events require min 1h stepping 
    if t_step > 1: 
        t_step = 1
    # Check if virus params limit the timestep since
    # there can be max one sneeze during the t_step interval.
    if t_step > 1 / virus.sneeze_per_h:
        t_step = 1 / virus.sneeze_per_h
                
    # Initial setup
    for person in persons: 
        person.initial_setup()
            
    # Run simulation 
    sim_time = 0 
    while sim_time < sim_hours:

        # Initialize result params for each timestep
        n_sick = 0 

        # Run any updates in the event (home, work, etc) states, such 
        # as shuffle the person locations. 
        for ev in events: 
            ev.update(sim_time=sim_time)
        
        # Update persons
        for prs in persons:
            # Update status and spread virus
            result = prs.update(sim_time=sim_time)
            if result['sneezed']: 
                spread_virus(virus=result['virus'],
                             sneeze_loc=result['loc'],
                             sneezing_person=prs,
                             event=result['event'],
                             sim_time=sim_time)

            # Process and store data for result analysis
            if result['sick']:
                n_sick += 1
                
        """
        # Plot map layout and persons 
        if render_function is not None:
            render_function(
                persons=persons, 
                events=events, 
                sim_time=sim_time
            )
        """

        # Store aggregates for later analysis
        timesteps.append(sim_time)
        sick_ratios.append(n_sick / n_person)

        # Increment time 
        sim_time += t_step
        
    # Progress monitoring 
    t1 = time.time()
    print('Scenario {} done in {:0.1f} s.'.format(scenario['label'], t1 - t0))
        
    # Add results to the simulation scenario
    scenario['timesteps'] = timesteps
    scenario['sick_ratios'] = sick_ratios
        
    return scenario


