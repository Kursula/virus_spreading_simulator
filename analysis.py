import numpy as np


def cumul_inf_ratio(persons : list, 
                    timestamps : list) -> np.ndarray: 
    """
    Calculates cumulative ratio of persons infected.     
    """
    ts_to_idx =  {ts : idx for idx, ts in enumerate(timestamps)}    
    cuminf = np.zeros(len(timestamps))
    for person in persons:
        for timestamp in person.state['infected_others_ts']:
            cuminf[ts_to_idx[timestamp]] += 1

    cuminf = np.cumsum(np.array(cuminf))
    cuminf = cuminf / float(len(persons))
    return cuminf
        