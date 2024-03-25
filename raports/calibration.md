# Calibration in EPANET

## Why do we need calibration?

Every model is only an approximate representation of a given reality to some extent. However, we should strive to ensure that the model always represents our network as closely as possible. To this end, a so-called calibration is performed, which is a process aimed at matching the indications of the model to the actual values occurring on the network. A skilfully calibrated model guarantees high efficiency.

## Calibration Files

 A Calibration File is a text file containing measured data for a particular quantity taken over a particular period of time within a distribution system. The file provides observed data that can be compared to the results of a network simulation. Separate files should be created for different parameters (e.g., pressure, fluoride, chlorine, flow, etc.) and different sampling studies. Each line of the file contains the following items:
 - Location ID - ID label (as used in the network model) of the location where the measurement was made
 - Time - Time (in hours) when the measurement was made
 - Value - Result of the measurement

 An excerpt from a Calibration File:
```{}
;Fluoride Tracer Measurements

;Location  Time   Value

;--------------------------

       N1    0      0.5
             6.4    1.2
            12.7    0.9
       N2    0.5    0.72
             5.6    0.77
```

### Registering Calibration Data
To register calibration data residing in a Calibration File:

1. Select __Project >> Calibration Data__ from the __Menu Bar__.
2. In the __Calibration Data__ dialog form, click in the box next to the parameter you wish to register data for.
3. Either type in the name of a __Calibration File__ for this parameter or click the __Browse__ button to search for it.
4. Click the __Edit__ button if you want to open the __Calibration File__ in Windows NotePad for editing.
5. Repeat steps 2 - 4 for any other parameters that have calibration data.
6. Click __OK__ to accept your selection

More information: [EPANET Documentation - Calibration Data](https://epanet22.readthedocs.io/en/latest/5_projects.html#calibration-data)