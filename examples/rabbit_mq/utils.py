import os
import pandas as pd
def mysplit(s):
    head = s.lstrip('0123456789.')
    tail = s[:-len(head)]
    return (head, tail)

def to_csv():
    cpu     = []
    memory = []
    mem_percent = []    
    netIn= []
    netOut = []
    blockingIn= []
    blockOut= []
    Pids= []
    for filename in os.listdir():
        if "logs" in filename:
            with open(filename) as f:
                lines = f.readlines()
                for idx,line in enumerate(lines, start = 0):
                    if "mn.server" in line and "--" not in line:
                        data = line.split(" ")

                        while '' in data:
                            data.remove('')

                        cpu.append(mysplit(data[2]))
                        memory.append(mysplit(data[3]))
                        mem_percent.append(mysplit(data[6]))
                        netIn.append(mysplit(data[7]))
                        netOut.append(mysplit(data[9]))
                        blockingIn.append(mysplit(data[10]))
                        blockOut.append(mysplit(data[12]))
                        Pids.append(mysplit(data[13]))
    df = pd.DataFrame({"cpu":cpu})
    df["memory"]=memory 
    df["memory_percent"]=mem_percent 
    df["netIn"]=netIn 
    df["netOut"]=netOut 
    df["blocksIN"]=blockingIn 
    df["blocksout"]=blockOut 
    df["Pids"]=Pids
    df.to_csv("logs.csv", index=False)



