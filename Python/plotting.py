import matplotlib.pyplot as plt
import numpy as np

class Plots:

    def __init__(self, sampling_frequency):
        self.sampling_frequency = sampling_frequency

        self.avg_velocities = list()

        self.median_velocities = list()

        self.max_velocities = list()

        self.densities = list()
        self.t_values = list()

    def add_sample(self, t, velocities=None, density=None):
        self.t_values.append(t)
        self.densities.append(density)

        self.avg_velocities.append(np.average(velocities))

        self.median_velocities.append(np.median(velocities))

        self.max_velocities.append(max(velocities))


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
        plt.plot(t, self.avg_velocities, t, self.median_velocities)

        plt.show()

# TODO:
#   * Flow rate, per target
#   * Avg efficiency, pr simulation run
#   * Continous flows of pedestrians (spawning)
#
