# #################################################################################################################
# Copyright (C) 2017 DeadSix27
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

ifndef VAPOURSYNTH_VERSION
$(error Please set VAPOURSYNTH_VERSION, e.g R49))
endif

all:
	@python2 install_vapoursynth_libs.py install $(ARCH) $(VAPOURSYNTH_VERSION) $(PREFIX) $(DLLTOOL) $(GENDEF)
uninstall:
	@python2 install_vapoursynth_libs.py uninstall $(ARCH) $(VAPOURSYNTH_VERSION) $(PREFIX) $(DLLTOOL) $(GENDEF)
