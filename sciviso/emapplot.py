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
import networkx as nx
import seaborn as sns
from matplotlib.patches import Rectangle
from matplotlib.legend_handler import HandlerBase
from matplotlib.colors import ListedColormap
import sys

from sciviso import Vis


class HandlerColormap(HandlerBase):
    """
    # https://stackoverflow.com/questions/55501860/how-to-put-multiple-colormap-patches-in-a-matplotlib-legend
    """
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

    def __init__(self, df: pd.DataFrame, size_column='Count', color_column='p.adjust', id_column='ID',
                 label_column='Description', overlap_column='gene_id', overlap_sep='/', title='',
                 config={}):
        super().__init__(df)
        self.title=title
        self.size = size_column
        self.color = color_column
        self.id = id_column
        self.label = label_column
        self.overlap_column = overlap_column
        self.overlap_sep = overlap_sep
        if config:
            self.load_style(config)

    def build_graph(self, min_overlap=1, node_cmap='viridis', plot_cliques=False):
        """
        Builds a graph from the dataframe from R
        :return:
        """
        G = nx.Graph()

        edge_map = defaultdict(dict)
        gene_ids = self.df[self.overlap_column].values
        gene_ids = [set(genes.split(self.overlap_sep)) for genes in gene_ids] # Turn it into a list
        all_genes = 0
        for g in gene_ids:
            all_genes += len(g)
        min_overlap = min_overlap
        # Want to iterate over and get the maps between the two
        for i, id_i in enumerate(self.df[self.id].values):
            for j, id_j in enumerate(self.df[self.id].values):
                if i != j:
                    if edge_map.get(id_j):
                        if edge_map[id_j].get(id_i):
                            continue
                        else:
                            overlapping_genes = len(gene_ids[i] & gene_ids[j])
                            if overlapping_genes >= min_overlap:
                                edge_map[id_i][id_j] = overlapping_genes
                    else:
                        overlapping_genes = len(gene_ids[i] & gene_ids[j])
                        if overlapping_genes >= min_overlap:
                            edge_map[id_i][id_j] = overlapping_genes
        edges = []
        for node1 in edge_map:
            for node2 in edge_map[node1]:
                edges.append((node1, node2))

        seen_nodes = []
        edge_groups = defaultdict(list)
        for node_from, node_to_lst in edge_map.items():
            if node_from not in seen_nodes:
                # Now we want to traverse the graph visiting each node
                for node in node_to_lst:
                    if node not in edge_groups[node_from] and node not in seen_nodes:
                        edge_groups[node_from].append(node)
                        seen_nodes.append(node)
                        if edge_map.get(node) and node not in seen_nodes:
                            for node2 in edge_map.get(node):
                                edge_groups[node_from].append(node2)
                                seen_nodes.append(node2)
                seen_nodes.append(node_from)
                edge_groups[node_from].append(node_from)

        G.add_edges_from(edges)
        nodes = G.nodes()
        # Check that all nodes have been added and if not add them
        nodes_to_add = [node_id for node_id in self.df[self.id].values if node_id not in nodes]
        for node in nodes_to_add:
            G.add_node(node)
            edge_groups[node].append(node) # So that we actually draw it!
        # Now we want a list of node sizes and colours
        mins = np.min(self.df[self.size].values)
        maxs = np.max(self.df[self.size].values)
        norms = maxs - mins
        counts = [20 + 100 * (maxs - c)/norms for c in self.df[self.size].values]
        sizes = counts
        colour = self.df[self.color].values
        # Colour the edges by the number of genes shared between the nodes
        edge_values = [edge_map[edge[0]][edge[1]] for edge in edges]
        lut = dict(zip(set(edge_values), sns.dark_palette("#d1d5db", len(set(edge_values)), reverse=True)))
        edge_cmap = ListedColormap(sns.dark_palette("#d1d5db", len(set(edge_values)), reverse=True))
        edge_colours = pd.DataFrame(edge_values)[0].map(lut).values
        # Need to create a layout when doing
        # separate calls to draw nodes and edges
        pos = nx.spring_layout(G,  k=2) #nx.kamada_kawai_layout(G) # nx.spring_layout(G,  k=2) #
        nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap(node_cmap),
                               node_color=colour, node_size=sizes)

        labels = dict(zip(self.df[self.id].values, self.df[self.label].values))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edge_colours, arrows=False)
        # Plot the small labels and then for each "cluster" plot the smallest GO ID this should
        # correspond to the "top" term.
        # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.clique.find_cliques.html#networkx.algorithms.clique.find_cliques
        labels_to_draw = {}
        gene_numbers = dict(zip(self.df[self.id].values, self.df[self.size].values))

        # If the user has selected the smallest GO term as the one they want
        if plot_cliques:
            cliques = nx.find_cliques(G)
            for clique in cliques:
                # For each clique we want to get the GO term with the smallest ID
                smallest_GO = min([g.split(':')[1] for g in clique])
                labels_to_draw[f'GO:{smallest_GO}'] = labels[f'GO:{smallest_GO}']

        for node, node_group in edge_groups.items():
            # For each clique we want to get the GO term with the smallest ID
            smallest_GO = np.argmax([gene_numbers.get(g) for g in node_group])
            go = node_group[smallest_GO]
            labels_to_draw[go] = labels[go]

        small_labels = {}
        for go in labels:
            if not labels_to_draw.get(go):
                small_labels[go] = labels[go]
        # Clip on is only available in later versions
        if sys.version_info[0] < 3.8:
            nx.draw_networkx_labels(G, pos, small_labels, font_size=self.axis_font_size, font_color='black',
                                    font_family='sans-serif', verticalalignment='bottom')

            nx.draw_networkx_labels(G, pos, labels_to_draw, font_size=self.label_font_size,
                                    verticalalignment='bottom',
                                    font_family='sans-serif')
        else:
            nx.draw_networkx_labels(G, pos, small_labels, font_size=self.axis_font_size, font_color='black',
                                    font_family='sans-serif', verticalalignment='bottom', clip_on=False)

            nx.draw_networkx_labels(G, pos, labels_to_draw, font_size=self.label_font_size,
                                    verticalalignment='bottom',
                                    font_family='sans-serif', clip_on=False)
        cmin_node = '{:.2e}'.format(min(colour))
        cmax_node = '{:.2e}'.format(max(colour))

        cmap_labels = [f'P.adj:{cmin_node},{cmax_node}', f'G.shared:{min(edge_values)}-{max(edge_values)}']
        # create proxy artists as handles:
        cmaps = [plt.get_cmap(node_cmap), edge_cmap]
        cmap_handles = [Rectangle((0, 0), 1, 1) for _ in cmaps]
        handler_map = dict(zip(cmap_handles,
                               [HandlerColormap(cm, num_stripes=8) for cm in cmaps]))
        legend2 = plt.legend(handles=cmap_handles,
                   labels=cmap_labels,
                   handler_map=handler_map,
                   fontsize=self.axis_font_size, bbox_to_anchor=(0.4, 0.3))

        plt.gca().add_artist(legend2)

        gene_min = int(np.min(self.df[self.size].values))
        gene_mean = int(np.mean(self.df[self.size].values))
        gene_max = int(np.max(self.df[self.size].values))
        gmin = plt.scatter([], [], s=int(np.min(counts)), marker='o', color='#222')
        gmid = plt.scatter([], [], s=int(np.mean(counts)), marker='o', color='#222')
        gmax = plt.scatter([], [], s=int(np.max(counts)), marker='o', color='#222')

        legend = plt.legend((gmin, gmid, gmax),
                   (str(gene_min), str(gene_mean), str(gene_max)),
                   scatterpoints=1,
                   loc='lower left',
                   ncol=1,
                   fontsize=self.axis_font_size, bbox_to_anchor=(0, -0.1))
        legend.set_title("No. Genes")

        plt.gca().add_artist(legend)
        plt.axis("off")