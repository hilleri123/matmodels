
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStyle, QScrollArea, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
import numpy as np
import numpy.typing as npt
from typing import List, NewType, Any
import sip
import re
import math

from rocket import RocketParams, RocketParamsType, RocketStage, RocketStageType, Rocket, RocketStatus
from economy import Economy, EconomyParams, EconomyParamsType
from common import MyLineEdit, replace_params, replace_math_functions


class ParamsWidget(QWidget):
    text_changed_sig = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)


    def set_params(self, params: Any) -> None:
        pass


    def params(self) -> Any:
        pass


ParamsWidgetType = NewType('ParamsWidgetType', ParamsWidget)


def create_params_widget(cls: Any, *args, **kwargs) -> ParamsWidgetType:
    if cls is Rocket:
        return RocketParamsWidget(*args, **kwargs)
    if cls is Economy:
        return EconomyWidget(*args, **kwargs)
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


def default_economy_params() -> EconomyParamsType:
    params = EconomyParams(S_a=1, S_b=2, D_a=3, D_b=4, y_per_t=1, p_0=11, d=0.01)
    return params


class StageWidget(QWidget):
    delete_me = pyqtSignal()
    text_changed_sig = pyqtSignal()
    def __init__(self, stage: RocketStageType, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        self._stage = stage
        main_layout = QVBoxLayout(self)

        label = QLabel(self._stage.name, self)
        self._delete = QPushButton(self.style().standardIcon(QStyle.SP_BrowserStop), '', self)
        self._delete.clicked.connect(self.delete_me)
        label.setBuddy(self._delete)
        main_layout.addWidget(self._delete)

        LineEditType = NewType('LineEditType', MyLineEdit)

        def beautify_lineedit(line: LineEditType, name:str) -> None:
            line.textChanged.connect(self.text_changed_sig)
            layout = QHBoxLayout()
            label = QLabel(name)
            label.setBuddy(line)
            layout.addWidget(label)
            layout.addWidget(line)
            main_layout.addLayout(layout)

        self._G = MyLineEdit(1, self._stage.G)
        beautify_lineedit(self._G, 'G')

        self._uG = MyLineEdit(1, self._stage.uG)
        beautify_lineedit(self._uG, 'uG')

        self._M_fuel = MyLineEdit(0, self._stage.M_fuel)
        beautify_lineedit(self._M_fuel, 'M_fuel')

        self._M_const = MyLineEdit(0, self._stage.M_const)
        beautify_lineedit(self._M_const, 'M_const')

    def params(self) -> RocketStageType:
        return RocketStage(
                G = float(self._G.text()),
                uG = float(self._uG.text()),
                M_fuel = float(self._M_fuel.text()),
                M_const = float(self._M_const.text())
                )


class RocketParamsWidget(ParamsWidget):
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        layout = QHBoxLayout()
        self._M_const = MyLineEdit(1)
        self._M_const.textChanged.connect(self.text_changed_sig)
        label = QLabel('M_const', self)
        label.setBuddy(self._M_const)
        layout.addWidget(label)
        layout.addWidget(self._M_const)
        main_layout.addLayout(layout)

        layout = QHBoxLayout()
        self._v_start = MyLineEdit(0)
        self._v_start.textChanged.connect(self.text_changed_sig)
        label = QLabel('v_start', self)
        label.setBuddy(self._v_start)
        layout.addWidget(label)
        layout.addWidget(self._v_start)
        main_layout.addLayout(layout)

        layout = QHBoxLayout()
        self._angle_func = QLineEdit()
        self._angle_func.setText(r'angle + 0.08 if h > 10 and angle < atan(1)*2 else angle')
        self._angle_func.textChanged.connect(self.text_changed_sig)
        label = QLabel('angle_func(t, m, x, h, angle, v) =', self)
        label.setBuddy(self._angle_func)
        layout.addWidget(label)
        layout.addWidget(self._angle_func)
        main_layout.addLayout(layout)

        self._add_button = QPushButton("add stage")
        self._add_button.clicked.connect(self.__add_stage)
        main_layout.addWidget(self._add_button)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        w = QWidget()
        scroll_area.setWidget(w)
        self._stage_layout = QVBoxLayout()
        w.setLayout(self._stage_layout)
        main_layout.addWidget(scroll_area)

        self.set_params(default_rocket_params())
        self.resize(self.minimumSizeHint())
        #self.adjustSize()


    def set_params(self, rocket_params: RocketParamsType) -> None:
        self._rocket_params = rocket_params
        self._M_const.setText(str(self._rocket_params.M_const))
        self._v_start.setText(str(self._rocket_params.v_start))

        for i in range(self._stage_layout.count()-1, -1, -1):
            item = self._stage_layout.itemAt(i)
            self._stage_layout.removeWidget(item)
            sip.delete(item)

        for stage in self._rocket_params.stages:
            self.__add_stage(stage)


    def params(self) -> RocketParamsType:
        r = RocketParams(
                M_const = float(self._M_const.text()),
                v_start = float(self._v_start.text()),
                angle_func = eval(self.__func_text())
                )

        for i in range(self._stage_layout.count()):
            item = self._stage_layout.itemAt(i).widget()
            r.stages.append(item.params())
        return r


    def __add_stage(self, stage: RocketStageType = RocketStage()) -> None:
        if not stage.__class__ is RocketStage: #Conncet to signal(bool) :(
            stage = RocketStage() 
        new_stage = StageWidget(stage)
        new_stage.delete_me.connect(self.__remove_stage)
        new_stage.text_changed_sig.connect(self.text_changed_sig)
        self._stage_layout.addWidget(new_stage)


    def __remove_stage(self) -> None:
        sender = self.sender()
        self._stage_layout.removeWidget(sender)
        sip.delete(sender)
        

    def __func_text(self) -> str:
        res = self._angle_func.text()
        res = replace_math_functions(res)
        res = replace_params(res, 'x', RocketStatus)
        return f'lambda x : {res}'


class EconomyWidget(ParamsWidget):
    def __init__(self, *args, **kwargs):
        super(ParamsWidget, self).__init__(*args, **kwargs)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self._fields = {}
        for field in EconomyParams().__dataclass_fields__.keys():
            layout = QHBoxLayout()
            self._fields[field] = MyLineEdit(1)
            self._fields[field].textChanged.connect(self.text_changed_sig)
            label = QLabel(field, self)
            label.setBuddy(self._fields[field])
            layout.addWidget(label)
            layout.addWidget(self._fields[field])
            main_layout.addLayout(layout)
        self.set_params(default_economy_params())


    def set_params(self, params: EconomyParamsType) -> None:
        for field_n, field in self._fields.items():
            val = eval('params.' + field_n)
            field.setText(str(val))


    def params(self) -> EconomyParamsType:
        args = {field_n : float(field.text()) for field_n, field in self._fields.items()}
        return EconomyParams(**args)
