import logging
import sys
import time

import numpy as np

from pyk4a import PyK4A
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont, QImage, QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)