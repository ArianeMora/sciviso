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


from sciutil import SciUtil, SciException


class VisException(SciException):
    def __init__(self, message=''):
        Exception.__init__(self, message)


class Vis:

    def __init__(self, df: pd.DataFrame, sciutil=None, cmap='viridis', sep='_', figsize=(12, 8), dpi=300,
                 style='whitegrid', palette='pastel', opacity=0.8):
        self.sep = sep
        self.df = df
        self.columns = list(df.columns)
        self.cmap = cmap
        self.figsize = figsize
        self.dpi = dpi
        self.palette = palette
        sns.set(style="whitegrid")
        sns.set(rc={'figure.figsize': self.figsize})
        self.u = SciUtil() if sciutil is None else sciutil
        self.opacity = opacity

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