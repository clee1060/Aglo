import pandas as pd
import numpy as np
import graph_cluster

df = pd.read_csv('Purchase_Card_Transactions.csv')

full_vendors = False #whether to use vendor descriptions (MCC_DESCRIPTION) or full vendor names

if full_vendors:

    df_group = df.groupby(['VENDOR_NAME', 'AGENCY'])['TRANSACTION_AMOUNT'].agg(['sum', 'count'])
    df_numpy = df_group.to_numpy()

    agency_spending = df.groupby(['AGENCY'])['TRANSACTION_AMOUNT'].agg(['sum']).reset_index()

    hash_a = {}
    list_a = []
    a_val = 0
    hash_v = {}
    v_val = 0
    list_v = []
    ret_list = []

    for i in range(round(len(df_numpy) / 40)):
        #add vendor/agency names to lists
        a_name = df_group.iloc[i].name[1]
        v_name = df_group.iloc[i].name[0]
        if a_name not in hash_a:
            hash_a[a_name] = a_val
            a_val += 1
            list_a.append(a_name)
        if v_name not in hash_v:
            hash_v[v_name] = v_val
            v_val += 1
            list_v.append(v_name)
        s = df_numpy[i][0]
        # print(agency_spending[agency_spending["AGENCY"]==a_name].reset_index()['sum'][0])

        #add edge to matrix
        ret_list.append([hash_a[a_name], hash_v[v_name],
                         abs(s) / agency_spending[agency_spending["AGENCY"] == a_name].reset_index()['sum'][0]])

else:
    df_group = df.groupby(['AGENCY', 'MCC_DESCRIPTION'])['TRANSACTION_AMOUNT'].agg(['sum', 'count'])
    df['MCC_DESCRIPTION'] = df['MCC_DESCRIPTION'].apply(lambda x: str(x).replace('-', ' ').upper())
    df_numpy = df_group.to_numpy()

    agency_spending = df.groupby(['AGENCY'])['TRANSACTION_AMOUNT'].agg(['sum']).reset_index()

    hash_a = {}
    list_a = []
    a_val = 0
    hash_v = {}
    v_val = 0
    list_v = []
    ret_list = []

    for i in range(len(df_numpy)):
        # add vendor/agency names to lists
        a_name = df_group.iloc[i].name[0]
        v_name = df_group.iloc[i].name[1]
        if a_name not in hash_a:
            hash_a[a_name] = a_val
            a_val += 1
            list_a.append(a_name)
        if v_name not in hash_v:
            hash_v[v_name] = v_val
            v_val += 1
            list_v.append(v_name)
        s = df_numpy[i][0]

        # add edge to matrix
        ret_list.append([hash_a[a_name], hash_v[v_name], abs(s)/agency_spending[agency_spending["AGENCY"]==a_name].reset_index()['sum'][0]])


ag_cluster, ag_groups, v_cluster, v_groups = graph_cluster.cluster(len(list_a), len(list_v), np.array(ret_list), 1, init_vendor_cluster = None)

for i in range(len(ag_groups)):
    print("\nAgency Group " + str(i+1))
    for idx in ag_groups[i]:
        print(list_a[idx])

for i in range(len(v_groups)):
    print("\nVendor Group " + str(i+1))
    for idx in v_groups[i]:
        print(list_v[idx])

print("Done!")