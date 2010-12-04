import matplotlib.pyplot as plt
import numpy as np

class Plots:

    def __init__(self, sampling_frequency):
        self.sampling_frequency = sampling_frequency

        self.avg_velocities = list()

        self.densities = list()
        self.flowrates = list()
        self.t_values = list()

    def add_sample(self, t, velocities=None, density=None, flowrate=None):
        self.t_values.append(t)
        self.densities.append(density)
        self.flowrates.append(flowrate)

        self.avg_velocities.append(np.average(velocities))


    def show(self):
        t = self.t_values

        plt.figure(1)
        plt.subplot(211)
        plt.xlabel("t")
        plt.ylabel("actors in area")
        plt.title("Density")
        plt.plot(t, self.densities)
        plt.subplot(212)
        plt.xlabel("t")
        plt.ylabel("average velocity")
        plt.title("Velocities")
        plt.plot(t, self.avg_velocities)

        plt.show()

# TODO:
#   * Flow rate, per target
#   * Avg efficiency, pr simulation run
#   * Continous flows of pedestrians (spawning)
#
