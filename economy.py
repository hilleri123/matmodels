
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import NewType, List, Callable
import math
import numpy.typing as npt
import matplotlib.pyplot as plt

from common import Calculable, CalculableType


@dataclass
class EconomyParams:
    S_b: float = 1
    S_a: float = 1
    D_b: float = 1
    D_a: float = 1
    y_per_t: float = 1
    p_0: float = 1
    d: float = 0.01

    
    def y(self, time_step: float = 1):
        return self.y_per_t * time_step


    def a(self) -> float:
        return self.p_0 - self.p_ideal


    def p_ideal(self) -> float:
        return (self.D_a - self.S_a) / (self.D_b + self.S_b)


EconomyParamsType = NewType('EconomyParamsType', EconomyParams)


class Economy(Calculable):
    S_D = 'S_D'
    def __init__(self, params: EconomyParamsType = EconomyParams()):
        self._calcs = pd.DataFrame({"t":np.zeros(0),"S":np.zeros(0),"D":np.zeros(0),"p":np.zeros(0)})
        self.set_params(params)


    def set_params(self, params: EconomyParamsType) -> None:
        self._params = params


    def calc(self, step: float = 1, after: float = 0) -> None:
        if self._params is None:
            raise RuntimeError("Economy is undefined")
        self._step = step
        max_time = (math.log(self._params.d)-math.log(self._params.p_0))/(-self._params.S_a - self._params.D_a)
        all_time = max_time + after
        steps = int(all_time / step) + 1
        self._calcs = pd.DataFrame({"t":np.zeros(0),"S":np.zeros(0),"D":np.zeros(0),"p":np.zeros(0, dtype=float)})
        self._calcs[self._calcs.columns] = np.zeros((steps, self._calcs.shape[1]))
        self._calcs['p'] = self._params.p_0
        self._calcs['t'] = np.arange(0, all_time, step)
        for idx, t in enumerate(self._calcs['t']):
            prev = self._calcs.iloc[idx-1 if idx-1 >= 0 else 0] #Предыдущие значения
            self._calcs.loc[idx, 'S'] = self._params.S_a * prev['p'] + self._params.S_b
            self._calcs.loc[idx, 'D'] = self._params.D_b - self._params.D_a * prev['p']
            self._calcs.loc[idx, 'p'] = prev['p'] + self._params.y(step) * (prev['D'] - prev['S'])
            print(dict(prev), dict(self._calcs.iloc[idx]), prev['p'] + self._params.y(step) * (prev['D'] - prev['S']), self._params.y(step) * (prev['D'] - prev['S']))
            
        print(self._calcs)


    def axis(self) -> List[str]:
        return list(self._calcs) + [self.S_D]


    def get_axis(self, axis: str) -> npt.ArrayLike:
        if axis == self.S_D:
            return np.concatenate([self._calcs['S'], self._calcs['D']])
        return self._calcs[axis]


    def title(self) -> str:
        return 'Economy'


    def plot(self, ax: plt.Axes, y: str, x: str) -> None:
        if y == self.S_D:
            super().plot(ax, 'S', x)
            super().plot(ax, 'D', x)
        elif x == self.S_D:
            super().plot(ax, y, 'S')
            super().plot(ax, y, 'D')
        else:
            super().plot(ax, y, x)

        if x == 'p':
            tmp = self.get_axis(y)
            ymin = tmp.min()
            ymax = tmp.max()
            ax.vlines(x = self._params.p_ideal(), ymin = ymin, ymax = ymax, colors = 'red')
        elif y == 'p':
            tmp = self.get_axis(x)
            xmin = tmp.min()
            xmax = tmp.max()
            ax.hlines(y = self._params.p_ideal(), xmin = xmin, xmax = xmax, colors = 'red')
