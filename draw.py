from matplotlib import pyplot as plt


def draw_stop():
    plt.ioff()
    plt.show()


class Draw:
    def __init__(self):
        self.buffer = []
        self.fig, self.ax = plt.subplots()
        self.t = []
        self.i = 0
        plt.ion()

    def update(self, data, time):
        self.ax.cla()
        self.ax.set(xlabel='time(s)', ylabel='avg_EAR', title='EAR')
        self.ax.grid()
        self.i = self.i + time
        self.t.append(self.i)
        self.buffer.append(data)
        self.ax.plot(self.t, self.buffer)
        plt.pause(time)

    def save_pic(self, path):
        self.fig.savefig(path)
        print("saved picture to %s" % path)
