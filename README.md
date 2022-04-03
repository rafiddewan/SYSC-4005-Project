# SYSC-4005-Project
## Authors 
- Rafid Dewan
- Aashan Narang
- Nick Coutts

## Running the original policy of the simulation
To run the original policy of the simulation you need to make sure that on Performance.py that the following variable is false:

```IS_ROUND_ROBIN = False```

To run the simulation you must run the following command:
``` python3 Performance.py``` to generate the production run

This will then generate the production run of the simulation in a CSV called ***Priority_Queue_Production_Run.csv***

## Running the alternative policy of the simulation
To run the alternative policy of the simulation you need to make sure that on Performance.py that the following variable is true:

```IS_ROUND_ROBIN = True```

To run the simulation you must run the following command:
``` python3 Performance.py``` to generate the production run

This will then generate the production run of the simulation in a CSV called ***RoundRobin_Production_Run.csv***