# Python stubs generated by omniidl from idl/inf1822.idl
# DO NOT EDIT THIS FILE!

import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA


_omnipy.checkVersion(4,2, __file__, 1)

try:
    property
except NameError:
    def property(*args):
        return None


#
# Start of module "INF1822"
#
__name__ = "INF1822"
_0_INF1822 = omniORB.openModule("INF1822", r"idl/inf1822.idl")
_0_INF1822__POA = omniORB.openModule("INF1822__POA", r"idl/inf1822.idl")


# interface Device
_0_INF1822._d_Device = (omniORB.tcInternal.tv_objref, "IDL:INF1822/Device:1.0", "Device")
omniORB.typeMapping["IDL:INF1822/Device:1.0"] = _0_INF1822._d_Device
_0_INF1822.Device = omniORB.newEmptyClass()
class Device :
    _NP_RepositoryId = _0_INF1822._d_Device[1]

    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")

    _nil = CORBA.Object._nil


_0_INF1822.Device = Device
_0_INF1822._tc_Device = omniORB.tcInternal.createTypeCode(_0_INF1822._d_Device)
omniORB.registerType(Device._NP_RepositoryId, _0_INF1822._d_Device, _0_INF1822._tc_Device)

# Device operations and attributes
Device._d__get_id = ((),(omniORB.tcInternal.tv_ulong,),None)
Device._d__set_id = ((omniORB.tcInternal.tv_ulong,),(),None)
Device._d__get_type = ((),((omniORB.tcInternal.tv_string,0),),None)
Device._d__set_type = (((omniORB.tcInternal.tv_string,0),),(),None)

# Device object reference
class _objref_Device (CORBA.Object):
    _NP_RepositoryId = Device._NP_RepositoryId

    def __init__(self, obj):
        CORBA.Object.__init__(self, obj)

    def _get_id(self, *args):
        return self._obj.invoke("_get_id", _0_INF1822.Device._d__get_id, args)

    def _set_id(self, *args):
        return self._obj.invoke("_set_id", _0_INF1822.Device._d__set_id, args)

    id = property(_get_id, _set_id)


    def _get_type(self, *args):
        return self._obj.invoke("_get_type", _0_INF1822.Device._d__get_type, args)

    def _set_type(self, *args):
        return self._obj.invoke("_set_type", _0_INF1822.Device._d__set_type, args)

    type = property(_get_type, _set_type)


omniORB.registerObjref(Device._NP_RepositoryId, _objref_Device)
_0_INF1822._objref_Device = _objref_Device
del Device, _objref_Device

# Device skeleton
__name__ = "INF1822__POA"
class Device (PortableServer.Servant):
    _NP_RepositoryId = _0_INF1822.Device._NP_RepositoryId


    _omni_op_d = {"_get_id": _0_INF1822.Device._d__get_id, "_set_id": _0_INF1822.Device._d__set_id, "_get_type": _0_INF1822.Device._d__get_type, "_set_type": _0_INF1822.Device._d__set_type}

Device._omni_skeleton = Device
_0_INF1822__POA.Device = Device
omniORB.registerSkeleton(Device._NP_RepositoryId, Device)
del Device
__name__ = "INF1822"

# interface LightDevice
_0_INF1822._d_LightDevice = (omniORB.tcInternal.tv_objref, "IDL:INF1822/LightDevice:1.0", "LightDevice")
omniORB.typeMapping["IDL:INF1822/LightDevice:1.0"] = _0_INF1822._d_LightDevice
_0_INF1822.LightDevice = omniORB.newEmptyClass()
class LightDevice (_0_INF1822.Device):
    _NP_RepositoryId = _0_INF1822._d_LightDevice[1]

    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")

    _nil = CORBA.Object._nil


_0_INF1822.LightDevice = LightDevice
_0_INF1822._tc_LightDevice = omniORB.tcInternal.createTypeCode(_0_INF1822._d_LightDevice)
omniORB.registerType(LightDevice._NP_RepositoryId, _0_INF1822._d_LightDevice, _0_INF1822._tc_LightDevice)

# LightDevice operations and attributes
LightDevice._d__get_lightLevel = ((),(omniORB.tcInternal.tv_long,),None)
LightDevice._d__set_lightLevel = ((omniORB.tcInternal.tv_long,),(),None)

