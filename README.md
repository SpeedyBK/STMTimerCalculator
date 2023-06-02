# STMTimerCalculator

Just a little python commandline calculator, to find the optimal settings for timers on STM 32 microcontrollers. It takes 4 parameters to calculate the optimal values for prescaler and counter on STM32 Timers. 

### Parameters:
--lb: Lower Bound, the minimum value for prescaler and counter

--ub: Upper Bound, the maximum value for prescaler and counter

--baseclock: Clock on which the timer is running on your microcontroller

--targetfreq: The desired targetfrequency for the timer. The timerperiode can be calculated by 1/targetfreq.

### Commandline Example:

Our timer has a base clock of 10 MHz, and we want to get a typical samplefrequency for audio signals.

python TimerCalculator.py --lb 5 --ub 25 --baseclock 10000000 --targetfreq 44100

### Output:

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
-- Values to get the closest frequency above the target frequency:

Error = 1.757369614512462e-07

Prescaler = 15

Counter Value = 15

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
-- Values to get the closest frequency below the target frequency:

Error = -1.2426303854875091e-07

Prescaler = 12

Counter Value = 19

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

### Plot:

Plot with prescaler and countervalues on X- and Y-axis, and the resulting error on Z-axis. The green plane shows the plane with no error.
The red line shows all optimal values, assuming all real numbers were available, not only integers. 

![Figure_1](https://github.com/SpeedyBK/STMTimerCalculator/assets/34403003/b90cfc61-12d0-4ce2-94c1-6f6f47ff8110)
