import clr
import System

clr.AddReference("System.Management.Automation")
from System.Management.Automation import Runspaces
import clrtype
from ctypes import *
import ctypes
from System import Convert, Text, Environment
from System.Management.Automation import Runspaces, RunspaceInvoke
from System.Runtime.InteropServices import DllImportAttribute, PreserveSigAttribute, Marshal, HandleRef, CharSet

def main():
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