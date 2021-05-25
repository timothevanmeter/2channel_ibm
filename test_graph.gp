

# Used to ignore the first row containing headers
set key autotitle columnhead

set datafile separator ","

set xlabel 'Time step'
set ylabel 'Number of individuals'
# unset key
set key top left
set logscale y


graph_name(n) = sprintf("simulation_%s.png",n)
file_name(n) = sprintf("simulation_%s_output.csv",n)


set terminal pngcairo size 700,500 enhanced font 'Verdana,13'
set output graph_name(sim_num) # 'simulation.png'

plot file_name(sim_num) u 1:2 w lp lw 2 t 'R sp1',\
     '' u 1:3 w lp lw 2 t 'R sp2',\
     '' u 1:5 w lp lw 2 t 'H sp1',\
     '' u 1:6 w lp lw 2 t 'H sp2',\
     '' u 1:7 w lp lw 2 t 'P'
     
     
     # '' u 1:3 w lp lw 2 t 'H ',\
     # '' u 1:4 w lp lw 2 t 'H_sp1',\
     # '' u 1:5 w lp lw 2 t 'H_sp2',\
     # '' u 1:6 w lp lw 2 t 'P',\
     # '' u 1:7 w lp lw 2 t 'P_sp1',\
     # '' u 1:8 w lp lw 2 t 'P_sp2'
