from virus import spread_virus


def run_sim(persons : list, 
            events : list,
            t_step : float = 1, 
            sim_hours : float = 1500, 
            plot_map : bool = False, 
           ) -> tuple:
    """
    This function executes the simulation process. 
    """
        
    timesteps = []
    sick_count = []
    sim_time = 0 
    n_person = len(persons)
    while sim_time < sim_hours: 

        # Sick count at each timestemp
        n_sick = 0 

        # Update persons
        for person in persons:
            result = person.update(sim_time=sim_time)
            if result['sneezed']: 
                spread_virus(sneeze_output=result['sneeze_output'],
                             sneeze_loc=result['loc'],
                             event=result['event'],
                             sim_time=sim_time)

            if result['sick']:
                n_sick += 1

        if plot_map:
                render(persons=persons, 
                       events=events, 
                       sim_time=sim_time)

        # Store aggregates for later analysis
        timesteps.append(sim_time)
        sick_count.append(n_sick / n_person)

        # Increment time 
        sim_time += t_step

    return timesteps, sick_count