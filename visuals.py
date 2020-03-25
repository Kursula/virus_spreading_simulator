import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
import matplotlib.patches as patches
from scipy.ndimage import gaussian_filter


def plot_sick_ratio(results : dict, 
                    figsize : tuple = (8, 4),
                    fontsize : float = 14) -> None:
    """
    Plots sick ratios. 
    """
    plt.figure(figsize=figsize)
    for key, values in results.items():
        timesteps = np.array(values['x']) / 24
        plt.plot(timesteps, 
                 gaussian_filter(values['sick_ratio'], sigma=24),
                 label=values['label'])
    
    plt.legend(fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.title('Ratio of population sick', fontsize=fontsize)
    plt.xlabel('Days from start', fontsize=fontsize)
    plt.ylabel('Ratio of all persons', fontsize=fontsize)
    plt.show()
    
    
def plot_cumul_inf_ratio(results : dict, 
                         figsize : tuple = (8, 4),
                         fontsize : float = 14) -> None:
    """
    Plots cumulative infection ratios. 
    """
    plt.figure(figsize=figsize)
    for key, values in results.items():
        timesteps = np.array(values['x']) / 24
        plt.plot(timesteps, 
                 gaussian_filter(values['cumul_new_inf'], sigma=24),
                 label=values['label'])
    
    plt.legend(fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.title('Cumulative ratio of population infected', fontsize=fontsize)
    plt.xlabel('Days from start', fontsize=fontsize)
    plt.ylabel('Ratio of all persons', fontsize=fontsize)
    plt.show()
    

def render(persons : list, 
           events : list, 
           sim_time : float, 
           figsize : tuple = (9, 9)) -> None: 
    """
    Rendering of the simulation map and persons in their locations. 
    Sickness status and sneezing are indicated by color and radius of the 
    person marker. 
    
    Note that the rendeing is slow with large setups. 
    """
    event_name_offset = np.array([0, -5])
    
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, aspect='equal')
    
    # Draw event location borders
    for event in events: 
        loc = np.array(event.get_loc())
        size = event.get_size()
        rect = patches.Rectangle(xy=loc, 
                                 width=size[0],
                                 height=size[1],
                                 linewidth=1,
                                 edgecolor='black',
                                 facecolor='none')
        ax.add_patch(rect)
        # Plot event name
        plt.annotate(xy=loc + event_name_offset, 
                     s=event.name)

    # Plot persons 
    for person in persons: 
        # Color code the sick status 
        color = person.get_color()
        radius = person.get_radius()
        loc = person.get_loc()
        plt.scatter(x=loc[0], y=loc[1], s=radius, color=color)
    
    clear_output(wait=True)
    days = int(sim_time / 24)
    hours = sim_time - days * 24 
    plt.title('Day {}, hour {:0.1f}'.format(days, hours))
    plt.xticks([])
    plt.yticks([])
    plt.show()

    