# Bello: A Video chat platform implemented purely in python.
Author: Phvash
version 0.1 (Beta Preview)
==========================================================================

### About

* uses tcp protocol
* written in python 2
* compatible with smartphones through qpython
* minimal external module dependency

### Requirements
* opencv (sudo apt-get install python-opencv libopencv-dev python-numpy python-dev)
* sounddevice (pip install sounddevice)

### Installation

* Download or clone from https://www.github.com/phvash/Bello

### How to use:

<<<<<<< HEAD
- To launch, run 'app.py' from the terminal or cmd 
      ``` $ python app.py ```

### To do:
* Build GUI for easier user interraction
* Add support for video conferencing
=======
1. Always leave 'host.py' running in the background to accept incoming phone calls 
   - To launch, run 'host.py' from the terminal or cmd 
      ``` $ python host.py ```

2. To Make a phone call
   - Run the 'client.py' script from terminal
      ``` $ python client.py ```
   - A list containing usernames of currently active (available) Bello users in your subnet will be returned
   - To place a call to any of them, enter the username when prompted.

### To do:
* Build GUI for easier user interraction
* Add audio support
* Add support for video conferencing

### Issues
* lag in audio playback
>>>>>>> 5b4c03d89f1d30f77450e6e0bd3cbb4cdade8d83
