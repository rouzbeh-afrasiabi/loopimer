# loopimer
<p align="justify">
Package for time-controlled execution of a looping function using threading. Allows control over the time between each function execution and the introduction of time delays/pauses. Furthermore, the package utilizes Queues and slicing to provide the user with the ability to control the execution of the looping function using queued slices. The package was originally developed for working with rate limited APIs and only uses python standard libraries.
</p>  

## Requirements
### Python Standard Libraries
 - threading
 - time
 - datetime
 - queue
 - math
 - sys
 - os
## Decorators:
 - loopimer
 
## Examples
### Simple Usage: 
```
from loopimer import *

@loopimer(every=1)
def test(loop,t):
    loop.s_print(loop.now,' ',loop.elapsed)
    if(loop.counter%3==0):
        loop.pause=20
    if(loop.counter%5==0):
        loop.pause=2
    if(loop.counter==20):
        loop.kill()

```
