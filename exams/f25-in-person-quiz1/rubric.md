# In-Person Quiz Drawing Rubric

No partial credit was given on any individual rubric item.

## Question 11

### Version A

 - nothing should be async, so no stars (1pt)
 - B and C should processes, and D should be a a file (1pt)
 - A's stdout and stderr should both go to the terminal (1pt)
 - B's stdout should go to C's stdin (1pt)
 - C's stdout and stderr should go to D (1pt)

## Question 12

No credit for incorrect arrow directions.

### Version A

 - does the browser point to the laptop's loopback interface (lo), port 6000? (1pt)
 - is there an arrow from the laptop's ens0 to the virtual machine's ens0? (1pt)
 - does sshd point to the virtual machine's loopback interface (lo), port 7000? (1pt)
 - are there two containers with virtual NICs drawn (outside of the docker process) with ports 4000 and 8000? (1pt)
 - are there two arrows forwarding from the virtual machine's loopback (lo) to the container ports, through Docker? (1pt)
