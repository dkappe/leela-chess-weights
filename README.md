# leela-chess-weights

## Tracking Gauntlet

The tracking gauntlet now uses lc0 with defaults. Performance is 7513 nps.

![Ratings Graph](https://raw.githubusercontent.com/dkappe/leela-chess-weights/master/chart2.png)

## Old lczero Tracking Gauntlet
![Ratings Graph](https://raw.githubusercontent.com/dkappe/leela-chess-weights/master/chart.png)

Rating diff vs Donna, Crafty, Cheng, sennpai, gull and Komodo 12 with a 10 ply opening book. Each opening is played twice, once by each side. TC is 0.25 seconds per move. Each gauntlet has 400 games per engine.

The graph shows how much better (or worse) than a particular engine Leela is by network ID. Positive numbers mean better. Error bars are generally a little over +- 30 elo. With the exception of ID238 and ID262, which are there for comparison, testing commenced with ID292 and tests every 4th network. ID238 and ID262 are thrown in for good measure.

## Changes

- Dropped Donna and Crafty
- Added Komodo 12 and Gull

## System

Intel(R) Core(TM) i7-6700HQ CPU @ 2.60GHz
GeForce GTX 1070
Ubuntu 16.04
1407 nps on v0.10 with 192x15 net

# Important Network Weights

TBD
