import psutil
# import time
def cpu_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_freq    = psutil.cpu_freq()
    cpu_count = psutil.cpu_count()
    cpu_time = psutil.cpu_times()
    def print_detail():
        print ('cpu_precent: ', cpu_percent)
        # time.sleep(0.9)
        print('cpu_freq: ' ,cpu_freq)
        # time.sleep(0.9)
        print('cpu_count: ' ,cpu_count)
        # time.sleep(0.9)
        print('cpu_times: ' ,cpu_time)
        # time.sleep(0.9)

    print_detail()


if __name__ == "__main__":
    cpu_info()

