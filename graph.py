
from PyQt5.QtWidgets import QWizard, QWizardPage, QHBoxLayout, QVBoxLayout
from typing import NewType, List, Any
import numpy as np
import numpy.typing as npt
import matplotlib.backends.qt_compat
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class Calculable:
    def set_params(self, params: Any) -> None:
        pass


    def calc(self, step: float = 1, after: float = 0) -> None:
        pass


    def axis(self) -> List[str]:
        pass


    def get_axis(self, axis: str) -> npt.ArrayLike:
        pass


CalculableType = NewType('CalculableType', Calculable)


class Graph(QWizardPage):
    def __init__(self, calc: CalculableType,  *args, **kwargs):
        super(QWizardPage, self).__init__(*args, **kwargs)
        self._calc = calc
        main_layout = QHBoxLayout(self)
        self.setLayout(main_layout)
        self._params_layout = QVBoxLayout(self)
        main_layout.addLayout(self._params_layout)
        
        self._canvas = FigureCanvas(Figure(figsize=(5, 3)))
        main_layout.addWidget(self._canvas)
        main_layout.addWidget(NavigationToolbar(self._canvas, self))


    def update_graph(self) -> None:


class Graphs(QWizard):
    def __init__(self, calcs: List[CalculableType] = None, *args, **kwargs):
        super(QWizard, self).__init__(*args, **kwargs)
        if not calcs is None:
            register_calculables(calcs)


    def register_calculables(self, calcs: List[CalculableType]) -> None:
        last = max(self.pageIds())+1 if len(self.pageIds()) > 0 else 0
        for idx, calc in enumerate(calcs):
            self.setPage(last+idx, Graph(calc))


