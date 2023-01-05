import numpy as np
import matplotlib.pyplot as plt


class Data:
    def __init__(self, length, n, unwrap=None, labels=None):
        self.array = np.empty((n + 1, length))
        self.n = n
        self.unwrap = unwrap
        self.labels = labels

    array = np.empty((5, 5))
    depth = 0
    n = 6
    unwrap = None
    labels = None
    toPlot = None

    def add_series(self, t, data):
        series = np.array([t])

        if type(data) != "list":
            series = np.append(series, data)
        else:
            for i in data:
                series = np.append(series, i)

        if self.depth >= self.array.shape[1]:
            self.array = np.hstack((self.array, series))
        else:
            self.array[:, self.depth] = series
        self.depth += 1

        if self.unwrap != None:
            for i in self.unwrap:
                self.array[i + 1, :] = np.unwrap(self.array[i + 1, :])

    def get_series(self):
        return self.array[:, self.depth - 1]

    def plot(self, plot=None):

        if plot == None:
            for i in range(self.n):
                if self.labels == None:
                    plt.plot(self.array[0, 0 : self.depth - 1], self.array[i + 1, 0 : self.depth - 1])
                else:
                    plt.plot(
                        self.array[0, 0 : self.depth - 1], self.array[i + 1, 0 : self.depth - 1], label=self.labels[i]
                    )
        else:
            for i in range(len(plot)):
                if self.labels == None:
                    plt.plot(
                        self.array[0, 0 : self.depth - 1],
                        self.array[plot[i] + 1, 0 : self.depth - 1],
                        label=self.labels[i],
                    )
                else:
                    plt.plot(self.array[0, 0 : self.depth - 1], self.array[plot[i] + 1, 0 : self.depth - 1])

        # if labels != None:
        plt.legend()
        plt.show()

    def get_data(self):
        return self.array[:, 0 : self.depth - 1]

    def save(self, path):
        np.savetxt(f"{path}/data.txt", self.array)


if __name__ == "__main__":
    myData = Data(2000, 1, unwrap=[0], labels=["test"])

    # myData.addSeries(1, 2, 3, 4, 5)
    # myData.addSeries(6, 7, 8, 9, 10)

    # myData.addSeries(11, 12, 13, 14, 15)
    # myData.addSeries(16, 17, 18, 19, 20)
    # myData.addSeries(21, 22, 23, 24, 25)

    phase = np.linspace(0.0, 20.0, 1000) % 2 * np.pi

    for i in range(phase.size):
        myData.add_series(i, phase[i])

    myData.plot()
