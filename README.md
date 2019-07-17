## loopimer
<p align="justify">
Package for time controlled execution of a function in a loop. Allows controlling the time steps between function executions and also the introduction of time delays. Furthermore, the package utilizes Queues and slicing to provide the user with the ability to control the execution of the looping function using queued slices. Tha package was originally developed for working with rate limited APIs.
</p>  

# Examples
```
from loopimer import *

@loopimer(every=1)
def test(timer,t):
    timer.s_print(timer.now,' ',timer.elapsed)
    if(timer.counter%3==0):
        timer.pause=20
    if(timer.counter%5==0):
        timer.pause=2
    if(timer.counter==20):
        timer.kill()

```
