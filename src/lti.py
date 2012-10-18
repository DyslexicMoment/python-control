"""lti.py

The lti module contains the Lti parent class to the child classes StateSpace and
TransferFunction.  It is designed for use in the python-control library.

Routines in this module:

Lti.__init__
isdtime()
isctime()
timebase()
timebaseEqual()
"""

from types import NoneType

class Lti:

    """Lti is a parent class to linear time invariant control (LTI) objects.
    
    Lti is the parent to the StateSpace and TransferFunction child
    classes. It contains the number of inputs and outputs, and the
    timebase (dt) for the system.

    The timebase for the system, dt, is used to specify whether the
    system is operating in continuous or discrete time.  It can have
    the following values:

      * dt = None       No timebase specified
      * dt = 0          Continuous time system
      * dt > 0          Discrete time system with sampling time dt
      * dt = True       Discrete time system with unspecified sampling time

    When to Lti systems are combined, there timebases much match.  A system
    with timebase None can be combined with a system having a specified
    timebase, and the result will have the timebase of the latter system.

    The StateSpace and TransferFunction child classes contain several common
    "virtual" functions.  These are:

    __init__
    copy
    __str__
    __neg__
    __add__
    __radd__
    __sub__
    __rsub__
    __mul__
    __rmul__
    __div__
    __rdiv__
    evalfr
    freqresp
    pole
    zero
    feedback
    returnScipySignalLti
    
    """
    
    def __init__(self, inputs=1, outputs=1, dt=None):
        """Assign the LTI object's numbers of inputs and ouputs."""

        # Data members common to StateSpace and TransferFunction.
        self.inputs = inputs
        self.outputs = outputs
        self.dt = dt

# Return the timebase (with conversion if unspecified)
def timebase(sys, strict=True):
    """Return the timebase for an Lti system

    dt = timebase(sys)

    returns the timebase for a system 'sys'.  If the strict option is
    set to False, dt = True will be returned as 1.
    """
    # System needs to be either a constant or an Lti system
    if isinstance(sys, (int, float, long, complex)):
        return None
    elif not isinstance(sys, Lti):
        raise ValueError("Timebase not defined")

    # Return the dample time, with converstion to float if strict is false
    if (sys.dt == None):
        return None
    elif (strict):
        return float(sys.dt)

    return sys.dt

# Check to see if two timebases are equal
def timebaseEqual(sys1, sys2):
    # TODO: add docstring
    if (type(sys1.dt) == bool or type(sys2.dt) == bool):
        # Make sure both are unspecified discrete timebases
        return type(sys1.dt) == type(sys2.dt) and sys1.dt == sys2.dt
    elif (type(sys1.dt) == NoneType or type(sys2.dt) == NoneType):
        # One or the other is unspecified => the other can be anything
        return True
    else:
        return sys1.dt == sys2.dt

# Check to see if a system is a discrete time system
def isdtime(sys, strict=False):
    # TODO: add docstring
    # Check to see if this is a constant
    if isinstance(sys, (int, float, long, complex)):
        # OK as long as strict checking is off
        return True if not strict else False

    # Check for a transfer fucntion or state space object
    if isinstance(sys, Lti):
        # Look for dt > 0 or dt == None (if not strict)
        # Note that dt = True will be checked by dt > 0
        return sys.dt > 0 or (not strict and sys.dt == None)

    # Got possed something we don't recognize
    return False

# Check to see if a system is a continuous time system
def isctime(sys, strict=False):
    # TODO: add docstring
    # Check to see if this is a constant
    if isinstance(sys, (int, float, long, complex)):
        # OK as long as strict checking is off
        return True if not strict else False

    # Check for a transfer fucntion or state space object
    if isinstance(sys, Lti):
        # Look for dt == 0 or dt == None (if not strict)
        return sys.dt == 0 or (not strict and sys.dt == None)

    # Got possed something we don't recognize
    return False
