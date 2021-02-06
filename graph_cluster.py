import pandas as pd
import numpy as np
import random


def build_clusters(set_grouping, n_nodes, edge_matrix, n_clusters, boolClusterAgency):
    # bool cluster agency indicates whether agencies are being clustered (1) or vendors (0)

    rho = .0003 #cluster size regularization parameter

    new_clusters = np.arange(n_nodes)
    new_cluster_groupings = [[i] for i in range(n_nodes)]

    #generate average weight from set_grouping to nodes
    cluster_weights = np.zeros([len(set_grouping), n_nodes])
    for cluster_num in range(len(set_grouping)):
        for part in set_grouping[cluster_num]:
            node_indices = np.where(edge_matrix[:, boolClusterAgency] == part)
            for edge_idx in node_indices[0]:
                cluster_weights[cluster_num, int(edge_matrix[edge_idx, 1 - boolClusterAgency])] += edge_matrix[
                                                                                                       edge_idx, 2] / len(
                    set_grouping[cluster_num])

    #compute pairwise distances
    node_similarity_matrix = 10000 * np.ones([n_nodes, n_nodes])
    for node1 in range(n_nodes):
        # for node2 in range(node1 + 1,n_nodes):
        for node2 in range(node1 + 1, n_nodes):
            node_similarity_matrix[node1, node2] = np.mean(
                np.abs((cluster_weights[:, node1] - cluster_weights[:, node2])))
            node_similarity_matrix[node2, node1] = np.mean(
                np.abs((cluster_weights[:, node1] - cluster_weights[:, node2])))
        # if node1 % 10 == 0:
        #    print(str(node1) + "/" + str(n_nodes))\


    print("Processing Done")

    total_clusters = n_nodes

    #combine nearest clusteres
    while True:

        (node1, node2) = np.unravel_index(np.argmin(node_similarity_matrix), node_similarity_matrix.shape)
        rm_cluster = new_clusters[node2]
        add_cluster = new_clusters[node1]

        # for rm_node in new_cluster_groupings[rm_cluster]:
        #    new_clusters[rm_node] = add_cluster
        #    for ad_node in new_cluster_groupings[add_cluster]:
        #        node_similarity_matrix[ad_node, rm_node] = 0
        #        node_similarity_matrix[rm_node, ad_node] = 0

        node_similarity_matrix[node1, :] = (len(new_cluster_groupings[rm_cluster]) * node_similarity_matrix[node2,:] + len(new_cluster_groupings[add_cluster]) * node_similarity_matrix[node1, :]) / (len(new_cluster_groupings[add_cluster]) + len(new_cluster_groupings[rm_cluster])) + rho * ((len(new_cluster_groupings[add_cluster]) + len(new_cluster_groupings[rm_cluster])) * n_clusters / n_nodes) ** 2
        node_similarity_matrix[:, node1] = (len(new_cluster_groupings[rm_cluster]) * node_similarity_matrix[:,node2] + len(new_cluster_groupings[add_cluster]) * node_similarity_matrix[:, node1]) / (len(new_cluster_groupings[add_cluster]) + len(new_cluster_groupings[rm_cluster])) + rho * ((len(new_cluster_groupings[add_cluster]) + len(new_cluster_groupings[rm_cluster])) * n_clusters / n_nodes) ** 2

        node_similarity_matrix[node2, :] = 10000
        node_similarity_matrix[:, node2] = 10000

        for rm_node in new_cluster_groupings[rm_cluster]:
            new_clusters[rm_node] = add_cluster

            for ad_node in new_cluster_groupings[add_cluster]:
                node_similarity_matrix[ad_node, rm_node] = 10000
                node_similarity_matrix[rm_node, ad_node] = 10000

        new_cluster_groupings[add_cluster].extend(new_cluster_groupings[rm_cluster])
        new_cluster_groupings[rm_cluster] = []


        total_clusters -= 1

        if n_clusters >= total_clusters:

            final_clusters, final_cluster_groupings = build_cluster_sets_vector(new_clusters)

            return final_clusters, final_cluster_groupings


def build_cluster_sets_vector(set_ids):

    #removee empty clusters and reset indexing
    unique_sets = np.unique(set_ids)
    cluster_sets = [[] for i in range(len(unique_sets))]
    new_set_ids = np.zeros(len(set_ids), )
    for i in range(len(unique_sets)):
        indices = np.where(set_ids == unique_sets[i])
        cluster_sets[i].extend(indices[0])
        new_set_ids[indices] = i

    return new_set_ids, cluster_sets

def cluster(n_agency, n_vendors, edge_matrix, iter, init_vendor_cluster = None):
    #n_agency - number of agencies
    #n_vendors - number of vendors
    #edge_matrix - matrix of [agency node index, vendor node index, edge weight]
    #iter - number of clustering iterations to run
    #init_vendor_cluster


    vendor_cluster_groupings = init_vendor_cluster
    if init_vendor_cluster == None:
        vendor_cluster_groupings = [[i] for i in range(n_vendors)]

    for i in range(iter):
        print("Iteration " + str(i))

        agency_clusters, agency_cluster_groupings = build_clusters(vendor_cluster_groupings, n_agency, edge_matrix, 15, 1)

        vendor_clusters, vendor_cluster_groupings = build_clusters(agency_cluster_groupings, n_vendors, edge_matrix, 100, 0)

    return agency_clusters, agency_cluster_groupings, vendor_clusters, vendor_cluster_groupings