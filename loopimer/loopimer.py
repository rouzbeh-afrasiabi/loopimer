import threading
import time
import datetime as dt
from threading import Semaphore,Timer
import queue
import math
import sys
import os


class timer:
    def __init__(self,target=None,n_splits=0):

        def _nslice(s, n, truncate=False, reverse=False):
            """Splits s into n-sized chunks, optionally reversing the chunks."""
            assert n > 0
            while len(s) >= n:
                if reverse: yield s[:n][::-1]
                else: yield s[:n]
                s = s[n:]
            if len(s) and not truncate:
                yield (s)
        self.loop=False
        self.print_it=False
        self.start_time=0
        if(target):
            self._input=_nslice(target,n_splits)
        else:
            self._input=[0]
        self.sequence = queue.Queue()
        self.minutes=0
        self.seconds=0
        self.hours=0
        self.total_seconds=0
        self.timedelta=dt.timedelta(hours=0,minutes=0,seconds=0,milliseconds=0 ,microseconds=0)
        self.strftime=0
        self._activeEvent=False
        self.lock = threading.Lock() 
        self._timerEnd=threading.Event()
        self._killit=threading.Event()
        self.keep_alive=False
        self.delay=0
        self._target_function=None
        self.pause=0
        self._kwargs=None
        self._timer_thread=None
        self._running_thread=None
        self.counter=0
        #put slices in queue
        for item in self._input:
            self.sequence.put(item)
        
        
    def apply_to(self,function,**kwargs):
        self._target_function=function
        self._kwargs=kwargs
        
    def s_print(self,*a, **b):
        with (self.lock):
            print(*a, **b)
            
        
    def _trigger(self,):
        self._timerEnd.clear()
        while (not self.sequence.empty()):
            
            if(not self.loop):
                self.loop=False
                self._timerEnd.set()
                break
            else:
                time.sleep(1)
                td=dt.datetime.now()-self.start_time
                self.timedelta=td
                self.hours, remainder = divmod(td.seconds, 3600)
                self.minutes, self.seconds = divmod(remainder, 60)
                self.total_seconds=td.total_seconds()
                self.strftime="{:0>2}:{:0>2}:{:0>2}".format(int(self.hours),int(self.minutes),int(self.seconds))
                if (self.print_it): 
                    self.s_print(self.strftime,end='\r')
        if (self.print_it):
            self.s_print('\r')
        self.loop=False
        self._timerEnd.set()
        

    def start(self,print_it=False):
        if(not self.loop):
            self.print_it=print_it
            self.start_time=dt.datetime.now()

            main_trigger=threading.Thread(target=self._trigger)
            main_trigger.setDaemon(True)
            self.loop=True
            self._timer_thread=main_trigger
            main_trigger.start()  
        
    def stop(self,):
        self.loop=False
    
    def get(self,):
        return(self.sequence.get())
    
    def kill(self,):
        while (self.keep_alive):
            self.keep_alive=False
            if(self.loop):
                self.loop=False
    
    def _eventTrigger(self,total_seconds):
        while (not self.sequence.empty()):
            if(self.total_seconds>=total_seconds):
#                 self.s_print('triggered',self.loop)
                self.stop()
                break

    def addTimeEvent(self,total_seconds=None): 
        event_trigger=threading.Thread(target=self._eventTrigger,args=(total_seconds,))
        event_trigger.setDaemon(True)
        event_trigger.start() 

    def _simpleloopTrigger(self,every):
        while (not self.sequence.empty()):
            if(not self.keep_alive):
                break
            else:
                time.sleep(every)
                if(self._target_function and self.keep_alive):
                    self._target_function(self,**self._kwargs)
                else:
                    break
        
    def startSimpleLoop(self,every=None):
        loop_trigger=threading.Thread(target=self._simpleloopTrigger,args=(every,))
        loop_trigger.setDaemon(True)
        self.keep_alive=True
        self._running_thread=loop_trigger
        loop_trigger.start() 
        
    def _timedloopTrigger(self,every):
        while (not self.sequence.empty()):
            if(not self.keep_alive):
                break
            else:
                time.sleep(every)
                if(self.pause>0):
                    self.s_print("Process suspended for ", self.pause," seconds")
                    self.start(True)
                    time.sleep(self.pause)
                    self.pause=0
                    self.stop()
                    self._timerEnd.wait()
                if(self._target_function and self.keep_alive):
                    if(self.pause>0 and not self._timerEnd.isSet()):
                        continue
                    elif(self.pause==0):
                        self.counter=self.counter+1
                        self._target_function(self,**self._kwargs)
                else:
                    break
        
    def startTimedLoop(self,every=None):
        loop_trigger=threading.Thread(target=self._timedloopTrigger,args=(every,))
        loop_trigger.setDaemon(True)
        self.keep_alive=True
        self.counter=0
        self._running_thread=loop_trigger
        loop_trigger.start() 