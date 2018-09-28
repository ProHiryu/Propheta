# WinNET

As e-sports become more and more popular, e-sports gambling has also been accepted by the majority of gamblers. The purpose of winnet is to achieve a deep neural network that can perfectly predict the results of e-sports competition. Although the process is very difficult, I will keep working hard and welcome you to keep improving.

## Samples

Use 2018 lol games to feed the net, and predict.

- just Heros pick on input data
- one-hot encoding

## Version 1.0

### Graphs

![](http://wx4.sinaimg.cn/mw690/0060lm7Tly1fvoyopjjuaj31hg15o0zb.jpg)

### Usage

```bash
$ python winnet.py
```

### Requirements

- tensorflow > 1.5
- numpy
- pandas
- tqdm
- sklearn

### Configuration

You can set the time period you want to grab in the configuration file and set the total number of heroes in the current LOL, but you can also set the location and name of the data file

## To DO

- sparse inputs
- improve networks performance

Hope you can help!
