from typing import List, Any, NewType, ClassVar, Dict
from typing_extensions import Protocol
from dataclasses import dataclass
import numpy.typing as npt
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QDoubleValidator
import re
import math
import matplotlib.pyplot as plt

class IsDataclass(Protocol):
    __dataclass_fields__: ClassVar[Dict] 


class Calculable:
    def set_params(self, params: Any) -> None:
        pass


    def calc(self, step: float = 1, after: float = 0) -> None:
        pass


    def axis(self) -> List[str]:
        pass


    def get_axis(self, axis: str) -> npt.ArrayLike:
        pass


    def title(self) -> str:
        return 'Title'


    def plot(self, ax: plt.Axes, y: str, x: str) -> None:
        ax.set_ylabel(y)
        ax.set_xlabel(x)
        ax.set_title(f'{y}({x})')
        ax.plot(self.get_axis(x), self.get_axis(y))


CalculableType = NewType('CalculableType', Calculable)


class MyLineEdit(QLineEdit):
    def __init__(self, starts: float = 0, value: float = 0, *args, **kwargs):
        super(QLineEdit, self).__init__(*args, **kwargs)
        val = QDoubleValidator()
        val.setBottom(starts)
        self.setValidator(val)
        self.setText(str(value))


_symbols = r'[\s+\-*/<>=%&|\(\)]'

def replace_math_functions(text: str) -> str:
    text = f' {text} '
    for math_func in dir(math):
        if '__' in math_func:
            continue
        text = re.sub(f'({_symbols})((math\.)?{math_func})({_symbols})', f'\\1math.{math_func}\\4', text)
    return text

        
def replace_params(text: str, params_name: str, params: IsDataclass) -> str:
    text = f' {text} '
    for param in dir(params):
        if '__' in param:
            continue
        text = re.sub(f'({_symbols})(({params_name}\.)?{param})({_symbols})', f'\\1{params_name}.{param}\\4', text)
    return text



