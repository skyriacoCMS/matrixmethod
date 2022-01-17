from abc import ABCMeta, abstractproperty
from itertools import product as cartesianproduct
import operator

def product(iterable):
    return reduce(operator.mul, iterable, 1)

from extendedcounter import ExtendedCounter
from weightshelper import WeightsHelper

class SumOfSamplesBase(object):
  __metaclass__ = ABCMeta
  @abstractproperty
  def samplesandfactors(self): pass
  def __add__(self, other):
    return SumOfSamples(self.samplesandfactors + other.samplesandfactors)
  def __neg__(self):
    return SumOfSamples(-self.samplesandfactors)
  def __sub__(self, other):
    return SumOfSamples(self.samplesandfactors - other.samplesandfactors)
  def __mul__(self, scalar):
    return SumOfSamples(self.samplesandfactors * scalar)
  def __rmul__(self, scalar):
    return self * scalar
  def __div__(self, scalar):
    return SumOfSamples(self.samplesandfactors / scalar)
  @property
  def weight_terms(self):
    return [self.weight_terms_expanded]
  @property
  def weight_terms_expanded(self):
    terms = [(weight, weightfactor*factor) for s, factor in self.samplesandfactors.iteritems() for weight, weightfactor in s.weight_terms_expanded]
    c = ExtendedCounter()

    for weight, factor in terms:
      c[weight] += factor

    maxfactor = max(abs(factor) for factor in c.values())
    if maxfactor:
      for weight, factor in c.items():
        if abs(factor/maxfactor) < 1e-10: del c[weight]

    return [(weight, factor) for weight, factor in c.iteritems()]

  @property
  def weight(self):
    result = "*".join(
                      "("+
                      "+".join(
                               "({}*{})".format(weightname, couplingsq)
                                   for weightname, couplingsq in factor
                              )
                      +")" if factor else "0"
                      for factor in self.weight_terms
                     )
    return result


class SumOfSamples(SumOfSamplesBase):
  def __init__(self, samplesandfactors=None):
    if samplesandfactors is None: samplesandfactors = ExtendedCounter()
    self.__samplesandfactors = samplesandfactors
  @property
  def samplesandfactors(self): return self.__samplesandfactors

class Sample(SumOfSamplesBase):
    def __init__(self, productionmode,useHJJ=False, **kwargs):
        self.productionmode = productionmode
        self.useHJJ = useHJJ
        self.ghv1 = kwargs.pop("ghv1")
        self.ghz2 = kwargs.pop("ghz2")
        self.ghw2 = kwargs.pop("ghw2")
        self.ghz4 = kwargs.pop("ghz4")
        self.ghw4 = kwargs.pop("ghw4")
        self.ghz1prime2 = kwargs.pop("ghz1prime2")
        self.ghw1prime2 = kwargs.pop("ghw1prime2")
        self.ghzgs1prime2 = kwargs.pop("ghzgs1prime2")

        if self.productionmode == "ggH":
            self.ghg2 = kwargs.pop("ghg2")
            self.ghg4 = kwargs.pop("ghg4")
        if self.productionmode == "ttH":
            self.kappa = kwargs.pop("kappa")
            self.kappa_tilde = kwargs.pop("kappa_tilde")



        
    @property
    def ghz1(self): return self.ghv1
    @property
    def ghw1(self): return self.ghv1

    @property
    def weight_terms(self):
        factors = []

        weightshelper = WeightsHelper(self.productionmode,self.useHJJ)

        for prodordec in "prod", "dec":
          if weightshelper.useproddec(prodordec):
            counter = ExtendedCounter()
            for couplingname, couplingvalue, weight in weightshelper.couplingsandweights(prodordec, mix=False):
              coupling = getattr(self, couplingname) / float(couplingvalue)
              counter[weight] += coupling**2
            for ((coupling1name, coupling1value, weight1),
                 (coupling2name, coupling2value, weight2),
                 weightint) in weightshelper.couplingsandweights(prodordec, mix=True):
              coupling1 = getattr(self, coupling1name ) / float(coupling1value)
              coupling2 = getattr(self, coupling2name ) / float(coupling2value)
              counter[weight1]   -= coupling1*coupling2
              counter[weight2]   -= coupling1*coupling2
              counter[weightint] += coupling1*coupling2

            factors.append([
                            (weightname, couplingsq)
                                  for weightname, couplingsq in counter.iteritems()
                                   if couplingsq
                                         and weightname is not None
                           ])

        assert factors
        return factors

    @property
    def weight_terms_expanded(self):
      factors = self.weight_terms
      result = []
      for individualfactors in cartesianproduct(*factors):
        result.append(("*".join(weightname for weightname, multiplier in individualfactors), product(multiplier for weightname, multiplier in individualfactors)))
      return result


    @property
    def samplesandfactors(self):
      return ExtendedCounter({self: 1})
