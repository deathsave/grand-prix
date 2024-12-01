Grand Prix '86
==============

[![Grand Prix '86 Pinball](https://github.com/deathsave/grand-prix/actions/workflows/python-app.yml/badge.svg)](https://github.com/deathsave/grand-prix/actions/workflows/python-app.yml)

Grand Prix '86 is an attempt at a solid-state conversion / re-theme
of the 1976 [EM Pinball
Machine](http://www.ipdb.org/machine.cgi?id=1072) by Williams.

![Playfield](https://github.com/deathsave/grand-prix/raw/main/monitor/playfield.jpg)

### Rules

**Proposed rules [can be found from here](https://github.com/deathsave/grand-prix/blob/main/docs/RULES.md).**

### Docs

A simple web server is included to serve up the markdown docs and
Mermaid diagrams. To setup, run `pip install -r requirements.txt`
in the `./web/` root. Then to run it, use `bin/docs`.

```mermaid
graph TD
    TODO --> DIAGRAM["Diagram Modes"]
```

### Production Machine Setup

Hardware is as such:

- [Mini 5" HDMI Display](https://www.amazon.com/dp/B0CP3DH3LN)
- [MLLSE M2 Mini PC](https://www.newegg.com/mllse-m2/p/2SW-00A4-00007)
- [OPP "Cypress" Pinball Interface](https://pinballmakers.com/wiki/index.php?title=OPP-Cypress)
- [My Pinballs Segment Display](https://missionpinball.org/latest/hardware/mypinballs/wiring/)
- [FadeCandy LED Controller](https://www.adafruit.com/product/1689)

**A guide to setup the [production machine on Xubuntu is here](https://github.com/deathsave/grand-prix/blob/main/docs/XUBUNTU.md).**

Proposed OPP Build
------------------

OPP boards can each have up to 4 wings attached as shown:

![OPP Processor Board](http://pinballmakers.com/wiki/images/f/f1/Opp-processor.png)

### Board Switch Mapping

For latest, see
[Google Sheet](https://docs.google.com/spreadsheets/d/1fP1gkxzNxdvTTTq80cS0wRv1wayha4IzK5jE9S3geUE/edit?usp=sharing).

### Setup for MacOS

1. Install Python 3.11+ with `pyenv`
2. Install mpf with `pip install mpf==0.57`
3. Install `mpf-mc` deps with:
   `brew install SDL2 SDL2_mixer SDL2_image gstreamer`
4. Install mpf-mc with `pip install mpf-mc==0.57`
5. Install mpf-monitor with `pip install mpf-monitor==0.57`
6. Install foreman with `gem install foreman` - this makes it
   possible to run all 3 processes in a single terminal window
   for local development.

### Running

- **Development** - `bin/dev` will run both `mpf` and `mpf-mc`
  without the console GUI. It will also run `mpf monitor` so you can
  interact with it.
- **Production** - `bin/run` will run for production using the real
  hardware devices and the console GUI.
- **Test** - Run a test with `bin/test tests/test_something.py` or
  simply `bin/test` to run all tests from the `./tests` folder.
