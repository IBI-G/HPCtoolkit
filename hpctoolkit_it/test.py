class SampleIterator(object):
    def __init__(self, list: list):
        self.list = list
        self.num = len(list)
        self.current = 0

    def __iter__(self):
        # 一番最初に1回だけ呼ばれる
        print(str(self.current) + "が開始")
        return self

    def __next__(self):
        if not self.current == 0:
            print(str(self.current-1) + "が終了")
            # ここで終了を検知する
        if self.current == self.num:
            raise StopIteration()
        if not self.current == 0:
            print(str(self.current) + "が開始")
        ret = self.list[self.current]
        self.current += 1
        return ret


list = [0, 2, 4]
# si = SampleIterator(range(0, 7, 2))

for i in SampleIterator(range(4)):
    # print("")
    print(str(i) + "が動作中")
    pass
