![Tests](https://github.com/hyperspy/hyperspy_gui_traitsui/workflows/Tests/badge.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hyperspy_gui_traitsui.svg)
![PyPI](https://img.shields.io/pypi/v/hyperspy_gui_traitsui.svg)
[![Anaconda Cloud](https://anaconda.org/conda-forge/hyperspy-gui-traitsui/badges/version.svg)](https://anaconda.org/conda-forge/hyperspy-gui-traitsui)

**hyperspy_gui_traitsui** provides traitsui graphic user interface (GUI) elements for hyperspy.


## Installation

### Option 1: With pip
Make sure you have
[pip installed](https://pip.pypa.io/en/stable/installing/) and run:

```bash
pip install hyperspy_gui_traitsui
```

### Option 2: With Anaconda

Install anaconda for your platform and run

```bash
conda install hyperspy-gui-traitsui -c conda-forge
```

## Usage

Please refer to the [HyperSpy documentation](http://hyperspy.org/hyperspy-doc/current/index.html) for details. Example (to run in any jupyter flavour):

```python
%matplotlib qt
import hyperspy.api as hs
hs.preferences.gui(toolkit="traitsui")
```
![alt text](https://github.com/hyperspy/hyperspy_gui_traitsui/raw/master/images/preferences_gui.png "HyperSpy preferences ipywidget")


## Development

Contributions through pull requests are welcome. See the
[HyperSpy Developer Guide](http://hyperspy.org/hyperspy-doc/current/dev_guide.html).
