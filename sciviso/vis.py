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

    def __init__(self, df: pd.DataFrame, sciutil=None, cmap='Purples', sep='_', dpi=300,
                 style='ticks', palette='pastel', opacity=0.8, default_colour="teal", figsize=(3, 3),
                 title_font_size=12, label_font_size=8, title_font_weight=700, text_font_weight=700):
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
        self.axis_font_size = label_font_size
        self.palette = palette
        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.cmap_str = cmap
        self.labels = None
        self.bins, self.cluster_rows, self.cluster_cols, self.line_width = None, None, None, None
        self.col_colours, self.row_colours, self.vmin, self.vmax, self.x_tick_labels = None, None, None, None, None
        self.min_x, self.min_y, self.max_x, self.max_y = None, None, None, None
        self.add_legend, self.zlabel, self.colour = None, None, None
        self.hue, self.add_dots, self.add_stats, self.stat_method = None, None, None, None
        self.palette = palette if palette else ['#AAC7E2', '#FFC107', '#016957', '#9785C0',
             '#D09139', '#338A03', '#FF69A1', '#5930B1', '#FFE884', '#35B567', '#1E88E5',
             '#ACAD60', '#A2FFB4', '#B68F5', '#854A9C']
        if isinstance(self.palette, str):
            self.palette = sns.color_palette(self.palette)

        plt.rcParams['svg.fonttype'] = 'none'  # Ensure text is saved as text
        plt.rcParams['figure.figsize'] = self.figsize
        self.font_family = 'sans-serif'
        self.font = 'Arial'
        sns.set(rc={'figure.figsize': self.figsize, 'font.family': self.font_family,
                    'font.sans-serif': self.font, 'font.size': label_font_size}, style=self.style)

    def load_style(self, style_dict):
        """ Load a style from a dict. """
        self.default_colour = style_dict.get('default_colour') or self.default_colour
        self.label_font_size = style_dict.get('label_font_size') or self.label_font_size
        self.axis_font_size = style_dict.get('axis_font_size') or self.axis_font_size
        self.title_font_size = style_dict.get('title_font_size') or self.title_font_size
        self.title_font_weight = style_dict.get('title_font_weight') or self.title_font_weight
        self.text_font_weight = style_dict.get('text_font_weight') or self.text_font_weight
        self.palette = style_dict.get('palette') or self.palette
        self.figsize = style_dict.get('figsize') or self.figsize
        plt.rcParams['figure.figsize'] = self.figsize
        self.font_family = self.font_family or 'sans-serif'
        self.font = self.font or 'Arial'
        sns.set(rc={'figure.figsize': self.figsize, 'font.family': self.font_family,
                    'font.sans-serif': self.font, 'font.size': self.label_font_size}, style=self.style)
        plt.rcParams['font.family'] = self.font_family
        plt.rcParams['font.sans-serif'] = self.font
        self.cmap_str = style_dict.get('cmap') or self.cmap_str
        self.style = style_dict.get('style') or self.style
        self.cmap = ListedColormap(sns.color_palette(self.cmap_str))
        self.opacity = style_dict.get('opacity') or self.opacity
        self.labels = style_dict.get('labels') or self.labels
        self.bins = style_dict.get('bins') or self.bins
        self.cluster_rows = style_dict.get('cluster_rows') or self.cluster_rows
        self.cluster_cols = style_dict.get('cluster_cols') or self.cluster_cols
        self.line_width = style_dict.get('line_width') or self.line_width
        self.vmin = style_dict.get('vmin') or self.vmin
        self.vmax = style_dict.get('vmax') or self.vmax
        self.col_colours = style_dict.get('col_colours') or self.col_colours
        self.row_colours = style_dict.get('row_colours') or self.row_colours
        self.x_tick_labels = style_dict.get('x_tick_labels') or self.x_tick_labels
        self.min_x = style_dict.get('min_x') or self.min_x
        self.min_y = style_dict.get('min_y') or self.min_y
        self.max_x = style_dict.get('max_x') or self.max_x
        self.max_y = style_dict.get('max_y') or self.max_y
        self.add_legend = style_dict.get('add_legend') or self.add_legend
        self.zlabel = style_dict.get('zlabel') or self.zlabel
        self.colour = style_dict.get('colour') or self.colour
        self.add_dots = style_dict.get('add_dots') or self.add_dots
        self.add_stats = style_dict.get('add_stats') or self.add_stats
        self.stat_method = style_dict.get('stat_method') or self.stat_method
        self.hue = style_dict.get('hue') or self.hue
        self.s = style_dict.get('s') or 10

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
        ax.tick_params(labelsize=self.axis_font_size)
        ax.tick_params(axis='x', which='major', pad=2.0)
        ax.tick_params(axis='y', which='major', pad=2.0)