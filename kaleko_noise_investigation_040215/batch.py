import os

files = [
#(148,317,326),
#(148,337,380),
#(148,394,409),
#(148,417,443),
(149,0,82),
#(147,150,163),
#(150,2,15),
#(150,24,33),
#(150,36,50),
#(150,56,75)
]

for aho in files:    
    os.system("python find_chirping_channels.py %d %d %d"%(aho[0],aho[1],aho[2]))
