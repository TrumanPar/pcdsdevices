from pydm import Display
from os import path
from typhos import utils

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

        def _update_pseudos(*args, **kwargs):
            try:
                v = self.device.xwidth.position
                self.ui.XWidth_RBV.setText(str(f"{v:.5f}"))
            except Exception as e:
                print(f"Error updating xwidth: {e}")
            try:
                v = self.device.ywidth.position
                self.ui.YWidth_RBV.setText(str(f"{v:.5f}"))
            except Exception as e:
                print(f"Error updating ywidth: {e}")
            try:
                v = self.device.xcenter.position
                self.ui.XCenter_RBV.setText(str(f"{v:.5f}"))
            except Exception as e:
                print(f"Error updating xcenter: {e}")
            try:
                v = self.device.ycenter.position
                self.ui.YCenter_RBV.setText(str(f"{v:.5f}"))
            except Exception as e:
                print(f"Error updating ycenter: {e}")

        # Subscribe all real axes to update widgets with pseudo readbacks
        for motor in [self.device.top, self.device.bottom, self.device.north, self.device.south]:
            motor.user_readback.subscribe(_update_pseudos, run=False)

        # Seed the initial value
        _update_pseudos()

        # Link the calibrate cpt to the ready widget, and VAL widget's enabled bits
        self.ui.READY_INDICATOR.value = self.device.calibrated

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
        top_pv = self.device.top.prefix
        bottom_pv = self.device.bottom.prefix
        north_pv = self.device.north.prefix
        south_pv = self.device.south.prefix

        # Set up the shell commands for each motor button
        self.ui.TOP_EXPERT.commands = [f"typhos \"pcdsdevices.smaract.SmarAct[{{'prefix':'{top_pv}','name':'{self.device.name}_bottom'}}]\""]
        self.ui.BOTTOM_EXPERT.commands = [f"typhos \"pcdsdevices.smaract.SmarAct[{{'prefix':'{bottom_pv}','name':'{self.device.name}_bottom'}}]\""]
        self.ui.NORTH_EXPERT.commands = [f"typhos \"pcdsdevices.smaract.SmarAct[{{'prefix':'{north_pv}','name':'{self.device.name}_north'}}]\""]
        self.ui.SOUTH_EXPERT.commands = [f"typhos \"pcdsdevices.smaract.SmarAct[{{'prefix':'{south_pv}','name':'{self.device.name}_south'}}]\""]
