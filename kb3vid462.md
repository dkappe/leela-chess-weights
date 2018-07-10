## KB3 v ID462 gauntlets

TC 3+1
Leela Ratio ~5.0

### Settings

```
|   _ | |
|_ |_ |_| built Jul  2 2018
uci
id name The Lc0 chess engine. v0.14.0
id author The LCZero Authors.
```

Default params used for ID462.

For KB3:
```
--cpuct=2.906
--fpu-reduction=0.515
--policy-softmax-temp=1.714
```

### Results

```
   KB3
   Rank Name                          Elo     +/-   Games   Score   Draws
      0 KB3                            35      45      80   55.0%   65.0%
      1 komodo12                      168      99      20   72.5%   55.0%
      2 gull                          -17      59      20   47.5%   85.0%
      3 cheng                         -70      64      20   40.0%   80.0%
      4 senpai                       -241     127      20   20.0%   40.0%

   ID462
   Rank Name                          Elo     +/-   Games   Score   Draws
      0 ID462                         127      65      80   67.5%   32.5%
      1 komodo12                      168     120      20   72.5%   45.0%
      2 gull                          -89     118      20   37.5%   45.0%
      3 senpai                       -338     191      20   12.5%   25.0%
      4 cheng                        -436     nan      20    7.5%   15.0%
```      

### Longer TC

Same settings, but with 6+6
```
KB3
Rank Name                          Elo     +/-   Games   Score   Draws
   0 KB3                            14     105      24   52.1%   45.8%
   1 komodo12                      280     nan       6   83.3%   33.3%
   2 gull                          120     162       6   66.7%   66.7%
   3 senpai                       -191     238       6   25.0%   50.0%
   4 cheng                        -280     nan       6   16.7%   33.3%

ID462
Rank Name                          Elo     +/-   Games   Score   Draws
   0 ID462                         154     126      24   70.8%   33.3%
   1 komodo12                        0     173       6   50.0%   66.7%
   2 gull                          -58     226       6   41.7%   50.0%
   3 senpai                       -191     nan       6   25.0%   16.7%
   4 cheng                        -inf     nan       6    0.0%    0.0%
```

### Equal Nodes
2500 nodes, same params, no smart pruning. From KB3's perspective. It has a slight edge.

```
Games:	 200
Wins:	 59
Draws:	 101
Pct:	 54.75% (45.25%)
Elo:	 33
Elo difference: 33.11 +/- 33.93
```

### Equal Nodes 2

KB3 vs ID479 at equal nodes, 2500 and 5000.

```
2500 nodes KB3 vs ID479
Games:	 100
Wins:	 31
Draws:	 47
Pct:	 54.50% (45.50%)
Elo:	 31

5000 nodes KB3 vs ID479
Games:	 100
Wins:	 27
Draws:	 59
Pct:	 56.50% (43.50%)
Elo:	 45
```

