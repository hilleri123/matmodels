from typing import List, Any, NewType
import numpy.typing as npt
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QDoubleValidator

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


CalculableType = NewType('CalculableType', Calculable)


class MyLineEdit(QLineEdit):
    def __init__(self, starts: float = 0, value: float = 0, *args, **kwargs):
        super(QLineEdit, self).__init__(*args, **kwargs)
        val = QDoubleValidator()
        val.setBottom(starts)
        self.setValidator(val)
        self.setText(str(value))


