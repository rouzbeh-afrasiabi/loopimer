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
```python
from loopimer import *
```
### Usage: 

<p align="justify">
In the simplest usage case, you pass a value in seconds to the decorator through the 'every' variable. This will modify the
function that is declared after the decorator to execute every x seconds as an indefinite loop when called.
</p>

```python
@loopimer(every=5)
def test(loop,): 
    print('loopimer')
test()    
```
<p align="justify">
 <b>
Please note that when calling the target function we don't pass the placeholder variable name to the function.
 </b>
</p>

<p align="justify">
The first variable passed to the target function allows you to control the loop running in the background (called 'loop' in the examples on this page). You can choose any name for this variable, but it is important that you pass a variable name as a placeholder to the target function when declaring your desired function. The first variable name passed to your target function during declaration will always be reserved for the loop that will be running in the background. Upon calling the target function, this placeholder will be linked to the related thread controlling the loop.
</p>

<p align="justify">
The loop starts authomatically when the function is called and will run indefinity. You can control the loop and how the function is executed using the placeholder variable. This is currently only possible when declaring the target function.
</p>

<b>Stopping the loop</b>
```python
@loopimer(every=5)
def test(loop,): 
    print('loopimer')
    loop.kill()
test()    
```

<p align="justify">
The loop placeholder variable is an open class and you can add new attributes to it. However, it is important to use attribute names that don't cause an attribute naming conflict with attribute names already being used.
</p>

```python
from random import randrange

@loopimer(every=1)
def test(loop,):
    loop.k=randrange(10)
    print(loop.k,'loopimer')
test()     
```

<b>Stopping the loop using loop counter</b>
<p align="justify">
 It is important to note that the counter starts at 1 instead of 0.
</p>

```python
@loopimer(every=1)
def test(loop,):
    print(loop.counter)
    if(loop.counter==10):
        print('loopimer')
        loop.kill()
test()   
```
<b>Stopping the loop using loop elapsed time</b>
```python
@loopimer(every=1)
def test(loop,):
    print(loop.elapsed,loop.total_seconds)
    if(loop.total_seconds>=6):
        print('loopimer')
        loop.kill()
test()  
```
<b>Using queue</b>
<p align="justify">
A sliceable variable can be passed to the loopimer decorator through the 'target' variable for processing. This sliceable variable is then split into slices of 'n_splits' size. The slices are placed in a queue and can be accessed through the 'sequence' attribute of the loop (loop.squence). This attribute is an instance of <a href='https://docs.python.org/3/library/queue.html'>Queue</a>. The loop automatically stops when no items are left in the queue.
</p>

<p align="justify">
 When a target  is not provided the queue is automatically filled with one item containing a zero. This means that the loop will stop after one cycle if the queue is accessed.</p>

```python
@loopimer(every=1)
def test(loop,):
    print(loop.counter,loop.sequence.get())
test()   
```
<b>Using queue with target and n_splits</b>
```python
target=[i for i in range(0,100,1)]
n_splits=10 

@loopimer(target=target,n_splits=n_splits,every=1)
def test(loop,):
    print(loop.sequence.get())
test()      
```

<b>Using queue without providing target and n_splits to decorator</b>
```python
import queue

new_queue=queue.Queue()
new_target=[1,2,3,4,5,6,7,8,9]
for item in new_target:
    new_queue.put(item)
    
@loopimer(every=1)
def test(loop,new_queue):
    if(loop.counter==1):
        loop.sequence=new_queue
    else:
        print(loop.counter,loop.sequence.get())
test(new_queue=new_queue) 
```

```python
import queue

@loopimer(every=1)
def test(loop):
    if(loop.counter==1):
        items=[1,2,3,4,5,6]
        loop.sequence=queue.Queue()
        for item in items:
            loop.sequence.put(item)
    else:
        print(loop.counter,loop.sequence.get())
test()   
```

<b>Adding your own queue variable to the loop</b>
```python
import queue

@loopimer(every=1)
def test(loop):
    if(loop.counter==1):
        items=[1,2,3,4,5,6]
        loop.my_queue=queue.Queue()
        for item in items:
            loop.my_queue.put(item)
        
    else:
        print(loop.counter,loop.my_queue.get())
    if(loop.my_queue.qsize()==0):
        loop.kill()
test() 

```

<b>Using time delays</b>
<p align="justify">
 By Changing the value of the loop's pause attribute you can introduce time delays. This is especially useful when you reach a rate limit when pulling/pushing data from/to an API. 
 </p>
 
```python

target=[i for i in range(0,100,1)]
n_splits=10

@loopimer(target=target,n_splits=n_splits,every=1)
def test(loop,):
    print(loop.sequence.qsize(),loop.sequence.get())
    if(loop.sequence.qsize()==8):
        loop.pause=20
test()         
```





<b>Using queue and json</b>
```python
import numpy as np
import pandas as pd
import datetime as dt
import simplejson as json

df = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))
df['date']=dt.datetime.now()

df_json=json.loads(df.to_json(orient='records'))

@loopimer(target=df_json,n_splits=10,every=1)
def test(loop,):
    print(json.dumps(loop.sequence.get()),'\n')
test()  
```
