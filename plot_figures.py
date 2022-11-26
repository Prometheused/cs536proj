import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

rtt_list = [20, 50, 100, 200, 500, 1000, 3000, 5000]
bw_list = [56, 256, 512, 1000, 2000, 3000, 5000, 7000]

def read_one_txt_file(txt_file):
    f = open(txt_file,"r")
    all_num = []
    for line in f:
        data = line.rsplit()
        all_num.append(float(data[0]))
    mean_num = np.mean(all_num)
    return mean_num

def read_all_txt_files():
    cwnd3_array = np.zeros([len(rtt_list),len(bw_list)])
    cwnd10_array = np.zeros([len(rtt_list),len(bw_list)])
    for i in range(len(rtt_list)):
        for j in range(len(bw_list)):
            rtt = rtt_list[i]
            bw = bw_list[j]
            all_num = []
            for cwnd in [3, 10]:
                txt_file = "results/cwnd" + str(cwnd) + "_rtt"  + str(rtt) + "_bw" + str(bw) + ".txt"
                mean_num = read_one_txt_file(txt_file)
                if cwnd == 3:
                    cwnd3_array[i][j] = mean_num
                if cwnd == 10:
                    cwnd10_array[i][j] = mean_num

    return (cwnd3_array, cwnd10_array)

def plot_bar_graph(cwnd3_array,cwnd10_array,percent_dict, plot_object):
    improve_abs_list = []
    improve_relative_list = []
    if plot_object == "rtt":
        list1 = rtt_list 
        list2 = bw_list 
    if plot_object == "bw":
        list1 = bw_list
        list2 = rtt_list
        cwnd3_array = np.transpose(cwnd3_array)
        cwnd10_array = np.transpose(cwnd10_array)
    for i in range(len(list1)):
        improve_abs_all = 0
        improve_base_all = 0
        improve_relative_all = 0
        for j in range(len(list2)):
            improve_abs_one = (cwnd3_array[i][j] - cwnd10_array[i][j]) * percent_dict[list2[j]]
            improve_base_one = cwnd3_array[i][j] * percent_dict[list2[j]]
            improve_abs_all += improve_abs_one
            improve_base_all += improve_base_one

        improve_abs_list.append(improve_abs_all*1000/sum(percent_dict.values()))
        improve_relative_list.append((float(improve_abs_all)/improve_base_all)*100)

    fig, ax_abs = plt.subplots()
    ax_relative = ax_abs.twinx()
    bar_abs = ax_abs.bar(np.arange(len(list1)) + 0.85, improve_abs_list, 0.3, color='red', log=True)
    bar_relative = ax_relative.bar(np.arange(len(list1)) + 1.15,improve_relative_list,0.3, color='blue')
    ax_abs.set_ylim([1,10000])
    ax_relative.set_ylim([0, 50])
    ax_abs.grid()
    ax_abs.set_ylabel('Improvement (ms)')
    ax_abs.set_yticklabels([0,1,10,100,1000,10000])
    ax_abs.set_xticklabels([''] + list1)
    ax_abs.legend((bar_abs[0],bar_relative[0]), ('Absolute Improvement', 'Percentage Improvement'), loc= "upper center")

    if plot_object == "rtt":
        ax_abs.set_xlabel('RTT (msec)')
        plt.savefig('figures/figure5_rtt.png')
    if plot_object == "bw":
        ax_abs.set_xlabel('Bandwidth (Kbps)')
        plt.savefig('figures/figure5_bw.png')

    plt.close()

if __name__ == "__main__":
    cwnd3_array, cwnd10_array = read_all_txt_files()
    """ This percent dict is based on the figure5 """
    rtt_bucket_percent_dict = {20: 0.0429, 50: 0.2455, 100: 0.4836, 200: 0.1381, 500: 0.0662, 1000: 0, 3000: 0.007, 5000: 0.0008}
    bw_bucket_percent_dict = {56: 0.0064, 256: 0.0313, 512: 0.1539, 1000: 0.2999, 2000: 0.2834, 3000: 0.1071, 5000: 0.0979, 7000: 0.0201}
    print("start plotting RTT graph for Figure 5")
    plot_bar_graph(cwnd3_array, cwnd10_array, bw_bucket_percent_dict,"rtt")
    print("start plooting BW graph for Figure 5")
    plot_bar_graph(cwnd3_array, cwnd10_array, rtt_bucket_percent_dict,"bw")
