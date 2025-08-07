import pydm
import re

from pydm import Display
from os import path

from pydm.widgets import PyDMEmbeddedDisplay
from qtpy import QtCore, QtWidgets
from typhos import utils
from epics import PV, camonitor, caget

class SmaractSlitsDetailedWidget(Display, utils.TyphosBase):
    """
    Custom widget for managing the pdu detailed screen
    """

    def __init__(self, parent=None, ui_filename='SmaractSlits.detailed.ui', macros=None, **kwargs):
        super().__init__(parent=parent, ui_filename=ui_filename, macros=macros, **kwargs)

    @property
    def device(self):
        """The associated device."""
        try:
            return self.devices[0]
        except Exception:
            ...

    def add_device(self, device):
        """Typhos hook for adding a new device."""
        super().add_device(device)
