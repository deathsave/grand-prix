William’s Grand Prix
====================

Code for solid-state conversion / re-theme of the 1976 [EM Pinball Machine](http://www.ipdb.org/machine.cgi?id=1072) by William’s.

![Sanded Playfield](https://github.com/pinballplaid/grand-prix/raw/master/monitor/playfield.jpg)


Proposed OPP Build
------------------

OPP boards can each have up to 4 wings attached as shown:

![OPP Processor Board](http://pinballmakers.com/wiki/images/f/f1/Opp-processor.png)

### Board Switch Mapping

For latest, see [Google Sheet](https://docs.google.com/spreadsheets/d/1fP1gkxzNxdvTTTq80cS0wRv1wayha4IzK5jE9S3geUE/edit?usp=sharing).


How to Run
----------

### Development

- `mpf both -VXt` - smart virtual, traditional logging, no console GUI
- `mpf both -X` - just smart virtual

### Production

- `DISPLAY=:0 mpf both -Pt` - ENV is necessary for running via `ssh` session
