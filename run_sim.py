from virus import Virus, spread_virus


def run_sim(persons : list, 
            events : list,
            virus : Virus,
            sim_hours : float, 
            render_function : any = None, 
           ) -> tuple:
    """
    This function executes the simulation process. 
    """        
    timesteps = []
    sick_count = []
    n_person = len(persons)

    # Find the max timestemp that can be used without compromising results
    temp = [ev.loc_shuffle_interval for ev in events]
    t_step = min(temp)
    # Person calendar events require min 1h stepping 
    if t_step > 1: 
        t_step = 1
    # Check if virus params limit the timestep. 
    # There can be max 1 sneeze during the t_step interval.
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
        for event in events: 
            event.update(sim_time=sim_time)
        
        # Update persons
        for person in persons:
            # Update status and spread virus
            result = person.update(sim_time=sim_time)
            if result['sneezed']: 
                spread_virus(virus=result['virus'],
                             sneeze_loc=result['loc'],
                             sneezing_person=person,
                             event=result['event'],
                             sim_time=sim_time)

            # Process and store data for result analysis
            if result['sick']:
                n_sick += 1
                
        # Plot map layout and persons 
        if render_function is not None:
            render_function(
                persons=persons, 
                events=events, 
                sim_time=sim_time
            )

        # Store aggregates for later analysis
        timesteps.append(sim_time)
        sick_count.append(n_sick / n_person)

        # Increment time 
        sim_time += t_step

    return timesteps, sick_count


