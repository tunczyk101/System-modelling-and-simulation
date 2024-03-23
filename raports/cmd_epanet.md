# Command Line EPANET

EPANET can be run as a console application using commandline.
To use this version clone this [EPANET GitHub Repository](https://github.com/OpenWaterAnalytics/EPANET/tree/dev).

```cmd
git clone <EPANET GitHub Repository>
```

Go to root directory of the project and enter the following commands:

```cmd
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

The `runepanet.exe` will be placed in the `build\bin\Release` (Windows) or `build\lib\Release` (Linux/Mac). More information: [Building EPANET](https://github.com/OpenWaterAnalytics/EPANET/blob/dev/BUILDING.md).

In this case input network are placed into a text file and results are written also to the text file.

To run cmd EPANET go to the directory in which EPANET is installed or add this directory to system PATH variable.

```cmd
runepanet inpfile rptfile
```

- **inpfile** - name of the impou file
- **rptfile** - ame of the outpot rport file

Example data is placed inside `epanet_files\example`. You can use them to test whether Command Line EPANET is working. Go to root directory of this repository and run:

```cmd
runepanet ./epanet_files/example/tutorial.txt ./epanet_files/example/tutorial_results.txt
```

Or choose an empty `.txt` file as rpt file.
