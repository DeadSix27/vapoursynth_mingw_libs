# #################################################################################################################
# Copyright (C) 2017 DeadSix27
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# #################################################################################################################

VAPOURSYNTH_VERSION = R39
#64, 32
ARCH = 64
ifndef PREFIX
$(error PREFIX is not set)
endif
ifndef GENDEF
$(error GENDEF is not set)
endif
ifndef DLLTOOL
$(error DLLTOOL is not set)
endif

all:
	@python install_vapoursynth_libs.py install $(ARCH) $(VAPOURSYNTH_VERSION) $(PREFIX) $(DLLTOOL) $(GENDEF)
uninstall:
	@python install_vapoursynth_libs.py uninstall $(ARCH) $(VAPOURSYNTH_VERSION) $(PREFIX) $(DLLTOOL) $(GENDEF)