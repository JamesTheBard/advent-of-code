If you loop across all positions from the minimum position in the
input to the maximum:

```
 Performance counter stats for 'python solution.py':

            214.65 msec task-clock:u                     #    0.998 CPUs utilized             
                 0      context-switches:u               #    0.000 /sec                      
                 0      cpu-migrations:u                 #    0.000 /sec                      
             1,317      page-faults:u                    #    6.136 K/sec                     
     1,097,150,037      cycles:u                         #    5.111 GHz                       
       120,022,828      stalled-cycles-frontend:u        #   10.94% frontend cycles idle      
     5,394,000,363      instructions:u                   #    4.92  insn per cycle            
                                                  #    0.02  stalled cycles per insn   
       962,120,946      branches:u                       #    4.482 G/sec                     
         3,147,393      branch-misses:u                  #    0.33% of all branches           

       0.215100671 seconds time elapsed

       0.214898000 seconds user
       0.000000000 seconds sys
```

However, if you loop across starting at the minimum and returning the minimum
fuel amount once the calculated fuel starts increasing.  The amount of fuel
burned is a curve with a well-defined minimum so once it starts increasing you
can just return the minimum fuel.

```
 Performance counter stats for 'python solution.py':

             64.84 msec task-clock:u                     #    0.995 CPUs utilized             
                 0      context-switches:u               #    0.000 /sec                      
                 0      cpu-migrations:u                 #    0.000 /sec                      
             1,310      page-faults:u                    #   20.204 K/sec                     
       273,258,916      cycles:u                         #    4.214 GHz                       
        44,802,518      stalled-cycles-frontend:u        #   16.40% frontend cycles idle      
     1,181,512,309      instructions:u                   #    4.32  insn per cycle            
                                                  #    0.04  stalled cycles per insn   
       211,174,831      branches:u                       #    3.257 G/sec                     
         1,287,326      branch-misses:u                  #    0.61% of all branches           

       0.065171205 seconds time elapsed

       0.065110000 seconds user
       0.000000000 seconds sys
```