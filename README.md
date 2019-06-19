MemoryCollector
------
This is a process status recorder constructed by Python3.
Now can only trace the data of the cpu usage and memory of a certain process.

#### How to use
##### For mac users
Please be sure that you already installed the xcrun
You can install it by
```
    xcode-select --install
```
1. Cd to the root of this folder
2. Download the supporting external libraries by executing
   ```
        pip3 install -r requirements.txt
   ```
3. Use
   ```
       python3 sys_listener.py 
   ```
   to run it
