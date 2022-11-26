import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

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

def read_all_txt_files(folder_dir):
    cwnd3_array = np.zeros([len(rtt_list),len(bw_list)])
    cwnd10_array = np.zeros([len(rtt_list),len(bw_list)])
    for i in range(len(rtt_list)):
        for j in range(len(bw_list)):
            rtt = rtt_list[i]
            bw = bw_list[j]
            all_num = []
            for cwnd in [3, 10]:
                txt_file = folder_dir + "/cwnd" + str(cwnd) + "_rtt"  + str(rtt) + "_bw" + str(bw) + ".txt"
                mean_num = read_one_txt_file(txt_file)
                if cwnd == 3:
                    cwnd3_array[i][j] = mean_num
                if cwnd == 10:
                    cwnd10_array[i][j] = mean_num

    return (cwnd3_array, cwnd10_array)


def Cal_improvement(cwnd3_array,cwnd10_array,percent_dict,plot_object):
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

    return improve_relative_list


def plot_bar_graph(improve_1,improve_2,improve_3,improve_4,_list,plot_object):
    ax = plt.subplot(111)
    ax.bar(np.arange(len(_list)) + 0.7, improve_1,width=0.2,color='r',align='center',label='response size 2000B')
    ax.bar(np.arange(len(_list)) + 0.9, improve_2,width=0.2,color='b',align='center',label='response size 9000B')
    ax.bar(np.arange(len(_list)) + 1.1, improve_3,width=0.2,color='g',align='center',label='response size 20000B')
    ax.bar(np.arange(len(_list)) + 1.3, improve_4,width=0.2,color='k',align='center',label='response size 40000B')
    ax.set_ylim([0, 50])
    ax.grid()
    ax.set_ylabel('Percentage Improvement')
    ax.set_xticklabels([''] + _list)
    fmt = '%.0f%%'
    yticks = mtick.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(yticks)
    ax.legend(loc="upper right")
    if plot_object == "rtt":
        ax.set_xlabel('RTT (msec)')
        plt.savefig("multiple_responsesize_rtt.png")
    elif plot_object == "bw":
        ax.set_xlabel('Bandwidth (Kbps)')
        plt.savefig("multiple_responsesize_bw.png")
    plt.close()
    


if __name__ == "__main__":
    """ This percent dict is based on the figure5 """
    rtt_bucket_percent_dict = {20: 0.0429, 50: 0.2455, 100: 0.4836, 200: 0.1381, 500: 0.0662, 1000: 0, 3000: 0.007, 5000: 0.0008}
    bw_bucket_percent_dict = {56: 0.0064, 256: 0.0313, 512: 0.1539, 1000: 0.2999, 2000: 0.2834, 3000: 0.1071, 5000: 0.0979, 7000: 0.0201}

    size2000_cwnd3_array, size2000_cwnd10_array = read_all_txt_files("results_2000")
    size9000_cwnd3_array, size9000_cwnd10_array = read_all_txt_files("results_9000")
    size20000_cwnd3_array, size20000_cwnd10_array = read_all_txt_files("results_20000")
    size40000_cwnd3_array, size40000_cwnd10_array = read_all_txt_files("results_40000")

    size2000_improve = Cal_improvement(size2000_cwnd3_array,size2000_cwnd10_array,bw_bucket_percent_dict,"rtt")
    size9000_improve = Cal_improvement(size9000_cwnd3_array,size9000_cwnd10_array,bw_bucket_percent_dict,"rtt")
    size20000_improve = Cal_improvement(size20000_cwnd3_array,size20000_cwnd10_array,bw_bucket_percent_dict,"rtt")
    size40000_improve = Cal_improvement(size40000_cwnd3_array,size40000_cwnd10_array,bw_bucket_percent_dict,"rtt")
    size2000_improve_bw = Cal_improvement(size2000_cwnd3_array,size2000_cwnd10_array,rtt_bucket_percent_dict,"bw")
    size9000_improve_bw = Cal_improvement(size9000_cwnd3_array,size9000_cwnd10_array,rtt_bucket_percent_dict,"bw")
    size20000_improve_bw = Cal_improvement(size20000_cwnd3_array,size20000_cwnd10_array,rtt_bucket_percent_dict,"bw")
    size40000_improve_bw = Cal_improvement(size40000_cwnd3_array,size40000_cwnd10_array,rtt_bucket_percent_dict,"bw")


    print("start plotting different response size for rtt graph")
    plot_bar_graph(size2000_improve,size9000_improve,size20000_improve,size40000_improve,rtt_list,"rtt")
    print("start plotting different response size graph for bandwidth")
    plot_bar_graph(size2000_improve_bw,size9000_improve_bw,size20000_improve_bw,size40000_improve_bw,bw_list,"bw")


