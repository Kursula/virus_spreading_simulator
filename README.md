## Virus Spreading Simulator 

This is simple simulator program for modeling the virus spreading in a population. 

The simulation uses a simple compartment model that divides the population to healthy, sick and healed compartments. The simulation includes features for quarantine, vaccination, lockdowns and masks. Dynamic changes to the setup during simulation can be done using time-triggered functions. 


## Disclaimer
The simulation model is meant to play with the key concepts in virus spreading control. It does not give scientifically accurate results and the parameters have not be calibrated from any kind of official sources. 

In small scale simulations, such as the cases included in the code, different initialisation parameters can have large impact on the simulation results. To obtain reliable results one should run a Monte Carlo simulation containing e.g. 100 pcs of individual scenario simulations that have been initialized with different random variables, and then calculate aggregate statistics from the results. 