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

    def __init__(self, parent=None, ui_filename='SmaractSlits.detailed.ui', **kwargs):
        super().__init__(parent=parent, ui_filename=ui_filename)

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
        self.post_typhos_init()

    def post_typhos_init(self):
        """
        Once typhos has relinked the device and parent widget, we need to clean
        Up some of the signals and maybe add new widgets to the display.
        Add any other init-esque shenanigans you need here.
        """
        self.fix_pvs()
        self.add_channels()


    def fix_pvs(self):
        """
        Reconnect PyDM widgets to the actual PVs from the device object.
        This is necessary because the macros aren't expanded during UI parsing.
        """

        # Slits pseudopositioners
        xwidth_rbv = self.ui.findChild(pydm.widgets.label.PyDMLabel, "XWidth_RBV")
        xwidth_rbv.setReadOnly(True)
        xwidth_req = self.ui.findChild(pydm.widgets.line_edit.PyDMLineEdit, "XWidth_REQ")

        ywidth_rbv = self.ui.findChild(pydm.widgets.label.PyDMLabel, "YWidth_RBV")
        ywidth_rbv.setReadOnly(True)
        ywidth_req = self.ui.findChild(pydm.widgets.line_edit.PyDMLineEdit, "YWidth_REQ")

        xcenter_rbv = self.ui.findChild(pydm.widgets.label.PyDMLabel, "XCenter_RBV")
        xcenter_rbv.setReadOnly(True)
        xcenter_req = self.ui.findChild(pydm.widgets.line_edit.PyDMLineEdit, "XCenter_REQ")

        ycenter_rbv = self.ui.findChild(pydm.widgets.label.PyDMLabel, "YCenter_RBV")
        ycenter_rbv.setReadOnly(True)
        ycenter_req = self.ui.findChild(pydm.widgets.line_edit.PyDMLineEdit, "YCenter_REQ")

        # Motor stages
        top_motor_lls = self.ui.findChild(pydm.widgets.byte.PyDMByteIndicator, "TOP_LLS")
        top_motor_hls = self.ui.findChild(pydm.widgets.byte.PyDMByteIndicator, "TOP_HLS")
        top_motor_rbv = self.ui.findChild(pydm.widgets.label.PyDMLabel, "TOP_RBV")
        top_motor_val = self.ui.findChild(pydm.widgets.line_edit.PyDMLineEdit, "TOP_VAL")
        top_motor_home = self.ui.findChild(pydm.widgets.pushbutton.PyDMPushButton, "TOP_HOME")
        top_motor_stop = self.ui.findChild(pydm.widgets.pushbutton.PyDMPushButton, "TOP_STOP")
        top_motor_expert = self.ui.findChild(pydm.widgets.shell_command.PyDMShellCommand, "TOP_EXPERT")
        top_motor_scale = self.ui.findChild(pydm.widgets.scale.PyDMScaleIndicator, "TOP_SCALE")

        bottom_motor_lls = self.ui.findChild(pydm.widgets.byte.PyDMByteIndicator, "BOTTOM_LLS")
        bottom_motor_hls = self.ui.findChild(pydm.widgets.byte.PyDMByteIndicator, "BOTTOM_HLS")
        bottom_motor_rbv = self.ui.findChild(pydm.widgets.label.PyDMLabel, "BOTTOM_RBV")
        bottom_motor_val = self.ui.findChild(pydm.widgets.line_edit.PyDMLineEdit, "BOTTOM_VAL")
        bottom_motor_home = self.ui.findChild(pydm.widgets.pushbutton.PyDMPushButton, "BOTTOM_HOME")
        bottom_motor_stop = self.ui.findChild(pydm.widgets.pushbutton.PyDMPushButton, "BOTTOM_STOP")
        bottom_motor_expert = self.ui.findChild(pydm.widgets.shell_command.PyDMShellCommand, "BOTTOM_EXPERT")
        bottom_motor_scale = self.ui.findChild(pydm.widgets.scale.PyDMScaleIndicator, "BOTTOM_SCALE")

        north_motor_lls = self.ui.findChild(pydm.widgets.byte.PyDMByteIndicator, "NORTH_LLS")
        north_motor_hls = self.ui.findChild(pydm.widgets.byte.PyDMByteIndicator, "NORTH_HLS")
        north_motor_rbv = self.ui.findChild(pydm.widgets.label.PyDMLabel, "NORTH_RBV")
        north_motor_val = self.ui.findChild(pydm.widgets.line_edit.PyDMLineEdit, "NORTH_VAL")
        north_motor_home = self.ui.findChild(pydm.widgets.pushbutton.PyDMPushButton, "NORTH_HOME")
        north_motor_stop = self.ui.findChild(pydm.widgets.pushbutton.PyDMPushButton, "NORTH_STOP")
        north_motor_expert = self.ui.findChild(pydm.widgets.shell_command.PyDMShellCommand, "NORTH_EXPERT")
        north_motor_scale = self.ui.findChild(pydm.widgets.scale.PyDMScaleIndicator, "NORTH_SCALE")

        south_motor_lls = self.ui.findChild(pydm.widgets.byte.PyDMByteIndicator, "SOUTH_LLS")
        south_motor_hls = self.ui.findChild(pydm.widgets.byte.PyDMByteIndicator, "SOUTH_HLS")
        south_motor_rbv = self.ui.findChild(pydm.widgets.label.PyDMLabel, "SOUTH_RBV")
        south_motor_val = self.ui.findChild(pydm.widgets.line_edit.PyDMLineEdit, "SOUTH_VAL")
        south_motor_home = self.ui.findChild(pydm.widgets.pushbutton.PyDMPushButton, "SOUTH_HOME")
        south_motor_stop = self.ui.findChild(pydm.widgets.pushbutton.PyDMPushButton, "SOUTH_STOP")
        south_motor_expert = self.ui.findChild(pydm.widgets.shell_command.PyDMShellCommand, "SOUTH_EXPERT")
        south_motor_scale = self.ui.findChild(pydm.widgets.scale.PyDMScaleIndicator, "SOUTH_SCALE")

         # Connect slit pseudopositioner readbacks (Python Signals)
        if xwidth_rbv:
            def update_xwidth_rbv(value):
                xwidth_rbv.setText(f"{value:.3f}")
            self.device.xwidth.readback.subscribe(update_xwidth_rbv)
            update_xwidth_rbv(self.device.xwidth.readback.get())

        if xwidth_req:
            def move_xwidth():
                try:
                    target = float(xwidth_req.text())
                    self.device.xwidth.move(target, wait=False)
                except (ValueError, AttributeError):
                    pass
            # Connect when user presses Enter
            xwidth_req.returnPressed.connect(move_xwidth)

        if ywidth_rbv:
            def update_ywidth_rbv(value):
                ywidth_rbv.setText(f"{value:.3f}")
            self.device.ywidth.readback.subscribe(update_ywidth_rbv)
            update_ywidth_rbv(self.device.ywidth.readback.get())

        if ywidth_req:
            def move_ywidth():
                try:
                    target = float(ywidth_req.text())
                    self.device.ywidth.move(target, wait=False)
                except (ValueError, AttributeError):
                    pass
            # Connect when user presses Enter
            ywidth_req.returnPressed.connect(move_ywidth)

        if xcenter_rbv:
            def update_xcenter_rbv(value):
                xcenter_rbv.setText(f"{value:.3f}")
            self.device.xcenter.readback.subscribe(update_xcenter_rbv)
            update_xcenter_rbv(self.device.xcenter.readback.get())

        if xcenter_req:
            def move_xcenter():
                try:
                    target = float(xcenter_req.text())
                    self.device.xcenter.move(target, wait=False)
                except (ValueError, AttributeError):
                    pass
            # Connect when user presses Enter
            xcenter_req.returnPressed.connect(move_xcenter)

        if ycenter_rbv:
            def update_ycenter_rbv(value):
                ycenter_rbv.setText(f"{value:.3f}")
            self.device.ycenter.readback.subscribe(update_ycenter_rbv)
            update_ycenter_rbv(self.device.ycenter.readback.get())

        if ycenter_req:
            def move_ycenter():
                try:
                    target = float(ycenter_req.text())
                    self.device.ycenter.move(target, wait=False)
                except (ValueError, AttributeError):
                    pass
            # Connect when user presses Enter
            ycenter_req.returnPressed.connect(move_ycenter)

        # Connect motor PVs (these use actual EPICS channels)
        if top_motor_lls:
            top_motor_lls.channel = f'ca://{self.device.top.prefix}:LLS'
        if top_motor_hls:
            top_motor_hls.channel = f'ca://{self.device.top.prefix}:HLS'
        if top_motor_rbv:
            top_motor_rbv.channel = f'ca://{self.device.top.prefix}.RBV'
        if top_motor_val:
            top_motor_val.channel = f'ca://{self.device.top.prefix}.VAL'
        if top_motor_home:
            top_motor_home.channel = f'ca://{self.device.top.prefix}:DO_CALIB.PROC'
        if top_motor_stop:
            top_motor_stop.channel = f'ca://{self.device.top.prefix}.STOP'
        if top_motor_scale:
            top_motor_scale.channel = f'ca://{self.device.top.prefix}.RBV'

        if bottom_motor_lls:
            bottom_motor_lls.channel = f'ca://{self.device.bottom.prefix}:LLS'
        if bottom_motor_hls:
            bottom_motor_hls.channel = f'ca://{self.device.bottom.prefix}:HLS'
        if bottom_motor_rbv:
            bottom_motor_rbv.channel = f'ca://{self.device.bottom.prefix}.RBV'
        if bottom_motor_val:
            bottom_motor_val.channel = f'ca://{self.device.bottom.prefix}.VAL'
        if bottom_motor_home:
            bottom_motor_home.channel = f'ca://{self.device.bottom.prefix}:DO_CALIB.PROC'
        if bottom_motor_stop:
            bottom_motor_stop.channel = f'ca://{self.device.bottom.prefix}.STOP'
        if bottom_motor_scale:
            bottom_motor_scale.channel = f'ca://{self.device.bottom.prefix}.RBV'

        if north_motor_lls:
            north_motor_lls.channel = f'ca://{self.device.north.prefix}:LLS'
        if north_motor_hls:
            north_motor_hls.channel = f'ca://{self.device.north.prefix}:HLS'
        if north_motor_rbv:
            north_motor_rbv.channel = f'ca://{self.device.north.prefix}.RBV'
        if north_motor_val:
            north_motor_val.channel = f'ca://{self.device.north.prefix}.VAL'
        if north_motor_home:
            north_motor_home.channel = f'ca://{self.device.north.prefix}:DO_CALIB.PROC'
        if north_motor_stop:
            north_motor_stop.channel = f'ca://{self.device.north.prefix}.STOP'
        if north_motor_scale:
            north_motor_scale.channel = f'ca://{self.device.north.prefix}.RBV'

        if south_motor_lls:
            south_motor_lls.channel = f'ca://{self.device.south.prefix}:LLS'
        if south_motor_hls:
            south_motor_hls.channel = f'ca://{self.device.south.prefix}:HLS'
        if south_motor_rbv:
            south_motor_rbv.channel = f'ca://{self.device.south.prefix}.RBV'
        if south_motor_val:
            south_motor_val.channel = f'ca://{self.device.south.prefix}.VAL'
        if south_motor_home:
            south_motor_home.channel = f'ca://{self.device.south.prefix}:DO_CALIB.PROC'
        if south_motor_stop:
            south_motor_stop.channel = f'ca://{self.device.south.prefix}.STOP'
        if south_motor_scale:
            south_motor_scale.channel = f'ca://{self.device.south.prefix}.RBV'
