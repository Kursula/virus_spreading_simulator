import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter


def plot_visuals(scenarios : list, 
                 figsize : tuple = (10, 12),
                 fontsize : float = 14, 
                 sigma : float = 24) -> None:
 
    specs = [
        {
            'key' : 'sick_ratio',
            'title' : 'Ratio of population (n={}) sick'.format(len(scenarios[0]['persons'])),
            'ylabel' : 'Ratio of population',
        },
        {
            'key' : 'cumul_inf_ratio',
            'title' : 'Cumulative ratio of population (n={}) infected'.format(len(scenarios[0]['persons'])),
            'ylabel' : 'Ratio of population',
        },
        {
            'key' : 'r_value',
            'title' : 'Average R value',
            'ylabel' : 'R',
        }
    ]

    plt.figure(figsize=figsize)
    
    for i, spec in enumerate(specs): 
        plt.subplot(len(specs), 1, i + 1)
        
        for scen in scenarios:
            timesteps = np.array(scen['timesteps']) / 24
            plt.plot(
                timesteps, 
                gaussian_filter(scen[spec['key']], sigma=sigma),
                label=scen['label']
            )
        plt.legend(
            fontsize=fontsize,
            bbox_to_anchor=(1, 1),
            loc='upper left'
        )
        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        plt.title(spec['title'], fontsize=fontsize)
        plt.xlabel('Day', fontsize=fontsize)
        plt.ylabel(spec['ylabel'], fontsize=fontsize)
    
    plt.tight_layout()
    plt.show()
    