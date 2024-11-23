Grand Prix '86
==============

Grand Prix '86 is an attempt at a solid-state conversion / re-theme
of the 1976 [EM Pinball
Machine](http://www.ipdb.org/machine.cgi?id=1072) by Williams.

![Playfield](https://github.com/deathsave/grand-prix/raw/main/monitor/playfield.jpg)


Proposed OPP Build
------------------

OPP boards can each have up to 4 wings attached as shown:

![OPP Processor Board](http://pinballmakers.com/wiki/images/f/f1/Opp-processor.png)

### Board Switch Mapping

For latest, see
[Google Sheet](https://docs.google.com/spreadsheets/d/1fP1gkxzNxdvTTTq80cS0wRv1wayha4IzK5jE9S3geUE/edit?usp=sharing).

### Setup for MacOS

1. Install Python 3.11+ with `pyenv`
2. Clone `mpf`
   `git clone https://github.com/missionpinball/mpf.git`
2. Checkout the `0.57.x` branch
   `git checkout 0.57.x`
3. `cd` into the repo folder and install `mpf`.
   `pip install -e .`
4. Install `mpf-mc` deps with:
   `brew install SDL2 SDL2_mixer SDL2_image gstreamer`
5. Install mpf-mc with `pip install mpf-mc`
6. Install foreman with `gem install foreman` - this makes it
   possible to run all 3 processes in a single terminal window
   for local development.

### Running

- **Development** - `bin/dev` will run both `mpf` and `mpf-mc`
  without the console GUI. It will also run `mpf monitor` so you can
  interact with it.
- **Production** - `bin/run` will run for production using the real
  hardward devices and the console GUI.
- **Test** - `bin/test` will run all tests from the `./tests` folder.
