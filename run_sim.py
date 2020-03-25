from virus import spread_virus

def run_sim(persons : list, 
            events : list,
            t_step : float = 1, 
            sim_hours : float = 1500, 
            render_function : any = None, 
           ) -> tuple:
    """
    This function executes the simulation process. 
    """
        
    timesteps = []
    sick_count = []
    
    sim_time = 0 
    n_person = len(persons)
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
                spread_virus(sneeze_output=result['sneeze_output'],
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


