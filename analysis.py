import numpy as np


def cumul_inf_ratio(persons : list, 
                    timestamps : list) -> np.ndarray: 
    """
    Results analysis. 
    Calculates cumulative ratios of persons infected. 
    
    Currently this cuts corners and assumes that there is only one 
    virus existing. 
    """
    
    ts_to_idx =  {ts : idx for idx, ts in enumerate(timestamps)}    
    cuminf = [0 for x in range(len(timestamps))]
    for person in persons:
        for vir_data in person.virus_status.values():
            for timestamp in vir_data['infected_others_ts']:
                cuminf[ts_to_idx[timestamp]] += 1

    cuminf = np.cumsum(np.array(cuminf))
    cuminf = cuminf / float(len(persons))
    return cuminf
        