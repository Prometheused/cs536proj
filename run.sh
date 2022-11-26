sudo mn -c > /dev/null 2>&1
sudo mkdir -p results
sudo mkdir -p figures
dir=results
for rtt in 20 50 100 200 500 1000 3000 5000;do
    for bw in 56 256 512 1000 2000 3000 5000 7000;do
        sudo python2 proj3.py --bw $bw --rtt $rtt --init_cwnd 3 --dir $dir
        sudo mn -c > /dev/null 2>&1
        sudo python2 proj3.py --bw $bw --rtt $rtt --init_cwnd 10 --dir $dir
        sudo mn -c > /dev/null 2>&1
    done
done
sudo python2 plot_figures.py
