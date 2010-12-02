import matplotlib.pyplot as plt
import numpy as np

class Plots:

    def __init__(self, sampling_frequency):
        self.sampling_frequency = sampling_frequency

        self.avg_pressures = list()
        self.avg_velocities = list()

        self.median_pressures = list()
        self.median_velocities = list()

        self.max_pressures = list()
        self.max_velocities = list()

        self.densities = list()
        self.t_values = list()

    def add_sample(self, t, pressures=None, velocities=None,
            density=None):
        self.t_values.append(t)
        self.densities.append(density)

        self.avg_velocities.append(np.average(velocities))
        self.avg_pressures.append(np.average(pressures))

        self.median_velocities.append(np.median(velocities))
        self.median_pressures.append(np.median(pressures))

        self.max_velocities.append(max(velocities))
        self.max_pressures.append(max(pressures))


    def show(self):
        t = self.t_values

        plt.figure(1)
        plt.subplot(211)
        plt.xlabel("t")
        #plt.ylabel("actors in area")
        plt.title("Density and pressure")
        plt.plot(t, self.densities, t, self.avg_pressures, t, self.median_pressures)
        plt.subplot(212)
        plt.xlabel("t")
        plt.ylabel("average velocity")
        plt.title("Velocities")
        plt.plot(t, self.avg_velocities, t, self.median_pressures)
#        plt.subplot(213)
#        plt.xlabel("t")
#        plt.ylabel("average pressure")
#        plt.title("Pressure")
#        plt.plot(t, avg_pressures)

        plt.show()
