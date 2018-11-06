#!/usr/bin/env python2

# #################################################################################################################
# Copyright (C) 2017 DeadSix27 (https://github.com/DeadSix27/vapoursynth_mingw_libs)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# #################################################################################################################


import sys,os,urllib

def is_tool(name):
        from distutils.spawn import find_executable
        return find_executable(name) is not None

SUPPORTED_VERSIONS = ('R37','R38','R39','R40','R41','R42','R42.1','R43','R44','R45')

VS_PC = """prefix=%%PREFIX%% 
exec_prefix=${prefix} 
libdir=${exec_prefix}/lib 
includedir=${prefix}/include/vapoursynth 
 
Name: vapoursynth 
Description: A frameserver for the 21st century 
Version: %%VERSION%% 
 
Requires.private: zimg 
Libs: -L${libdir} -lvapoursynth 
Libs.private: -L${libdir} -lzimg
Cflags: -I${includedir}"""

VSS_PC = """prefix=%%PREFIX%% 
exec_prefix=${prefix} 
libdir=${exec_prefix}/lib 
includedir=${prefix}/include/vapoursynth 
 
Name: vapoursynth-script 
Description: Library for interfacing VapourSynth with Python 
Version: %%VERSION%%
 
Requires: vapoursynth 
Requires.private: python-3.7
Libs: -L${libdir} -lvapoursynth-script 
Libs.private: -lpython37 
Cflags: -I${includedir}"""


def runCmd(cmd):
	if os.system(cmd) != 0:
		print("Failed to execute: " + str(cmd))
		exit(1)

def exitHelp():
	print("install_vapoursynth_libs.py install/uninstall <64/32> <version> <install_prefix> <dlltool> <gendef> - e.g install_vapoursynth_libs.py 64 R45 /test/cross_compilers/....../ DLLTOOLPATH GENDEFPATH")
	exit(1)
def exitVersions():
	print("Only these versions are supported: " + " ".join(SUPPORTED_VERSIONS))
	exit(1)
	
def simplePatch(infile,replacetext,withtext):
	lines = []
	print("Patching " + infile )
	with open(infile) as f:
		for line in f:
			line = line.replace(replacetext, withtext)
			lines.append(line)
	with open(infile, 'w') as f2:
		for line in lines:
			f2.write(line)

if not is_tool("rsync") or not is_tool("7z"):
	print("Please make sure that p7zip and rsync are installed.")
	exit(1)

if len(sys.argv) != 7:
	exitHelp()
else:
	if sys.argv[1] == "install":
		arch     = sys.argv[2]
		ver      = sys.argv[3]
		ver_suff = ver[1:]
		prefix   = sys.argv[4]
		dlltool  = sys.argv[5]
		gendef   = sys.argv[6]
		
		runCmd("mkdir work")
		runCmd("mkdir bin")
		os.chdir("work")
		print("Downloading")
		runCmd("wget https://github.com/vapoursynth/vapoursynth/releases/download/{0}/VapourSynth{1}-Portable-{0}.7z".format(ver,arch))
		runCmd('7z x -aoa "VapourSynth{1}-Portable-{0}.7z"'.format(ver,arch))
		
		print("Local installing binaries")
		runCmd("cp {0} ../bin".format("VSScript.dll"))
		runCmd("cp {0} ../bin".format("VapourSynth.dll"))
		pydName = "vapoursynth.cp36-win_amd64.pyd"
		if ver == "R45":
			pydName = "vapoursynth.cp37-win_amd64.pyd"
		runCmd("cp {0} ../bin".format(pydName))
		runCmd("cp {0} ../bin".format("portable.vs"))
		runCmd("cp -r {0} ../bin/".format("vapoursynth64"))
		print("Creating library")
		runCmd("{0} {1}".format(gendef,"VSScript.dll"))
		runCmd("{0} -d {1} -y {2}".format(dlltool,"VSScript.def","libvapoursynth-script.a"))
		runCmd("{0} {1}".format(gendef,"VapourSynth.dll"))
		runCmd("{0} -d {1} -y {2}".format(dlltool,"VapourSynth.def","libvapoursynth.a"))
		
		
		runCmd("mkdir lib")
		
		runCmd("mv libvapoursynth.a lib/")
		runCmd("mv libvapoursynth-script.a lib/")
		
		os.chdir("lib")
		
		runCmd("mkdir pkgconfig")
		
		os.chdir("pkgconfig")
		
		print("Creating pkgconfig")
		
		pc_script = VSS_PC.replace('%%PREFIX%%',prefix).replace('%%VERSION%%',ver_suff)
		pc        = VS_PC.replace('%%PREFIX%%',prefix).replace('%%VERSION%%',ver_suff)
		
		with open("vapoursynth.pc","w") as f:
			f.write(pc)
			
		with open("vapoursynth-script.pc","w") as f:
			f.write(pc_script)
		
		os.chdir("..")
		os.chdir("..")
		
		runCmd("mkdir include")
		os.chdir("include")
		
		runCmd("wget https://github.com/vapoursynth/vapoursynth/archive/{0}.tar.gz".format(ver))
		runCmd("tar -xvf {0}.tar.gz vapoursynth-{0}/include".format(ver))
		
		runCmd("mv vapoursynth-{0}/include vapoursynth".format(ver))
		runCmd("rm -r vapoursynth-{0}".format(ver))
		runCmd("rm {0}.tar.gz".format(ver))
		os.chdir("..")
		
		runCmd("mkdir ../work2")
		
		runCmd("mv include ../work2")
		runCmd("mv lib ../work2")
		
		os.chdir("..")
		
		print("Installing to " + prefix)
		runCmd("rsync -aKv work2/ {0}".format(prefix))
		
		runCmd("rm -r work")
		runCmd("rm -r work2")
		
		
	elif sys.argv[1] == "uninstall":
		pass
	else:
		exitHelp()
