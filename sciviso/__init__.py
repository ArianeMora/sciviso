###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

__title__ = 'sciviso'
__description__ = 'sciviso: Wrapper for common visualisations for sci packages.'
__url__ = 'https://github.com/ArianeMora/sciviso.git'
__version__ = '1.0.9'
__author__ = 'Ariane Mora'
__author_email__ = 'ariane.n.mora@gmail.com'
__license__ = 'GPL3'

from sciviso.vis import Vis, VisException
from sciviso.violinplot import Violinplot
from sciviso.boxplot import Boxplot
from sciviso.barchart import Barchart
from sciviso.heatmap import Heatmap
from sciviso.histogram import Histogram
from sciviso.scatterplot import Scatterplot
from sciviso.volcanoplot import Volcanoplot
from sciviso.emapplot import Emapplot
from sciviso.line import Line
from sciviso.sankey import Sankeyplot
