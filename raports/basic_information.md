# Useful information/links

- Manual: [EPANET 2.2 Online User's Manual](https://epanet22.readthedocs.io/en/latest/)
  - [Setup](https://epanet22.readthedocs.io/en/latest/2_quickstart.html#project-setup)
  - [Format of a partial network text file](https://epanet22.readthedocs.io/en/latest/11_importing_exporting.html#sec-import-partial-net)
- [EpaCAD](https://www.epacad.com/epacad-en.php)

  _"EpaCAD is a free software which easily converts an AutoCAD file into an EPANET one (...). EpaCAD is able to automatically import the main properties of elements, largely providing the required information to build a network."_

- [EPANET-Python Toolkit](https://github.com/OpenWaterAnalytics/EPyT)

   The EPANET-Python Toolkit features easy to use commands/wrappers for viewing, modifying, simulating and plotting results produced by the EPANET libraries.

   #### How to install?
   ___Environments -> base (root) -> open terminal -> pip install epyt___
   
   -  _PyPI: __pip install epyt___

   #### How to use the Toolkit?
    **Example:**
   ```python
   >>> from epyt import epanet
   >>> 
   >>> d = epanet('Net1.inp')
   >>> d.getNodeCount()
   >>> d.getNodeElevations()
   ```
   **More examples:**

   [https://github.com/KIOS-Research/EPYT/tree/main/epyt/examples](https://github.com/KIOS-Research/EPYT/tree/main/epyt/examples)