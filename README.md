# Datathon Bill.Com
Project for Rice Datathon 2021 for the Bill.com track

Watch our project presentation here:  https://youtu.be/G81OzCHZa9g

AGLO is a cutting-edge algorithm, based in agglomerative average linkage clustering.  It iteratively clusters each side of a bipartite partition of a graph based on the minimum sum difference in corresponding edge weights between a node and the present candidate clusters on the other side of the graph.  The new clusters are then used to update the graph's candidate clusters.  The algorithm repeats until convregence is observed.

We apply this algorithm to a dataset of business/vendor relationships.  By clustering businesses and vendors based on their transaction histories, we identify similar groups of businesses and of vendors, allowing us to recommend new vendor partners to a business.  The strength of the present relationship between a business and a vendor is described based on the proportion of a business' spending sent to a vendor and the number and value of these transactions.  ALGO successfully clusters similar vendors and businesses, delivering interesting and informative results to stakeholders.
