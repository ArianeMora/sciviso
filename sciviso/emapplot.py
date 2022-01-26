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
import matplotlib as mpl

import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.patches import Rectangle
from matplotlib.legend_handler import HandlerBase

from sciviso import Vis

# https://stackoverflow.com/questions/55501860/how-to-put-multiple-colormap-patches-in-a-matplotlib-legend
class HandlerColormap(HandlerBase):
    def __init__(self, cmap, num_stripes=8, **kw):
        HandlerBase.__init__(self, **kw)
        self.cmap = cmap
        self.num_stripes = num_stripes
    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        stripes = []
        for i in range(self.num_stripes):
            s = Rectangle([xdescent + i * width / self.num_stripes, ydescent],
                          width / self.num_stripes,
                          height,
                          fc=self.cmap((2 * i + 1) / (2 * self.num_stripes)),
                          transform=trans, linewidth=0)
            stripes.append(s)
        return stripes


class Emapplot(Vis):

    def __init__(self, df: pd.DataFrame, config={}):
        super().__init__(df)
        if config:
            self.load_style(config)

    def build_graph(self):
        """
        Builds a graph from the dataframe from R
        :return:
        """
        G = nx.Graph()
        node_cmap = 'RdBu_r'
        edge_cmap = 'Greys'
        min_overlap = 1
        edge_map = defaultdict(dict)
        gene_ids = self.df['geneID'].values
        gene_ids = [set(genes.split('/')) for genes in gene_ids] # Turn it into a list
        # Want to iterate over and get the maps between the two
        for i, id_i in enumerate(self.df['ID'].values):
            for j, id_j in enumerate(self.df['ID'].values):
                if i != j:
                    if edge_map.get(id_j):
                        if edge_map[id_j].get(id_i):
                            continue
                        else:
                            overlapping_genes = len(gene_ids[i] & gene_ids[j])
                            if overlapping_genes > min_overlap:
                                edge_map[id_i][id_j] = overlapping_genes
                    else:
                        overlapping_genes = len(gene_ids[i] & gene_ids[j])
                        if overlapping_genes > min_overlap:
                            edge_map[id_i][id_j] = overlapping_genes
        edges = []
        for node1 in edge_map:
            for node2 in edge_map[node1]:
                edges.append((node1, node2))
        G.add_edges_from(edges)
        nodes = G.nodes()
        # Check that all nodes have been added and if not add them
        nodes_to_add = [node_id for node_id in self.df['ID'].values if node_id not in nodes]
        for node in nodes_to_add:
            G.add_node(node)
        # Now we want a list of node sizes and colours
        mins = np.min(self.df['Count'].values)
        maxs = np.max(self.df['Count'].values)
        norms = maxs - mins
        counts = [100 * (maxs - c)/norms for c in self.df['Count'].values]
        self.df['Count'] = counts
        sizes = self.df['Count'].values
        colour = self.df['p.adjust'].values
        # Colour the edges by the number of genes shared between the nodes
        edge_values = [edge_map[edge[0]][edge[1]] for edge in edges]
        lut = dict(zip(set(edge_values), sns.color_palette("Greys", len(set(edge_values)))))
        edge_colours = pd.DataFrame(edge_values)[0].map(lut).values
        # Need to create a layout when doing
        # separate calls to draw nodes and edges
        pos = nx.spring_layout(G,  k=1) # nx.kamada_kawai_layout(G)
        nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap(node_cmap),
                               node_color=colour, node_size=sizes)

        labels = dict(zip(self.df['ID'].values, self.df['Description'].values))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edge_colours, arrows=False)
        # Plot the small labels and then for each "cluster" plot the smallest GO ID this should
        # correspond to the "top" term.
        # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.clique.find_cliques.html#networkx.algorithms.clique.find_cliques
        cliques = nx.find_cliques(G)
        labels_to_draw = {}
        gene_numbers = dict(zip(self.df['ID'].values, self.df['Count'].values))

        # If the user has selected the smallest GO term as the one they want
        # for clique in cliques:
        #     # For each clique we want to get the GO term with the smallest ID
        #     smallest_GO = min([g.split(':')[1] for g in clique])
        #     labels_to_draw[f'GO:{smallest_GO}'] = labels[f'GO:{smallest_GO}']

        for clique in cliques:
            # For each clique we want to get the GO term with the smallest ID
            smallest_GO = np.argmax([gene_numbers.get(g) for g in clique])
            go = clique[smallest_GO]
            labels_to_draw[go] = labels[go]

        small_labels ={}
        for go in labels:
            if not labels_to_draw.get(go):
                small_labels[go] = labels[go]
        nx.draw_networkx_labels(G, pos, small_labels, font_size=8, font_color='lightgrey',
                                clip_on=False, verticalalignment='bottom')

        nx.draw_networkx_labels(G, pos, labels_to_draw, verticalalignment='bottom',
                                font_weight='bold', clip_on=False)
        cmin_node = '{:.2e}'.format(min(colour))
        cmax_node = '{:.2e}'.format(max(colour))

        cmap_labels = [f'P.adj:{cmin_node},{cmax_node}', f'G.shared:{min(edge_values)}-{max(edge_values)}']
        # create proxy artists as handles:
        cmaps = [plt.get_cmap(node_cmap), plt.get_cmap(edge_cmap)]
        cmap_handles = [Rectangle((0, 0), 1, 1) for _ in cmaps]
        handler_map = dict(zip(cmap_handles,
                               [HandlerColormap(cm, num_stripes=8) for cm in cmaps]))
        legend2 = plt.legend(handles=cmap_handles,
                   labels=cmap_labels,
                   handler_map=handler_map,
                   fontsize=8, bbox_to_anchor=(0.4, 0.3))

        plt.gca().add_artist(legend2)

        gene_min = int(np.min(self.df['Count'].values))
        gene_max = int(np.max(self.df['Count'].values))
        gll = plt.scatter([], [], s=gene_min, marker='o', color='#222')
        ga = plt.scatter([], [], s=gene_max, marker='o', color='#222')

        legend = plt.legend((gll, ga),
                   (str(gene_min), str(gene_max)),
                   scatterpoints=1,
                   loc='lower left',
                   ncol=1,
                   fontsize=8, bbox_to_anchor=(0, -0.1))
        legend.set_title("No. Genes")
        # handles = [Patch(facecolor=lut[name]) for name in lut]
        # legend = plt.legend(handles, lut) #, bbox_to_anchor=(2, 1))
        plt.gca().add_artist(legend)
        plt.axis("off")