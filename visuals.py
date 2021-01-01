import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
import matplotlib.patches as patches
from scipy.ndimage import gaussian_filter


def plot_sick_ratio(scenarios : list, 
                    figsize : tuple = (8, 4),
                    fontsize : float = 14, 
                    sigma : float = 24) -> None:
    """
    Plots sick ratios. 
    """
    plt.figure(figsize=figsize)
    for scen in scenarios:
        timesteps = np.array(scen['timesteps']) / 24
        plt.plot(timesteps, 
                 gaussian_filter(scen['sick_ratios'], sigma=sigma),
                 label=scen['label'])
    
    plt.legend(fontsize=fontsize,
               bbox_to_anchor=(1, 1),
               loc='upper left')
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.title('Ratio of population sick', fontsize=fontsize)
    plt.xlabel('Days from start', fontsize=fontsize)
    plt.ylabel('Ratio of all persons', fontsize=fontsize)
    plt.show()
    
    
def plot_cumul_inf_ratio(scenarios : list, 
                         figsize : tuple = (8, 4),
                         fontsize : float = 14, 
                         sigma : float = 24) -> None:
    """
    Plots cumulative infection ratios. 
    """
    plt.figure(figsize=figsize)
    for scen in scenarios: 
        timesteps = np.array(scen['timesteps']) / 24
        plt.plot(timesteps, 
                 gaussian_filter(scen['cumul_inf_ratios'], sigma=sigma),
                 label=scen['label'])

    plt.legend(fontsize=fontsize,
               bbox_to_anchor=(1, 1),
               loc='upper left')
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.title('Cumulative ratio of population infected', fontsize=fontsize)
    plt.xlabel('Days from start', fontsize=fontsize)
    plt.ylabel('Ratio of all persons', fontsize=fontsize)
    plt.show()
    
    