import csv
import psutil
import time
import sys
import datetime

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
        return used_memory, cpu_percent
    except:
        exit()

def record():
    print("Next time record")
    new_time = datetime.datetime.now().isoformat()
    mem, cpu_usage = getCertainProcessInfo(p_pid)
    with open(filename, "a" , newline="") as datacsv:
        csvwriter = csv.writer(datacsv,dialect = ("excel"))
        csvwriter.writerow([times, p_name, p_pid, mem, cpu_usage, new_time])


if __name__ == '__main__':
    all_v = sys.argv[1]
    # print(variables)
    variables = all_v.split('-')
    p_name = variables[0]
    p_pid = int(variables[1])
    filename = variables[2]
    total_record_time = int(variables[3]) * 60 * 60
    record_total = int(variables[4])
    times = 1
    # 2 h = 6 * 2 = 12 times
    # total record 2 hour = 2 * 60 * 60
    # total_record_time = 2 * 60 * 60
    # record_total = 24
    for i in range(record_total):
        time.sleep(total_record_time / record_total) # record 10 min per period
        # time.sleep(4)
        record()
        times += 1