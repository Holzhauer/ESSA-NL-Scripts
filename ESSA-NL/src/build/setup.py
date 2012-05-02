# Script for py2exe
#
# @author:    Sascha Holzhauer, CESR, Kassel, Germany
# @date:    22.06.2011
#

from distutils.core import setup


manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
/>
<description>%(prog)s Program</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''

RT_MANIFEST = 24


essa_nl = dict(
    script = "essa_nl.py",
    other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog="essa_nl"))],
    dest_base = r"prog\essa_nl")

zipfile = r"lib\shardlib.zip"

options = {"py2exe": {"compressed": 1,
                      "optimize": 2,
                      "dist_dir":"..\\..\\dist"
                      }
}

FROM_DIRECTORY = r"..\\..\\dist"

################################################################
import os

class InnoScript:
    def __init__(self,
                 name,
                 lib_dir,
                 dist_dir,
                 windows_exe_files = [],
                 lib_files = [],
                 version = "1.0"):
        self.lib_dir = lib_dir
        self.dist_dir = dist_dir
        if not self.dist_dir[-1] in "\\/":
            self.dist_dir += "\\"
        self.name = name
        self.version = version
        self.windows_exe_files = [self.chop(p) for p in windows_exe_files]
        self.lib_files = [self.chop(p) for p in lib_files]

    def chop(self, pathname):
        assert pathname.startswith(self.dist_dir)
        return pathname[len(self.dist_dir):]


    def innoSourceLine(self, source, dest):
        #return 'Source: "%s"; DestDir: "{app}\%s"; CopyMode: alwaysoverwrite'%(source, dest)
        return 'Source: "%s"; DestDir: "{app}\%s"; Flags: ignoreversion'%(source, dest)

    
    def create(self, pathname="..\\..\\dist\\essa-nl.iss"):
        self.pathname = pathname
        ofi = self.file = open(pathname, "w")
        print >> ofi, "; WARNING: This script has been created by py2exe. Changes to this script"
        print >> ofi, "; will be overwritten the next time py2exe is run!"
        print >> ofi, r"[Setup]"
        print >> ofi, r"AppName=%s" % self.name
        print >> ofi, r"AppVerName=%s %s" % (self.name, self.version)
        print >> ofi, r"DefaultDirName={pf}\%s" % self.name
        print >> ofi, r"DefaultGroupName=%s" % self.name
        print >> ofi

        print >> ofi, r"[Files]"
#        for path in self.windows_exe_files + self.lib_files:
#            print >> ofi, r'Source: "%s"; DestDir: "{app}\%s"; Flags: ignoreversion' % (path, os.path.dirname(path))
        currPath = os.getcwd()
        os.chdir(FROM_DIRECTORY)
        for root, dirs, files in os.walk("."):
            sourcedir = os.path.abspath(root)
            for f in files:
                # get the destination directory
                source = os.path.join(sourcedir, f)
                dest = root
                print >> ofi, self.innoSourceLine(source, dest)
                        
        
        print >> ofi, """
    [Tasks]
    Name: "quicklaunchicon"; Description: "Create Icon on Start Panel"; GroupDescription: "Further Options to call the programm:"; Flags: checkedonce 
    Name: "desktopicon"; Description: "Create icon on Desktop"; GroupDescription: "Further Options to call the programm:"; Flags: checkedonce 
    """
        print >> ofi, r"[Icons]"
        for path in self.windows_exe_files:
            print >> ofi, r'Name: "{group}\%s"; Filename: "{app}\%s"' % \
                  (self.name, path)
        print >> ofi, 'Name: "{group}\Uninstall %s"; Filename: "{uninstallexe}"' % self.name
        print >> ofi, 'Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\%s"; Filename: "{app}\%s"; Tasks: quicklaunchicon' % (self.name, path)
        print >> ofi, 'Name: "{userdesktop}\%s"; Filename: "{app}\%s"; Tasks: desktopicon' % (self.name, path)
        
        os.chdir(currPath)

    def compile(self):
        try:
            import ctypes
        except ImportError:
            try:
                import win32api
            except ImportError:
                import os
                os.startfile(self.pathname)
            else:
                print "Ok, using win32api."
                win32api.ShellExecute(0, "compile",
                                                self.pathname,
                                                None,
                                                None,
                                                0)
        else:
            print "Cool, you have ctypes installed."
            res = ctypes.windll.shell32.ShellExecuteA(0, "compile",
                                                      self.pathname,
                                                      None,
                                                      None,
                                                      0)
            if res < 32:
                raise RuntimeError, "ShellExecute failed, error %d (%s)" % (res, self.pathname)
            
            # google: "ctypes.windll.shell32.ShellExecuteA" 2


################################################################

from py2exe.build_exe import py2exe

class build_installer(py2exe):
    # This class first builds the exe file(s), then creates a Windows installer.
    # You need InnoSetup for it.
    def run(self):
        # First, let py2exe do it's work.
        py2exe.run(self)

        lib_dir = self.lib_dir
        dist_dir = self.dist_dir
        
        # create the Installer, using the files py2exe has created.
        script = InnoScript("ESSA-NL",
                            lib_dir,
                            dist_dir,
                            self.windows_exe_files,
                            self.lib_files)
        print "*** creating the inno setup script***"
        script.create()
        print "*** compiling the inno setup script***"
        script.compile()
        # Note: By default the final setup.exe will be in an Output subdirectory.

################################################################

setup(
    name = 'ESSA Newsletter Tool',
    options = options,
    # The lib directory contains everything except the executables and the python dll.
    zipfile = zipfile,
    description = 'Fetch newsletter contents from Google spreadsheets and convert to HTML.',
    version = '1.0',
    windows = [
                  {
                      'script': '../essa_complete.py',
                      'icon_resources': [(1, "essa_nl.ico")],
                  }
              ],
    # use out build_installer class as extended py2exe build command
    cmdclass = {"py2exe": build_installer},
    data_files=[("config",["../config/essanl.config",]), ("ESSA-NL/general",["../ESSA-NL/general/content.html",]),("ESSA-NL/general",["../ESSA-NL/general/footer.html",])]
    )