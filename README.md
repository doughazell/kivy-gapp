# Get running on MacOS High Sierra
```
$ brew update
$ brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
$ sudo python -m ensurepip
$ sudo python -m pip install kivy
```
https://github.com/pypa/pip/issues/3165#issuecomment-145856429
```
$ sudo python -m pip install gspread --ignore-installed six
$ sudo python -m pip install oauth2client

$ cd kivy-gapp ; python main.py
```

### pyenv Python 2
The system is currently configured to use Python 2 (which has now been deprecated) so to use an existing install having upgraded Python use:
```
kivy-gapp$ pyenv versions
  system
  * 3.9.15 (set by /Users/doug/.pyenv/version)
  
kivy-gapp$ python main.py 
Traceback (most recent call last):
  File "/Users/doug/src/kivy-gapp/main.py", line 1, in <module>
    from kivy.app import App
ModuleNotFoundError: No module named 'kivy'

kivy-gapp$ pyenv local system
kivy-gapp$ pyenv versions
* system (set by /Users/doug/src/kivy-gapp/.python-version)
  3.9.15
```
