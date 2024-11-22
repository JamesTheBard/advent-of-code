Using a list to capture each individual lantern fish and just making that list bigger:

```
 Performance counter stats for 'python solution.py':

            109.54 msec task-clock:u                     #    0.996 CPUs utilized             
                 0      context-switches:u               #    0.000 /sec                      
                 0      cpu-migrations:u                 #    0.000 /sec                      
            15,838      page-faults:u                    #  144.585 K/sec                     
       464,662,972      cycles:u                         #    4.242 GHz                       
        49,466,920      stalled-cycles-frontend:u        #   10.65% frontend cycles idle      
     2,469,281,842      instructions:u                   #    5.31  insn per cycle            
                                                  #    0.02  stalled cycles per insn   
       381,520,224      branches:u                       #    3.483 G/sec                     
           767,859      branch-misses:u                  #    0.20% of all branches           

       0.109964212 seconds time elapsed

       0.096488000 seconds user
       0.013323000 seconds sys
```

Converting the list into a dict where the key is point in time of the fish's lifecycle
and the value is the number of fish at that particular point:

```
 Performance counter stats for 'python solution.py':

             14.34 msec task-clock:u                     #    0.968 CPUs utilized             
                 0      context-switches:u               #    0.000 /sec                      
                 0      cpu-migrations:u                 #    0.000 /sec                      
             1,294      page-faults:u                    #   90.228 K/sec                     
        53,918,261      cycles:u                         #    3.760 GHz                       
        23,233,846      stalled-cycles-frontend:u        #   43.09% frontend cycles idle      
        90,949,209      instructions:u                   #    1.69  insn per cycle            
                                                  #    0.26  stalled cycles per insn   
        19,288,849      branches:u                       #    1.345 G/sec                     
           712,086      branch-misses:u                  #    3.69% of all branches           

       0.014808707 seconds time elapsed

       0.011117000 seconds user
       0.003704000 seconds sys
```

Running the updated version for part 2:

```
 Performance counter stats for 'python solution.py':

             15.08 msec task-clock:u                     #    0.973 CPUs utilized             
                 0      context-switches:u               #    0.000 /sec                      
                 0      cpu-migrations:u                 #    0.000 /sec                      
             1,295      page-faults:u                    #   85.870 K/sec                     
        54,185,756      cycles:u                         #    3.593 GHz                       
        23,134,540      stalled-cycles-frontend:u        #   42.69% frontend cycles idle      
        93,916,238      instructions:u                   #    1.73  insn per cycle            
                                                  #    0.25  stalled cycles per insn   
        19,778,040      branches:u                       #    1.311 G/sec                     
           716,219      branch-misses:u                  #    3.62% of all branches           

       0.015499751 seconds time elapsed

       0.015512000 seconds user
       0.000000000 seconds sys
```