
# copy from  connectivity/200224-compare_PreciseOrRatioOutdegree_RandomClawModel.py
# Fig2D, SFig6A (200326, PNKC2019_v9_fig_200313DB-ZZfixedSuppl6B.pptx)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
%run startup_py3.py
%run load_pn_metadata_v2.py
%run medium_term_functions.py

save_path = "/Users/zhengz11/myscripts/data_results/200224-compare_random_claw_PreciseVSRatio/"

fafb_c = cc.fafb_connection(token)

pn_skids = cc.get_skids_from_annos(
    fafb_c, [['right_calyx_PN'], ['has_bouton']], ["multiglomerular PN"])

rd = cc.get_skids_from_annos(fafb_c,
                             [['Random Draw 1 KC', 'Random Draw 2 KC'], ['Complete']],
                             ['KCaBp', 'KCyd'])

t1p = cc.get_skids_from_annos(fafb_c,
                             [['T1+ Complete']])

'''

ana_all_rd = ar.Analysis.init_connectivity(fafb_c, pn_skids, rd + t1p)


##----------------------------------------------
# observed vs. random claw (ratios, i.e. input_prob summed from the observed connectivity)

num_exp = 1000

conn_data = ana.conn_data['glom_kc_in_claw_unit']
ob_conn, glom_prob, glom_idx_ids = get_conn_prob_idx(conn_data)

input_prob = conn_data.conn['1s'].sum(0)
input_prob = input_prob / sum(input_prob)

stat = [get_raw_inputs(shuffle_glom_kc_w_prob(ob_conn, input_prob)) for i in range(num_exp)]

stat = np.array(stat)
sd = np.nanstd(stat, axis=0)
avg = np.nanmean(stat, axis=0)

ob_ci = get_raw_inputs(ob_conn)

comm_zscore = np.divide(np.subtract(ob_ci, avg), sd)

# clustering
cm_zs = PairMatrix('', comm_zscore, glom_idx_ids)

# reorder_idx = km_cluster(cm_zs.conn)
reorder_idx = reorder(ClusterOrder0707, glom_idx_ids)
t1_zs = cm_zs.reorder(reorder_idx, return_new=True)

# plotting z score matrix
fig, ax1 = plt.subplots()
t1 = t1_zs;
gloms = df_lookup('glom_id',t1.col_ids,'short_glom_name',glom_btn_table)
sns.heatmap(t1.conn, xticklabels=gloms, yticklabels=gloms, ax=ax1, vmin=-8.53, vmax=8.53, cmap="RdBu_r")

ax1.tick_params(bottom=False,labeltop=True, top=True, labelbottom=False)
ax1.tick_params(axis='x',labelrotation=90)

col_list = t1.col_ids
col_colors = df_lookup('short_glom_name', gloms, 'color', tbl)

for x in [ax1.get_xticklabels(), ax1.get_yticklabels()]:
    for idx, tick in enumerate(x):
        tick.set_color(col_colors[idx])
        if col_list[idx] in comm_ids:
            tick.set_weight("extra bold")

ax1.set_aspect("equal")
fig.set_size_inches(16,12)
plt.show()
# fig.savefig(save_path + '200224-compare_random_claw_Precise.png', bbox_inches='tight')

##----------------------------------------------------
## observed vs. random claw (precise) maintain the precise number of claws per PN
# Fig2D
conn_data = ana.conn_data['glom_kc_in_claw_unit']

ob_conn, glom_prob, glom_idx_ids = get_conn_prob_idx(conn_data)

stat = [get_raw_inputs(i) for i in shuffle_glom_kc_iterate(ob_conn, 1000)]

stat = np.array(stat)
sd = np.nanstd(stat, axis=0)
avg = np.nanmean(stat, axis=0)

ob_ci = get_raw_inputs(ob_conn)

comm_zscore = np.divide(np.subtract(ob_ci, avg), sd)

# clustering
cm_zs = PairMatrix('', comm_zscore, glom_idx_ids)

reorder_idx = km_cluster(cm_zs.conn)
# reorder_idx = reorder(ClusterOrder0707, glom_idx_ids)
t1_zs = cm_zs.reorder(reorder_idx, return_new=True)

# plotting z score matrix
fig, ax1 = plt.subplots()
t1 = t1_zs;
gloms = df_lookup('glom_id',t1.col_ids,'short_glom_name',glom_btn_table)
sns.heatmap(t1.conn, xticklabels=gloms, yticklabels=gloms, ax=ax1, vmin=-8.53, vmax=8.53, cmap="RdBu_r")

ax1.tick_params(bottom=False,labeltop=True, top=True, labelbottom=False)
ax1.tick_params(axis='x',labelrotation=90)

col_list = t1.col_ids
col_colors = df_lookup('short_glom_name', gloms, 'color', tbl)

for x in [ax1.get_xticklabels(), ax1.get_yticklabels()]:
    for idx, tick in enumerate(x):
        tick.set_color(col_colors[idx])
        if col_list[idx] in comm_ids:
            tick.set_weight("extra bold")

ax1.set_aspect("equal")
fig.set_size_inches(16,12)
plt.show()
# fig.savefig(save_path + '200228-compare_random_claw_PreciseClawCount_recluster.png', bbox_inches='tight')



##------------------------------------------
# a randomized connectivity (random claw model) against the null model (random claw model)

sfl_conn = shuffle_glom_kc_iterate(ob_conn, 1)[0].copy()

stat = [get_raw_inputs(i) for i in shuffle_glom_kc_iterate(sfl_conn, 1000)]

stat = np.array(stat)
sd = np.nanstd(stat, axis=0)
avg = np.nanmean(stat, axis=0)

ob_ci = get_raw_inputs(sfl_conn)

comm_zscore = np.divide(np.subtract(ob_ci, avg), sd)

# clustering
cm_zs = PairMatrix('', comm_zscore, glom_idx_ids)

reorder_idx = km_cluster(cm_zs.conn)
# reorder_idx = reorder(ClusterOrder0707, glom_idx_ids)
t1_zs = cm_zs.reorder(reorder_idx, return_new=True)

# plotting z score matrix
fig, ax1 = plt.subplots()
t1 = t1_zs;
gloms = df_lookup('glom_id',t1.col_ids,'short_glom_name',glom_btn_table)
sns.heatmap(t1.conn, xticklabels=gloms, yticklabels=gloms, ax=ax1, vmin=-8.53, vmax=8.53, cmap="RdBu_r")

ax1.tick_params(bottom=False,labeltop=True, top=True, labelbottom=False)
ax1.tick_params(axis='x',labelrotation=90)

col_list = t1.col_ids
col_colors = df_lookup('short_glom_name', gloms, 'color', tbl)

for x in [ax1.get_xticklabels(), ax1.get_yticklabels()]:
    for idx, tick in enumerate(x):
        tick.set_color(col_colors[idx])
        if col_list[idx] in comm_ids:
            tick.set_weight("extra bold")

ax1.set_aspect("equal")
fig.set_size_inches(16,12)
plt.show()
# fig.savefig(save_path + '200228-compare_random_claw_PreciseClawCount_recluster_RandomClawAgainstRandomClaw.png', bbox_inches='tight')
