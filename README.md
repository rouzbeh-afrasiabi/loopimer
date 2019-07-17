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

### Importing 
```
from loopimer import *
```
### Simple Usage: 

<p align="justify">
In the simplest usage case, you pass a value in seconds to the decorator through the 'every' variable. This will modify the
function that is declared after the decorator to execute every x seconds as an indefinite loop when called.
</p>

```
@loopimer(every=5)
def test(loop,): 
    print('loopimer')
test()    
```
<p align="justify">
The first variable passed to the target function allows you to control the loop running in the background (called loop in the below example). You can choose any name for this variable, but it is important that you pass a variable name as a placeholder when declaring your function. Upon calling the function this placeholder will be linked to the related thread controling the loop.
</p>

<p align="justify">
The loop starts authomatically when the function is called and will run indefinity. You can control the loop and how the function is executed using the placeholder variable.  
</p>

<p align="justify">
By simply calling the function the loop will begin. Please note that when calling the function we don't provide the placeholder variable name.
</p>

```
@loopimer(every=1)
def test(loop,t): 
    #it is reccommended that you use the s_print() function for printing to avoid 
    loop.s_print(loop.now,' ',loop.elapsed)
    if(loop.counter%3==0):
        #the loop can be delayed by passing a value in seconds
        loop.pause=20
    if(loop.counter%5==0):
        loop.pause=2
    if(loop.counter==20):
        #the loop can be terminated by calling kill()
        loop.kill()

test(t=1)
        
```
