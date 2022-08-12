"""
Adaptado del módulo pySerial.
https://pyserial.readthedocs.io/en/latest/tools.html
(C) 2011-2015 Chris Liechti <cliechti@gmx.net>
 
SPDX-License-Identifier:    BSD-3-Clause
"""
import os
import re

# chose an implementation, depending on os
#~ if sys.platform == 'cli':
#~ else:
if os.name == 'nt':  # sys.platform == 'win32':
    from serial.tools.list_ports_windows import comports
elif os.name == 'posix':
    from serial.tools.list_ports_posix import comports
#~ elif os.name == 'java':
else:
    raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def buscar_puerto(regexp, include_links=False):
    """\
    Search for ports using a regular expression. Port name, description and
    hardware ID are searched. The function returns the port.
    """
    r = re.compile(regexp, re.I)
    for info in comports(include_links):
        port, desc, hwid = info
        if r.search(port) or r.search(desc) or r.search(hwid):
            return port
        else:
            return None