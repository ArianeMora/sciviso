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

import os
import matplotlib.pyplot as plt
import pandas as pd
import shutil
import tempfile
import unittest

from sciviso import Barchart, Boxplot, Heatmap, Scatterplot, Violinplot, Volcanoplot


class TestVis(unittest.TestCase):

    def setUp(self):
        # Flag to set data to be local so we don't have to download them repeatedly. ToDo: Remove when publishing.
        self.local = True
        THIS_DIR = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(THIS_DIR, 'data/')
        if self.local:
            self.tmp_dir = os.path.join(THIS_DIR, 'data/tmp/')
            if os.path.exists(self.tmp_dir):
                shutil.rmtree(self.tmp_dir)
            os.mkdir(self.tmp_dir)
        else:
            self.tmp_dir = tempfile.mkdtemp(prefix='scidatannotate_tmp_')
        # Lets use a simple dataframe e.g. the iris dataset
        self.df = pd.read_csv(self.data_dir + 'iris.csv')
        self.x = 'sepal_width'
        self.y = 'petal_width'
        self.numeric_cols = ['sepal_width', 'sepal_length', 'petal_length', 'petal_width']
        self.label = 'label'

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_barchart(self):
        barchart = Barchart(self.df, self.label, self.y)
        barchart.plot()
        plt.show()

    def test_boxplot(self):
        boxplot = Boxplot(self.df, self.label, self.y)
        boxplot.plot()
        plt.show()
        # Example showing formatting data for plots
        df = boxplot.format_data_for_boxplot(self.df, ["sepal_length", "sepal_width"], "label", ["Iris-setosa", "Iris-virginica"])
        boxplot = Boxplot(df, "Conditions", "Values")
        boxplot.plot()
        plt.show()

    def test_heatmap(self):
        heatmap = Heatmap(self.df, self.numeric_cols, self.label, 'Xlabel', 'Ylabel')
        heatmap.plot()
        heatmap.save_png([self.data_dir, "heatmap"])
        plt.show()

    def test_scatterplot(self):
        scatterplot = Scatterplot(self.df, self.x, self.y, 'sepal_length', 'Xlabel', 'Ylabel', points_to_annotate=['Iris-setosa'],
                                  annotation_label=self.label)
        scatterplot.plot()
        plt.show()

    def test_violinplot(self):
        violinplot = Violinplot(self.df, self.label, self.y, 'Xlabel', 'Ylabel', add_dots=True)
        violinplot.plot()
        plt.show()

    def test_volcanoplot(self):
        volcanoplot = Volcanoplot(self.df, self.x, self.y, self.label, 'A Title', 'Xlabel', 'Ylabel', label_big_sig=True)
        volcanoplot.plot()
        plt.show()

