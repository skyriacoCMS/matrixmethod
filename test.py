#!/usr/bin/env python

from sample import *
from random import randint

s = SumOfSamples()

for i in range(35):
  couplings = {
    "ghv1": randint(-10, 10),
    "ghz2": randint(-10, 10),
    "ghw2": randint(-10, 10),
    "ghz4": randint(-10, 10),
    "ghw4": randint(-10, 10),
    "ghz1prime2": randint(-10, 10),
    "ghw1prime2": randint(-10, 10),
    "ghzgs1prime2": randint(-10, 10),
  }

  s += Sample("VBF", **couplings)

w = s.weight
for _ in "+-*/":
  print _, w.count(_)
