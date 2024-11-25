So, we're not gonna talk about this solve.  I got both days done, but the code
is bad enough to make it very slow and you have to generate the 5x5 version
of part 1, dump that into the part 1 solve, then wait for what could only be
called an eternity.

Part 1:

```
 Performance counter stats for 'python solution.py':

            661.50 msec task-clock:u                     #    0.999 CPUs utilized             
                 0      context-switches:u               #    0.000 /sec                      
                 0      cpu-migrations:u                 #    0.000 /sec                      
             4,182      page-faults:u                    #    6.322 K/sec                     
     3,410,906,221      cycles:u                         #    5.156 GHz                       
       233,962,206      stalled-cycles-frontend:u        #    6.86% frontend cycles idle      
    15,248,025,467      instructions:u                   #    4.47  insn per cycle            
                                                  #    0.02  stalled cycles per insn   
     2,624,355,467      branches:u                       #    3.967 G/sec                     
         4,868,375      branch-misses:u                  #    0.19% of all branches           

       0.661984161 seconds time elapsed

       0.661354000 seconds user
       0.000000000 seconds sys
```

Part 2:

```
 Performance counter stats for 'python solution.py':

        376,144.30 msec task-clock:u                     #    1.000 CPUs utilized             
                 0      context-switches:u               #    0.000 /sec                      
                 0      cpu-migrations:u                 #    0.000 /sec                      
           417,637      page-faults:u                    #    1.110 K/sec                     
 2,039,646,565,545      cycles:u                         #    5.423 GHz                       
   121,515,531,001      stalled-cycles-frontend:u        #    5.96% frontend cycles idle      
 6,872,322,211,666      instructions:u                   #    3.37  insn per cycle            
                                                  #    0.02  stalled cycles per insn   
 1,196,235,252,435      branches:u                       #    3.180 G/sec                     
     1,792,836,077      branch-misses:u                  #    0.15% of all branches           

     376.193674441 seconds time elapsed

     375.114417000 seconds user
       0.732595000 seconds sys
```