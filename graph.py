
from PyQt5.QtWidgets import QWizard, QWizardPage, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt
from typing import NewType, List, Any
import numpy as np
import numpy.typing as npt
import matplotlib.backends.qt_compat
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from params import create_params_widget
from common import Calculable, CalculableType, MyLineEdit



class Graph(QWizardPage):
    #something_changed_sig = pyqtSignal()
    def __init__(self, calc: CalculableType,  *args, **kwargs):
        super(QWizardPage, self).__init__(*args, **kwargs)
        #self.something_changed_sig.connect(self.__something_changed)
        self._need_to_recalc = True
        self._calc = calc
        self._ax = None
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        layout = QHBoxLayout()
        self._params = create_params_widget(calc.__class__, self)
        if not self._params is None:
            layout.addWidget(self._params)
        
        tmp_layout = QVBoxLayout()
        self._canvas = FigureCanvas(Figure(figsize=(5, 3)))
        tmp_layout.addWidget(self._canvas)
        tmp_layout.addWidget(NavigationToolbar(self._canvas, self))
        layout.addLayout(tmp_layout)
        main_layout.addLayout(layout)

        layout = QHBoxLayout()
        label = QLabel('t_step')
        layout.addWidget(label)
        self._t_step = MyLineEdit(0.000001, 0.1)
        self._t_step.textChanged.connect(self.__something_changed)
        label.setBuddy(self._t_step)
        layout.addWidget(self._t_step)

        label = QLabel('t_after')
        layout.addWidget(label)
        self._t_after = MyLineEdit(0, 0)
        self._t_after.textChanged.connect(self.__something_changed)
        label.setBuddy(self._t_after)
        layout.addWidget(self._t_after)

        self._axis = self._calc.axis()

        label = QLabel('x')
        layout.addWidget(label)
        self._x = QComboBox()
        self._x.activated.connect(self.__combo)
        self._x.addItems(self._axis)
        label.setBuddy(self._x)
        layout.addWidget(self._x)

        label = QLabel('y')
        layout.addWidget(label)
        self._y = QComboBox()
        self._y.activated.connect(self.__combo)
        self._y.addItems(self._axis)
        if len(self._axis) > 1:
            self._y.setCurrentIndex(1)
        label.setBuddy(self._y)
        layout.addWidget(self._y)

        main_layout.addLayout(layout)
        self.__combo()
        self.setTitle(self._calc.title())


    def __combo(self) -> None:
        sender = self.sender()
        master = self._x
        slave = self._y

        def clear_disable(combobox):
            model = combobox.model()
            for i in range(model.rowCount()):
                model.item(i).setEnabled(True)
        #clear_disable(self._x)
        #clear_disable(self._y)

        if not sender is None:
            if self._y is sender:
                master = self._y
                slave = self._x
        clear_disable(slave)

        idx = master.currentIndex()
        model = slave.model()
        model.item(idx).setEnabled(False)

    
    def calc_graph(self) -> None:
        self._calc.set_params(self._params.params())
        self._calc.calc(float(self._t_step.text()), float(self._t_after.text()))
        self._need_to_recalc = False
        self.setTitle(self._calc.title())


    def plot_graph(self) -> None:
        if self._need_to_recalc:
            self.calc_graph()
        if self._ax is None:
            self._ax = self._canvas.figure.subplots()
        else:
            self._ax.clear()
        y = self._y.currentText()
        x = self._x.currentText()
        self._calc.plot(self._ax, y, x)
        self._canvas.draw()


    def __something_changed(self) -> None:
        self._need_to_recalc = True
        self.setTitle(self._calc.title()+'*')


class Graphs(QWizard):
    def __init__(self, calcs: List[CalculableType] = None, *args, **kwargs):
        super(QWizard, self).__init__(*args, **kwargs)
        if not calcs is None:
            register_calculables(calcs)
        self.setButtonLayout([QWizard.BackButton, QWizard.NextButton, QWizard.CustomButton1])
        self.setButtonText(QWizard.CustomButton1, 'Plot')
        self.button(QWizard.CustomButton1).clicked.connect(self.plot_graph)


    def register_calculables(self, calcs: List[CalculableType]) -> None:
        last = max(self.pageIds())+1 if len(self.pageIds()) > 0 else 0
        for idx, calc in enumerate(calcs):
            self.setPage(last+idx, Graph(calc))

    
    def plot_graph(self) -> None:
        self.currentPage().plot_graph()




