#!/usr/bin/env python

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

SUPPORTED_VERSIONS = ('R37','R38','R39','R40')

VS_PC = """prefix=%%PREFIX%% 
exec_prefix=${prefix} 
libdir=${exec_prefix}/lib 
includedir=${prefix}/include/vapoursynth 
 
Name: vapoursynth 
Description: A frameserver for the 21st century 
Version: %%VERSION%% 
 
Requires.private: zimg 
Libs: -L${libdir} -lvapoursynth 
Libs.private: -L${libdir} -lzimg -ldl 
Cflags: -I${includedir}"""

VSS_PC = """prefix=%%PREFIX%% 
exec_prefix=${prefix} 
libdir=${exec_prefix}/lib 
includedir=${prefix}/include/vapoursynth 
 
Name: vapoursynth-script 
Description: Library for interfacing VapourSynth with Python 
Version: %%VERSION%%
 
Requires: vapoursynth 
Requires.private: python-3.6 
Libs: -L${libdir} -lvapoursynth-script 
Libs.private: -lpython36 
Cflags: -I${includedir}"""


def exitHelp():
	print("install_vapoursynth_libs.py install/uninstall <64/32> <version> <install_prefix> - e.g install_vapoursynth_libs.py amd64 R39 /test/cross_compilers/....../")
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
		
		os.system("mkdir work")
		os.system("mkdir bin")
		os.chdir("work")
		print("Downloading")
		os.system("wget https://github.com/vapoursynth/vapoursynth/releases/download/{0}/VapourSynth{1}-Portable-{0}.7z".format(ver,arch))
		os.system('7za e -aoa "VapourSynth{1}-Portable-{0}.7z"'.format(ver,arch))
		
		print("Local installing binaries")
		os.system("cp {0} ../bin".format("VSScript.dll"))
		os.system("cp {0} ../bin".format("VapourSynth.dll"))
		os.system("cp {0} ../bin".format("vapoursynth.cp36-win_amd64.pyd"))
		os.system("cp {0} ../bin".format("portable.vs"))
		print("Creating library")
		os.system("{0} {1}".format(gendef,"VSScript.dll"))
		os.system("{0} -d {1} -l {2}".format(dlltool,"VSScript.def","libvapoursynth-script.a"))
		os.system("{0} {1}".format(gendef,"VapourSynth.dll"))
		os.system("{0} -d {1} -l {2}".format(dlltool,"VapourSynth.def","libvapoursynth.a"))
		
		
		os.system("mkdir lib")
		
		os.system("mv libvapoursynth.a lib/")
		os.system("mv libvapoursynth-script.a lib/")
		
		os.chdir("lib")
		
		os.system("mkdir pkgconfig")
		
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
		
		os.system("mkdir include")
		os.chdir("include")
		
		os.system("wget https://github.com/vapoursynth/vapoursynth/archive/{0}.tar.gz".format(ver))
		os.system("tar -xvf {0}.tar.gz vapoursynth-{0}/include".format(ver))
		
		os.system("mv vapoursynth-{0}/include vapoursynth".format(ver))
		os.system("rm -r vapoursynth-{0}".format(ver))
		os.system("rm {0}.tar.gz".format(ver))
		os.chdir("..")
		
		os.system("mkdir ../work2")
		
		os.system("mv include ../work2")
		os.system("mv lib ../work2")
		
		os.chdir("..")
		
		print("Installing to " + prefix)
		os.system("rsync -aKv work2/ {0}".format(prefix))
		
		os.system("rm -r work")
		os.system("rm -r work2")
		
		
	elif sys.argv[1] == "uninstall":
		pass
	else:
		exitHelp()
