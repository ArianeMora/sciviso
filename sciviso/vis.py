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

import io
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.colors import ListedColormap
from textwrap import wrap

from sciutil import SciUtil, SciException


class VisException(SciException):
    def __init__(self, message=''):
        Exception.__init__(self, message)


class Vis:

    """

    #font.serif      : DejaVu Serif, Bitstream Vera Serif, Computer Modern Roman,
    New Century Schoolbook, Century Schoolbook L, Utopia, ITC Bookman, Bookman, Nimbus Roman No9 L,
    Times New Roman, Times, Palatino, Charter, serif
#font.sans-serif : DejaVu Sans, Bitstream Vera Sans, Computer Modern Sans Serif,

 Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif

    """

    def __init__(self, df: pd.DataFrame, sciutil=None, cmap='seismic', sep='_', dpi=300,
                 style='ticks', palette='pastel', opacity=0.8, default_colour="teal", figsize=(3, 3),
                 title_font_size=8, label_font_size=6, title_font_weight=700, text_font_weight=700):
        self.sep = sep
        self.df = df
        self.columns = list(df.columns)
        self.cmap = ListedColormap(sns.color_palette(cmap))
        self.figsize = figsize
        self.dpi = dpi
        self.palette = palette
        self.style = style
        self.u = SciUtil() if sciutil is None else sciutil
        self.opacity = opacity
        self.label = ''
        self.default_colour = default_colour
        self.label_font_size = label_font_size
        self.title_font_size = title_font_size
        self.title_font_weight = title_font_weight
        self.text_font_weight = text_font_weight
        self.palette = palette
        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.cmap_str = cmap
        self.labels = 'short'
        self.palette = ['#483873', '#1BD8A6', '#B117B7', '#AAC7E2', '#FFC107', '#016957', '#9785C0',
             '#D09139', '#338A03', '#FF69A1', '#5930B1', '#FFE884', '#35B567', '#1E88E5',
             '#ACAD60', '#A2FFB4', '#B618F5', '#854A9C']
        plt.rcParams['svg.fonttype'] = 'none'  # Ensure text is saved as text
        plt.rcParams['figure.figsize'] = self.figsize
        sns.set(rc={'figure.figsize': self.figsize, 'font.family': 'sans-serif',
                    'font.sans-serif': 'Arial', 'font.size': label_font_size}, style=self.style)

    def load_style(self, style_dict):
        """ Load a style from a dict. """
        self.default_colour = style_dict.get('default_colour') or self.default_colour
        self.label_font_size = style_dict.get('label_font_size') or self.label_font_size
        self.title_font_size = style_dict.get('title_font_size') or self.title_font_size
        self.title_font_weight = style_dict.get('title_font_weight') or self.title_font_weight
        self.text_font_weight = style_dict.get('text_font_weight') or self.text_font_weight
        self.palette = style_dict.get('palette') or self.palette
        self.figsize = style_dict.get('figsize') or self.figsize
        plt.rcParams['figure.figsize'] = self.figsize
        sns.set(rc={'figure.figsize': self.figsize, 'font.family': 'sans-serif',
                    'font.sans-serif': 'Arial', 'font.size': self.label_font_size}, style=self.style)
        self.cmap_str = style_dict.get('cmap') or self.cmap_str
        self.style = style_dict.get('style') or self.style
        self.cmap = ListedColormap(sns.color_palette(self.cmap_str))
        self.opacity = style_dict.get('opacity') or self.opacity
        self.labels = style_dict.get('labels') or self.labels

    def set_palette(self, palette):
        self.palette = palette

    def add_labels(self, title=True, x=True, y=True):
        if x:
            plt.xlabel(self.xlabel, fontsize=self.label_font_size, fontweight=self.text_font_weight)
        if y:
            plt.ylabel(self.ylabel, fontsize=self.label_font_size, fontweight=self.text_font_weight)
        if title:
            plt.title(self.title, fontsize=self.title_font_size, fontweight=self.title_font_weight)

    @staticmethod
    def apply_limits(axis, max_v: float, min_v=None):
        min_v = 0 if min_v is None else min_v
        if axis == 'x' and max_v is not None:
            plt.xlim(min_v, max_v)
        elif axis == 'y' and max_v is not None:
            plt.ylim(min_v, max_v)

    @staticmethod
    def return_svg() -> str:
        """
        Returns the svg string.
        Parameters
        ----------
        plot

        Returns
        -------

        """
        file_io = io.StringIO()
        plt.savefig(file_io, format="svg")
        return file_io.getvalue()

    def save_svg(self, label_lst: list) -> None:
        label = self.u.generate_label(label_lst, '.svg')
        plt.savefig(label)

    def save_png(self, label_lst: list) -> None:
        label = self.u.generate_label(label_lst, '.png')
        self.u.save_plt(plt, label, dpi=300)

    def get_columns(self, reqs=None, method="all") -> list:
        """

        Parameters
        ----------
        reqs:   a list of requirements in the columns
        method: "any" or "all" i.e. whether all or any of the requirements have to be met.

        Returns
        -------
        list of columns in the dataframe meeting the requirements
        """
        if reqs is None:
            return self.columns
        else:
            cols_w_reqs = []
            for c in self.columns:
                cnt = 0
                for req in reqs:
                    if req in c:
                        cnt += 1
                if method == 'all':
                    if cnt == len(reqs):
                        cols_w_reqs.append(c)
                elif method == 'any':
                    if cnt > 0:
                        cols_w_reqs.append(c)
                else:
                    msg = self.u.msg.msg_arg_err("get_columns", "method", method, ["all", "any"])
                    self.u.err_p([msg])
                    raise VisException(msg)
            return cols_w_reqs

    def check_columns(self, columns: list) -> None:
        for c in columns:
            if c not in self.columns:
                msg = self.u.msg.msg_arg_err("check_columns", "columns", c, self.columns)
                self.u.err_p([msg])
                raise VisException(msg)

    def check_args_in_columns(self, args: list) -> None:
        """
        Check all the arguments exist in the columns.
        Parameters
        ----------
        args

        Returns
        -------

        """
        for arg in args:
            if not isinstance(arg, list):
                msg = self.u.msg.msg_data_type("check_args_in_columns", arg, "list")
                self.u.err_p([msg])
                raise VisException(msg)

            self.check_columns(arg)

    @staticmethod
    def check_label(label_lst: list, label_alt: str) -> list:
        """
        Checks label is in the correct format
        Parameters
        ----------
        label_lst
        label_alt

        Returns
        -------

        """
        if label_lst is None:
            return ['.', label_alt]
        return label_lst

    def get_plot_str(self) -> str:
        self.plot()
        return self.return_svg()

    def save_plot(self, label_lst: list) -> None:
        label_lst = self.check_label(label_lst, self.label)
        self.plot()
        self.save_svg(label_lst)

    def plot(self):
        self.u.warn_p(["Please initiate one of the charts. Vis is just a wrapper. See docs for more info."])

    def set_ax_params(self, ax):
        ax.tick_params(direction='out', length=2, width=0.5)
        ax.spines['bottom'].set_linewidth(0.5)
        ax.spines['top'].set_linewidth(0)
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['right'].set_linewidth(0)
        ax.tick_params(labelsize=self.label_font_size)
        ax.tick_params(axis='x', which='major', pad=2.0)
        ax.tick_params(axis='y', which='major', pad=2.0)
        # Make sure if the labels are very long they wrap
        labels = [str(item.get_text()).replace('_', ' ') for item in ax.get_xticklabels()]
        if self.labels == 'wrap':
            labels_short = ['\n'.join(wrap(l, 20)) for l in labels]
        elif self.labels == 'short':
            labels_short = []
            for l in labels:
                if len(l) < 15:
                    labels_short.append(l)
                else:
                    labels_short.append(f'{l[:15]}...')
        else:
            labels_short = labels
        if labels_short[0] != '':
            ax.set_xticklabels(labels_short, weight=self.text_font_weight)
