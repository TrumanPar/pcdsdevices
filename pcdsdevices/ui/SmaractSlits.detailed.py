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

        # Link the callibrate cpt to the ready widget, and VAL widget's enabled bits
        self.ui.READY_INDICATOR.enabled = self.device.calibrated

        self.ui.TOP_VAL.enabled = self.device.calibrated
        self.ui.BOTTOM_VAL.enabled = self.device.calibrated
        self.ui.NORTH_VAL.enabled = self.device.calibrated
        self.ui.SOUTH_VAL.enabled = self.device.calibrated

        self.ui.XCenter_REQ.enabled = self.device.calibrated
        self.ui.YCenter_REQ.enabled = self.device.calibrated
        self.ui.XWidth_REQ.enabled = self.device.calibrated
        self.ui.YWidth_REQ.enabled = self.device.calibrated

        # Set the expert screen buttons
        # Build the actual PV names using the device's prefix and PV attributes
        top_pv = f"{self.device.prefix}{self.device._top_pv}"
        bottom_pv = f"{self.device.prefix}{self.device._bottom_pv}"
        north_pv = f"{self.device.prefix}{self.device._north_pv}"
        south_pv = f"{self.device.prefix}{self.device._south_pv}"

        # Set up the shell commands for each motor button
        self.ui.TOP_EXPERT.command = f"typhos \"pcdsdevices.smaract.SmarAct[{{'prefix':'{top_pv}','name':'{self.device.name}_top'}}]\""
        self.ui.BOTTOM_EXPERT.command = f"typhos \"pcdsdevices.smaract.SmarAct[{{'prefix':'{bottom_pv}','name':'{self.device.name}_bottom'}}]\""
        self.ui.NORTH_EXPERT.command = f"typhos \"pcdsdevices.smaract.SmarAct[{{'prefix':'{north_pv}','name':'{self.device.name}_north'}}]\""
        self.ui.SOUTH_EXPERT.command = f"typhos \"pcdsdevices.smaract.SmarAct[{{'prefix':'{south_pv}','name':'{self.device.name}_south'}}]\""