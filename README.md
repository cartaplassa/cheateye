# cheateye

## Installation

```bash
git clone git@github.com:cartaplassa/cheateye.git
cd cheateye
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Or something like that, I dunno

## Usage

```bash
python main.py -f N
```

will generate N columns

```bash
python main.py -w N
```

will generate N-symbol-wide columns

You can chain a script like

```bash
clear && cd ~/Downloads/cheateye && source .venv/bin/activate && python main.py -w 55 && deactivate && cd
```

and put it in autostart.sh, just play around with values to find those that work best, they depend heavily on terminal configuration.

Also, `lists` prolly won't work. They might, but they're supposed to be individualized, so take time to write your own.

## Result
![screenshot-20231004-143248](https://github.com/cartaplassa/cheateye/assets/99555654/da1a9bac-1c12-4614-88af-6b500f20d465)