# LightDevice object reference
class _objref_LightDevice (_0_INF1822._objref_Device):
    _NP_RepositoryId = LightDevice._NP_RepositoryId

    def __init__(self, obj):
        _0_INF1822._objref_Device.__init__(self, obj)

    def _get_lightLevel(self, *args):
        return self._obj.invoke("_get_lightLevel", _0_INF1822.LightDevice._d__get_lightLevel, args)

    def _set_lightLevel(self, *args):
        return self._obj.invoke("_set_lightLevel", _0_INF1822.LightDevice._d__set_lightLevel, args)

    lightLevel = property(_get_lightLevel, _set_lightLevel)


omniORB.registerObjref(LightDevice._NP_RepositoryId, _objref_LightDevice)
_0_INF1822._objref_LightDevice = _objref_LightDevice
del LightDevice, _objref_LightDevice

# LightDevice skeleton
__name__ = "INF1822__POA"
class LightDevice (_0_INF1822__POA.Device):
    _NP_RepositoryId = _0_INF1822.LightDevice._NP_RepositoryId


    _omni_op_d = {"_get_lightLevel": _0_INF1822.LightDevice._d__get_lightLevel, "_set_lightLevel": _0_INF1822.LightDevice._d__set_lightLevel}
    _omni_op_d.update(_0_INF1822__POA.Device._omni_op_d)

LightDevice._omni_skeleton = LightDevice
_0_INF1822__POA.LightDevice = LightDevice
omniORB.registerSkeleton(LightDevice._NP_RepositoryId, LightDevice)
del LightDevice
__name__ = "INF1822"

# interface MasterLightDevice
_0_INF1822._d_MasterLightDevice = (omniORB.tcInternal.tv_objref, "IDL:INF1822/MasterLightDevice:1.0", "MasterLightDevice")
omniORB.typeMapping["IDL:INF1822/MasterLightDevice:1.0"] = _0_INF1822._d_MasterLightDevice
_0_INF1822.MasterLightDevice = omniORB.newEmptyClass()
class MasterLightDevice (_0_INF1822.LightDevice):
    _NP_RepositoryId = _0_INF1822._d_MasterLightDevice[1]

    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")

    _nil = CORBA.Object._nil


_0_INF1822.MasterLightDevice = MasterLightDevice
_0_INF1822._tc_MasterLightDevice = omniORB.tcInternal.createTypeCode(_0_INF1822._d_MasterLightDevice)
omniORB.registerType(MasterLightDevice._NP_RepositoryId, _0_INF1822._d_MasterLightDevice, _0_INF1822._tc_MasterLightDevice)

# MasterLightDevice operations and attributes
MasterLightDevice._d_startMonitoringDevice = ((omniORB.typeMapping["IDL:INF1822/LightDevice:1.0"], ), (omniORB.typeMapping["IDL:INF1822/LightDevice:1.0"], ), None)

# MasterLightDevice object reference
class _objref_MasterLightDevice (_0_INF1822._objref_LightDevice):
    _NP_RepositoryId = MasterLightDevice._NP_RepositoryId

    def __init__(self, obj):
        _0_INF1822._objref_LightDevice.__init__(self, obj)

    def startMonitoringDevice(self, *args):
        return self._obj.invoke("startMonitoringDevice", _0_INF1822.MasterLightDevice._d_startMonitoringDevice, args)

omniORB.registerObjref(MasterLightDevice._NP_RepositoryId, _objref_MasterLightDevice)
_0_INF1822._objref_MasterLightDevice = _objref_MasterLightDevice
del MasterLightDevice, _objref_MasterLightDevice

# MasterLightDevice skeleton
__name__ = "INF1822__POA"
class MasterLightDevice (_0_INF1822__POA.LightDevice):
    _NP_RepositoryId = _0_INF1822.MasterLightDevice._NP_RepositoryId


    _omni_op_d = {"startMonitoringDevice": _0_INF1822.MasterLightDevice._d_startMonitoringDevice}
    _omni_op_d.update(_0_INF1822__POA.LightDevice._omni_op_d)

MasterLightDevice._omni_skeleton = MasterLightDevice
_0_INF1822__POA.MasterLightDevice = MasterLightDevice
omniORB.registerSkeleton(MasterLightDevice._NP_RepositoryId, MasterLightDevice)
del MasterLightDevice
__name__ = "INF1822"

#
# End of module "INF1822"
#
__name__ = "inf1822_idl"

_exported_modules = ( "INF1822", )

# The end.
