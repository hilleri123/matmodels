
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import NewType, List, Callable
import math

F_g = 9.8

def F_c(v: float, h: float):
    return 0

@dataclass
class RocketStage:
    G: float = 1
    uG: float = 1
    M_fuel: float = 0
    M_const: float = 0

    def max_time(self) -> float:
        return self.M_fuel * self.uG * F_g / self.G

RocketStageType = NewType('RocketStageType', RocketStage)

    
@dataclass
class RocketParams:
    M_const: float = 0
    v_start: float = 100
    stages: List[RocketStageType] = field(default_factory=list)

    def M(self, t:float) -> float:
        t_tmp = t
        m = self.M_const
        for stage in self.stages:
            t_max = stage.max_time()
            if t_tmp > t_max:
                pass
            elif t_tmp < 0:
                m += stage.M_const + stage.M_fuel 
            else:
                m += stage.M_const + stage.M_fuel - stage.G * t_tmp / stage.uG / F_g
            t_tmp -= t_max
        return m

RocketParamsType = NewType('RocketStageType', RocketStage)

class Rocket:
    def __init__(self, params: RocketParamsType = None, angle_func: Callable[[float], float] = lambda _: 0.):
        self._max_times = np.zeros(0)
        self._calcs = pd.DataFrame({"v":np.zeros(0),"m":np.zeros(0),"h":np.zeros(0),"x":np.zeros(0),"angle":np.zeros(0)})
        self.set_params(params)
        self.set_angle_func(angle_func)

    def set_params(self, params: RocketParamsType) -> None:
        self._params = params
        self.__calc_time()

    def __calc_time(self) -> None:
        self._max_times = np.zeros(len(self._params.stages))
        for idx, stage in enumerate(self._params.stages):
            self._max_times[idx] = stage.max_time()
        
    def set_angle_func(self, func : Callable[[float], float]) -> None:
        self._angle_func = func

    def curr_stage(self, t:float) -> RocketStageType:
        tmp_t = t
        for idx, max_time in enumerate(self._max_times):
            tmp_t -= max_time
            if tmp_t < 0:
                break
        else:
            return None #?
        return self._params.stages[idx]

    def calc(self, step: float = 1, after: float = 0) -> None:
        if self._params is None:
            raise RuntimeError("Rocket is undefined")
        self._step = step
        all_time = sum(self._max_times) + after
        steps = int(all_time / step)
        self._calcs[self._calcs.columns] = np.zeros((steps, self._calcs.shape[1]))
        self._calcs['v'][0] = self._params.v_start
        for idx, t in enumerate(np.arange(0, all_time, step)):
            stage = self.curr_stage(t)
            self._calcs['m'][idx] = self._params.M(t) #Не самое оптимальное решение, но мне плевать

            prev = self._calcs.iloc[idx-1 if idx-1 >= 0 else 0] #Предыдущие значения

            self._calcs['x'][idx] = prev['x'] + prev['v']*math.sin(prev['angle'])
            self._calcs['h'][idx] = prev['h'] + prev['v']*math.cos(prev['angle'])

            if stage is not None:
                G = stage.G
            else:
                G = 0
            self._calcs['v'][idx] = prev['v'] + G - F_c(v=prev['v'], h=prev['h']) - F_g*math.cos(prev['angle'])


        print(self._calcs)




