
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import NewType, List, Callable

F_g = 9.8

@dataclass
class RocketStage:
    G: float
    uG: float
    M_fuel: float
    M_const: float

    def max_time(self) -> float:
        return stage.M_fuel * stage.uG * F_g / stage.G

RocketStageType = NewType('RocketStageType', RocketStage)

    
@dataclass
class RocketParams:
    M_const: float
    stages: List[RocketStageType] = field(default_factory=list)
RocketParamsType = NewType('RocketStageType', RocketStage)

class Rocket:
    def __init__(self, params: RocketParamsType = None, angle_func: Callable[float, float] = lambda _: 0.):
        self._max_times = np.zeros(0)
        self._calcs = pd.DataFrame({"v":np.zeros(0),"m":np.zeros(0),"h":np.zeros(0),"x":np.zeros(0),"angle":np.zeros(0)})
        if params is not None:
            self.set_params(params)
        self.set_angle_func(angle_func)

    def set_params(self, params: RocketParamsType) -> None:
        self._params = params
        self.__calc_time()

    def __calc_time(self) -> None:
        self._max_times = np.zeros(len(_params.stages))
        for idx, stage in enumerate(_params.stages):
            self._max_times[idx] = stage.max_time()
        
    def set_angle_func(self, func : Callable[float, float]) -> None:
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

    def calc(self, step = 1) -> None:


