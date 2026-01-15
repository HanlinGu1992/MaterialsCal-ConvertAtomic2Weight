# Conversion Between Atomic Percent and Weight Percent (at.%  $\leftrightarrow$ wt.%)

This code provides a solution for the conversion between atomic percentage and weight percentage.

## Generation of the Executable Program

### Step 1. Generate Atomic Weight JSON File

**1. Install the `mendeleev` package**

Execute the following command in the terminal:

```python
pip install mendeleev
```

**2. Install the `mendeleev` package**

Execute `01_get_atomic_weight.py` to generate `01_element_atomic-masses.json`, which contains the atomic weights of all elements from the Python package `mendeleev`.

Execute the following command in the terminal:

```python
python 01_get_atomic_weight.py
```

### Step 2. Packaging of GUI Applications

**1. Install the `pyinstaller` package**
Execute the following command in the terminal:

```python
pip install pyinstaller
```

**2. Package the GUI application**
Execute the following command in the terminal:

```python
pyinstaller --onefile --windowed --add-data "01_element_atomic-masses.json;." 02_GUI.py
```

### Executable Program

Find the Executable Program in the `dist` folder with name `02_Gui.exe`. Double click and enjoy the code.
