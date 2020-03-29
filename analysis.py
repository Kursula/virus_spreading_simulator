import numpy as np


def cumul_inf_ratio(scenario : dict) -> dict: 
    """
    Calculates cumulative ratio of persons infected and adds it to 
    the scenario dictionary. 
    """
    ts_to_idx =  {ts : idx for idx, ts in enumerate(scenario['timesteps'])}    
    cuminf = np.zeros(len(scenario['timesteps']))
    for person in scenario['persons']:
        for timestamp in person.state['infected_others_ts']:
            cuminf[ts_to_idx[timestamp]] += 1

    cuminf = np.cumsum(np.array(cuminf))
    cuminf = cuminf / float(len(scenario['persons']))
    scenario['cumul_inf_ratios'] = cuminf
    return scenario
        