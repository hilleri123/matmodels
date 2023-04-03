
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QDoubleValidator, QPushButton
import numpy as np
import numpy.typing as npt
from typing import List, NewType, Any

from rocket import RocketParams, RocketStage, Rocket


class ParamsWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)


    def set_params(self, params: Any) -> None:
        pass


    def params(self) -> Any:
        pass


ParamsWidgetType = NewType('ParamsWidgetType', ParamsWidget)


def create_params_widget(cls: Any, *args, **kwargs) -> ParamsWidgetType:
    if cls is Rocket:
        return RocketParamsWidget(args, kwargs)
    return None


def default_rocket_params() -> RocketParamsType:
    params = RocketParams(M_const = 9500, v_start = 1000)

    stage0 = RocketStage(G = 290000, uG = 320, M_fuel = 25000, M_const = 2500)
    stage1 = RocketStage(G = 800000, uG = 270, M_fuel = 100000, M_const = 5000)
    stage2 = RocketStage(G = 4000000, uG = 250, M_fuel = 170000, M_const = 7000)

    params.stages.append(stage0)
    params.stages.append(stage1)
    params.stages.append(stage2)
    return params


class RocketParamsWidget(ParamsWidget):
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        self._add_button = QPushButton("add stage")
        self.set_params(default_rocket_params)


    def set_params(self, params: RocketParamsType) -> None:
        self._params = params


    def params(self) -> RocketParamsType:
        pass


    def __add_stage(self) -> None:
        pass

