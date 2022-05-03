# NR Physical Resources Visualizer

### Preface

A simple visualizer for NR(5G) resource grid visualization for L1(Physical Layer), based on 3GPP release-16.

Implemented via Python 3.8.8+(only tested on Win10/11).

Dependencies(managed by Miniconda):

+ numpy
+ matplotlib

### Workflow

1. read `*.json` file as input, which describes the occurations of NR signals/channels,
    + Not completed yet

2. generate the signal/channel objects, which based on `NrSignalCommon`,
    + why not use duck-typing? To make sure derived class have method `get_get_resource_grid_fragments()`

3. use `get_resource_grid_fragments` to get fragments of resource grid, and fill them into class `NrPhysicalResourceRenderer`
    + max support 32 ports of L1

4. use `NrPhysicalResourceRenderer.plot()` to show the resource grids
    + you can specify which port to show

### Finished

- [x] CSI-RS downlink PHY initial supported

### TODOs

- [ ] add support for more channels of NR
- [ ] finish the json support
- [ ] more annotations on the figures
- [ ] UT and more test cases
- [ ] automatic test on GitHub with travis CI
- [ ] published to pypi.org
- [ ] a simple UI to configure/switch figures
- [ ] performance optimization
    - multi-thread support
    - python JIT with `numba`
- [ ] documentations improvement

### Reference

All reference could be found [here](https://www.3gpp.org/DynaReport/status-report.htm#activeRel-16).

1. 3GPP TS 38.211
2. 3GPP TS 38.212
3. 3GPP TS 38.213
4. 3GPP TS 38.214
5. 3GPP TS 38.300