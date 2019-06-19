'''
    作者信息：'SpringWave'
    本软件的目标就是简化内存 track 难度
'''
import psutil
import tkinter
import re
from tkinter.filedialog import askdirectory
from  tkinter import ttk  
import csv
import datetime
import subprocess
import threading

def thread_it(func, *args):
    t = threading.Thread(target=func, args=args) 
    t.setDaemon(True) 
    t.start()


def getAllProcess():
    return psutil.pids()

def returnProcessNameDict():
    process_dict = {}
    pids = getAllProcess()
    for pid in pids:
        p = psutil.Process(pid)
        try:
            p_name = p.name()
            process_dict[p_name] = pid
        except UnicodeEncodeError:
            pass
    return process_dict

def searchProcess(p_process_dict, search_key):
    result_dict = {}
    new_search_key = search_key.lower()
    for i in p_process_dict:
        process_name = i.lower()
        if search_key in process_name:
            result_dict[i] = p_process_dict[i]
    if not result_dict:
        print("No Result")
        result_dict["No result"] = 0
    return result_dict

def getCertainProcessInfo(p_pid):
    try:
        process = psutil.Process(p_pid)
        used_memory = process.memory_info().rss / 1024 / 1024
        cpu_percent = process.cpu_percent(interval = None)
        test_list = []
        for i in range(100):
            cpu_percent = process.cpu_percent(interval = None)
            test_list.append(cpu_percent)
        cpu_percent = sum(test_list)/100
    except:
        exit()
    return used_memory, cpu_percent
    # print('Used Memory:',process.memory_info().rss / 1024 / 1024,'MB')

def delTreeData(tree):
    x=tree.get_children()
    for item in x:
        tree.delete(item)

def refreshTreeData(tree, data):
    for i in range(len(data)): # 写入数据
        key = list(data.keys())[i]
        treeview.insert('', i, values=(key, data[key]))

def refreshData():
    global process_dict
    delTreeData(treeview)
    process_dict = returnProcessNameDict()
    refreshTreeData(treeview, process_dict)

def selectPath():
    path_ = askdirectory()
    path.set(path_)

def searchProcessBtn():
    delTreeData(treeview)
    text = e1.get()
    result = searchProcess(process_dict, text)
    refreshTreeData(treeview, result)

def treeviewClick(event):
    global chosed_name_str, chosed_pid
    warns.set("")
    for item in treeview.selection():
        item_text = treeview.item(item,"values")
        chosed_name.set("Current selected：\n"+item_text[0])
        # record the process
        chosed_name_str = item_text[0]
        chosed_pid = int(item_text[1])

def run_sub(variables_str):
    subprocess.call('python3 csv_recorder.py ' + variables_str, shell=True)
    warns.set("Tracer process is over, you can choose again now!")

def start_record():
    if chosed_pid == 0:
        warns.set("Haven't set the destination process yet")
        return
    times = int(record_times.get())
    file_path = path.get()
    if not file_path:
        file_path = './'
    filename = file_path + '/' + chosed_name_str + '.csv'
    # first time
    start_time = datetime.datetime.now().isoformat()
    mem, cpu_usage = getCertainProcessInfo(chosed_pid)
    with open(filename, "a" , newline="") as datacsv:
        csvwriter = csv.writer(datacsv,dialect = ("excel"))
        csvwriter.writerow(["RecordTimes","ProcessName","ProcessId","MemoryUsed", "TotalCPUUsage","Start_time"])
        csvwriter.writerow([times,chosed_name_str,chosed_pid,mem, cpu_usage ,start_time])
    s1 = '-'
    variables_str = s1.join([chosed_name_str,str(chosed_pid), filename])
    warns.set("Process tracing subprogram:\n"+ variables_str + "\nis now running")
    thread_it(run_sub, variables_str)
    
    

if __name__ == '__main__':
    process_dict = {}
    chosed_pid = 0
    chosed_name_str = ''
    # GUI
    root = tkinter.Tk(className='The Process Status Watcher')
    root.geometry("600x800+200+200")
    path = tkinter.StringVar()
    photo = tkinter.PhotoImage(file='./logo.png')
    img_label = tkinter.Label(root,image=photo).grid(row = 0, column = 0, sticky=tkinter.W)
    #Title
    label = tkinter.Label(root, text='Process Memory Info Collector',
                      font=("Arial", 15),  
                      fg='black'
    ).grid(row = 0, column = 1, sticky=tkinter.W)

    # choose the saving path
    tkinter.Label(root,text = "Result save path:").grid(row = 1, column = 0, sticky=tkinter.E)
    tkinter.Entry(root, textvariable = path).grid(row = 1, column = 1, sticky=tkinter.W)
    tkinter.Button(root, text = "Open", command = selectPath).grid(row = 1, column = 2, sticky=tkinter.W)
    
    # tree structure
    columns = ("p_name", "PID")
    treeview = ttk.Treeview(root, height=18, show="headings", columns=columns)  # 表格

    treeview.column("p_name", width=200, anchor='center') # 表示列,不显示
    treeview.column("PID", width=100, anchor='center')

    treeview.heading("p_name", text="ProcessName") # 显示表头
    treeview.heading("PID", text="PID")


    treeview.grid(row = 2, rowspan = 2, columnspan = 2, sticky=tkinter.E)
    
    btn_refresh = tkinter.Button(root,text="Refresh\nProcess", command = refreshData, width = 15, height = 5,
    ).grid(row=2, column = 2, sticky=tkinter.W)
    # the chosen process
    chosed_name = tkinter.StringVar()
    label_cname = tkinter.Label(root, textvariable = chosed_name).grid(row=3, column = 2, sticky=tkinter.W)

    treeview.bind('<ButtonRelease-1>', treeviewClick)
    
    # searching 
    e1 = tkinter.Entry(root)
    tkinter.Label(root,text = "Search the process name:").grid(row = 4, column = 0, sticky=tkinter.E)
    e1.grid(row = 4, column = 1, sticky=tkinter.W)
    btn_e = tkinter.Button(root, text = "Search", command = searchProcessBtn).grid(row = 4, column = 2, sticky=tkinter.W)
    
    btn_record = tkinter.Button(root,text="Start record 2 Hour", command = start_record, width = 15, height = 5,
    ).grid(row=5, column = 1, columnspan = 2)
    record_times = tkinter.StringVar()
    record_times.set('0')
    warns = tkinter.StringVar()
    label_warn = tkinter.Label(root, textvariable = warns, font=("Arial", 15),  
                      fg='Red').grid(row=6, column = 1, columnspan = 2, rowspan = 3)

    root.mainloop()