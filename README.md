# hyperspy_gui_traitsui
[![Build Status](https://travis-ci.org/hyperspy/hyperspy_gui_traitsui.svg?branch=master)](https://travis-ci.org/hyperspy/hyperspy_gui_traitsui)



**hyperspy_gui_traitsui** provides traitsui graphic user interface (GUI) elements for hyperspy.


## Installation

# Option 1: With pip
Make sure you have
[pip installed](https://pip.pypa.io/en/stable/installing/) and run:

```bash
pip install hyperspy_gui_traitsui
```

# Option 2: With Anaconda

Install anaconda for your platform and run

```bash
conda install hyperspy_gui_traitsui -c conda-forge

```
traitsui doesn't support Qt5 as of version 5.1. Therefore, when using the
Qt toolkit it may be necessary to downgrade pyqt, which requires removing
the anaconda-navigator package as follows:

```bash

conda uninstall anaconda-navigator -y
conda install pyqt=4.11.4 -y
```

## Usage

Please refer to the [HyperSpy documentation](http://hyperspy.org/hyperspy-doc/current/index.html) for details. Example (to run in any IPython flavour):

```python
%matplotlib qt4
import hyperspy.api as hs
hs.preferences.gui(toolkit="traitsui")
```
![alt text](https://github.com/hyperspy/hyperspy_gui_traitsui/raw/master/images/preferences_gui.png "HyperSpy preferences ipywidget")


## Development

Contributions through pull requests are welcome. See the
[HyperSpy Developer Guide](http://hyperspy.org/hyperspy-doc/current/dev_guide.html).
