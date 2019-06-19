MemoryCollector
------
This is a process status recorder constructed by Python3.
Now can only trace the data of the cpu usage and memory of a certain process.

##### For mac users
Please be sure that you already installed the xcrun
You can install it by
```
    xcode-select --install
```

#### How to use
- For mac users, You can double click the start.command
- For win users
  1. Cd to the root of this folder
  2. Download the supporting external libraries by executing
     ```
          pip install -r requirements.txt
     ```
  3. Use
     ```
         python sys_listener.py 
     ```
     to run it
