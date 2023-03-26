import multiprocessing
# import psutil
import datetime
import time
# import numpy as np


class HPCToolkit(object):
    def __init__(self, EsN0: list, SIM: object):
        self.EsN0 = EsN0
        self.num = len(EsN0)
        self.EsN0_idx = 0
        self.path = 'progress_bar.txt'
        self.cpu_count = get_spec1()
        self.start_time = get_start_time()
        self.nworker = SIM.nworker
        self.process_start_time_list = [['' for i in range(1)] for j in range(self.nworker)]
        self.process_finish_time_list = [['' for i in range(1)] for j in range(self.nworker)]
        self.lock = SIM.lock
        self.process_idx = SIM.process_idx
        # 初期値書き込み
        self.write_initial(self.get_str_spec(self.nworker))

    def __iter__(self):
        # 一番最初に1回だけ呼ばれる
        # print(str(self.current) + "が開始")
        self.start(self.process_idx, 0)
        return self

    def __next__(self) -> float:
        if not self.EsN0_idx == 0:
            # print(str(self.current-1) + "が終了")
            self.finish(self.process_idx, self.EsN0_idx-1)
            # ここで終了を検知する
        if self.EsN0_idx == self.num:
            raise StopIteration()
        if not self.EsN0_idx == 0:
            # print(str(self.EsN0_idx) + "が開始")
            self.start(self.process_idx, self.EsN0_idx)
        ret = self.EsN0[self.EsN0_idx]
        self.EsN0_idx += 1
        return ret

    def start(self, process_idx: int, EsN0_idx: int):
        if EsN0_idx == 0:
            self.process_start_time_list[process_idx][EsN0_idx] = time.time()
        else:
            self.process_start_time_list[process_idx].append(time.time())
        # self.process_start_time_ndarray[process_idx, EsN0_idx] = time.time()

    def finish(self, process_idx: int, EsN0_idx: int):
        if EsN0_idx == 0:
            self.process_finish_time_list[process_idx][EsN0_idx] = time.time()
        else:
            self.process_finish_time_list[process_idx].append(time.time())
        # self.process_finish_time_ndarray[process_idx, EsN0_idx] = time.time()
        # average_time = np.mean(self.process_finish_time_ndarray[process_idx, :] - self.process_start_time_ndarray[process_idx, :])
        diff_time_list = [x - y for x, y in zip(self.process_finish_time_list[process_idx], self.process_start_time_list[process_idx])]
        average_time = sum(diff_time_list) / len(diff_time_list)
        d, h, m, s = get_d_h_m_s(float(average_time))
        average_time_text = str(d) + "d " + str(h) + "h " + str(m) + "m " + str(s) + "s" + "/iter"
        text = str(process_idx) + " " + progressbar(EsN0_idx, len(self.EsN0)-1) + " " + average_time_text + "\n"
        self.write_finish_process(process_idx, text)

    def write_initial(self, text: str):
        with open(self.path, mode='w') as f:
            f.write(text)

    def write_finish_process(self, process_idx: int, string: str):
        self.lock.acquire()
        with open(self.path) as file:
            text_list = file.readlines()
        text_list[process_idx + 5] = string
        with open(self.path, mode='w') as f:
            f.writelines(text_list)
        self.lock.release()

    def get_str_spec(self, nwoker: int) -> str:
        start_text = "Start: " + self.start_time
        expect_text = "Expect: "
        cpu_count_text = "Active core: " + str(self.cpu_count)
        nwoker_text = "Process: " + str(nwoker)
        progress_bar_text = ""
        for i in range(self.nworker):
            progress_bar_text += str(i) + " " + progressbar(0, len(self.EsN0)) + "\n"
        return start_text + "\n" + expect_text + "\n" + cpu_count_text + "\n" + nwoker_text + "\n\n" + progress_bar_text


def get_spec1() -> int:
    cpu_count = multiprocessing.cpu_count()  # 論理コアの数
    return cpu_count


def get_start_time() -> str:
    dt_now = datetime.datetime.now()
    start_time_month = str(dt_now.month)
    start_time_day = str(dt_now.day)
    start_time_hour = str(dt_now.hour)
    start_time_minute = str(dt_now.minute)
    if dt_now.minute < 10:
        start_time_minute = "0" + str(dt_now.minute)
    start_time = start_time_month + "/" + start_time_day + " " + start_time_hour + ":" + start_time_minute
    return start_time


def progressbar(current, max) -> str:
    ratio = current / max
    length = 20
    progress = int(ratio * length)
    bar = f'[{"■" * progress}{"□" * (length - progress)}]'
    percentage = int(ratio * 100)
    return f'{bar} {percentage}%'


def get_d_h_m_s(sec: float) -> tuple:
    td = datetime.timedelta(seconds=sec)
    m, s = divmod(td.seconds, 60)
    h, m = divmod(m, 60)
    d = td.days
    return d, h, m, s
