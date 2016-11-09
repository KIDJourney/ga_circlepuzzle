# ga_circlepuzzle   

Use genetic algorithm to fit circles to image.

Inspired by (GA_engine)[https://github.com/pikeszfish/GA_engine].

## example 

![chrome](https://raw.githubusercontent.com/KIDJourney/ga_circlepuzzle/master/chrome.png)
![0.png](https://raw.githubusercontent.com/KIDJourney/ga_circlepuzzle/master/output/0.png)
![8000.png](https://raw.githubusercontent.com/KIDJourney/ga_circlepuzzle/master/output/8000.png)
![16000.png](https://raw.githubusercontent.com/KIDJourney/ga_circlepuzzle/master/output/16000.png)
![24000.png](https://raw.githubusercontent.com/KIDJourney/ga_circlepuzzle/master/output/24000.png)
![32000.png](https://raw.githubusercontent.com/KIDJourney/ga_circlepuzzle/master/output/32000.png)
![40000.png](https://raw.githubusercontent.com/KIDJourney/ga_circlepuzzle/master/output/40000.png)
![48000.png](https://raw.githubusercontent.com/KIDJourney/ga_circlepuzzle/master/output/48000.png)

## Usage

usage: transform.py [-h] [--max_loop MAX_LOOP] [--save_pre_loop SAVE_PRE_LOOP]
                    [--mutate_rate MUTATE_RATE] [--mutate_speed MUTATE_SPEED]
                    [--circle_nums CIRCLE_NUMS]
                    target output
                    
## Extend
 
You can write your class which implement `mutate`, `_mutate`, `as_image` method to use new shape to fit the image.

## What's more 

The speed of python to processing image is poor, use pypy if you want quicker fit.
 
## LICENSE
    
MIT

## Thanks

Special thanks to (GA_engine)[https://github.com/pikeszfish/GA_engine].