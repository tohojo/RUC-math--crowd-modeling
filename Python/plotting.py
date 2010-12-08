import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import constants

mpl.rc('font',
        size=11.0,
        serif="Gentium Basic",
        monospace="Inconsolata",
        )
mpl.rcParams['font.sans-serif'] = 'PT Sans'
#mpl.rc('legend',
#        fancybox=True,
#        )

class Plots:

    def __init__(self, sampling_frequency, parameters):
        self.sampling_frequency = sampling_frequency
        self.parameters = parameters

        self.avg_velocities = list()
        self.densities = list()
        self.flowrates = list()
        self.t_values = list()

        self.aggr_avg_velocities = list()
        self.aggr_flowrates = list()
        self.aggr_efficiencies = list()
        self.aggr_leaving_times = list()
        self.aggr_x_values = list()
        self.aggr_x_name = None



    def add_sample(self, t, velocities=None, density=None, flowrate=None):
        self.t_values.append(t)
        self.densities.append(density)
        self.flowrates.append(flowrate)

        self.avg_velocities.append(np.average(velocities))


    def add_aggregate(self, x_name, x_value, desired_velocity=None, leaving_time=None):
        self.aggr_x_name = x_name
        self.aggr_x_values.append(x_value)
        self.aggr_leaving_times.append(leaving_time)

        avg_velocity = np.average(self.avg_velocities)
        self.aggr_efficiencies.append(avg_velocity/desired_velocity)

        self.aggr_avg_velocities.append(avg_velocity)
        self.aggr_flowrates.append(np.average(self.flowrates))

    def _create_plot(self, title, xlabel, ylabel):
        fig = plt.figure()
        fig.set_size_inches(8,4)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        return fig

    def _annotate_plot(self, fig):

        ax = fig.gca()
        param_text = []

        if self.aggr_x_name != "A":
            param_text.append("$A=%.2f$" % self.parameters['A'])
        if self.aggr_x_name != "B":
            param_text.append("$B=%.2f$" % self.parameters['B'])
        if self.aggr_x_name != "U":
            param_text.append("$U=%.2f$" % self.parameters['U'])
        if self.aggr_x_name != "lambda":
            param_text.append("$\lambda=%.2f$" % self.parameters['lambda'])
        if self.aggr_x_name != "velocity_mean":
            param_text.append("mean velocity$=%.2f$" % self.parameters['velocity_mean'])

        leg = fig.gca().legend(loc='best')

        ax.text(0.98, 0.85, "\n".join(param_text),
                transform=ax.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                fontdict={'family': 'serif'},
                bbox = {'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5},
                )




    def _velocity_plot(self):
        fig = self._create_plot("Average actor velocity","t", "m/s")
        plt.plot(self.t_values, self.avg_velocities, label='average velocity')
        self._annotate_plot(fig)
        return fig

    def _aggr_velocity_plot(self):
        fig = self._create_plot("Average actor velocity",self.aggr_x_name, "m/s")
        plt.plot(self.aggr_x_values, self.aggr_avg_velocities, label='average velocity')
        self._annotate_plot(fig)
        return fig

    def _aggr_efficiency_plot(self):
        fig = self._create_plot("Simulation efficiency", 
                self.aggr_x_name, "average velocity / desired velocity")
        plt.plot(self.aggr_x_values, self.aggr_efficiencies, label='efficiency')
        self._annotate_plot(fig)
        return fig

    def _aggr_leaving_time_plot(self):
        fig = self._create_plot("Time to clear room", 
                self.aggr_x_name, "seconds")
        plt.plot(self.aggr_x_values, self.aggr_leaving_times, label='leaving time')
        self._annotate_plot(fig)
        return fig

    def _aggr_flowrate_plot(self):
        fig = self._create_plot("Average flowrate", 
                self.aggr_x_name, "pedestrians/second")
        plt.plot(self.aggr_x_values, self.aggr_flowrates, label='flowrate')
        self._annotate_plot(fig)
        return fig

    def _density_plot(self):
        fig = self._create_plot("Actor density","t","number of actors")
        plt.plot(self.t_values, self.densities, label='density')
        self._annotate_plot(fig)
        return fig

    def _flowrate_plot(self):
        fig = self._create_plot("Flow rate", "t", "actors/second")
        plt.plot(self.t_values, self.flowrates, label='aggregate flowrate')
        self._annotate_plot(fig)
        return fig

    def save(self, prefix):
        velocity_plot = self._velocity_plot()
        velocity_plot.savefig("%s-%s.pdf" % (prefix, "velocity"),
                bbox_inches='tight')

        density_plot = self._density_plot()
        density_plot.savefig("%s-%s.pdf" % (prefix, "density"),
                bbox_inches='tight')

        flowrate_plot = self._flowrate_plot()
        flowrate_plot.savefig("%s-%s.pdf" % (prefix, "flowrate"),
                bbox_inches='tight')

    def save_aggr(self, prefix):
        velocity_plot = self._aggr_velocity_plot()
        velocity_plot.savefig("%s-%s-aggr-%s.pdf" % (prefix, "velocity", 
            self.aggr_x_name),
                bbox_inches='tight')

        efficiency_plot = self._aggr_efficiency_plot()
        efficiency_plot.savefig("%s-%s-aggr-%s.pdf" % (prefix, "efficiency", 
            self.aggr_x_name),
                bbox_inches='tight')

        leaving_time_plot = self._aggr_leaving_time_plot()
        leaving_time_plot.savefig("%s-%s-aggr-%s.pdf" % (prefix, "leaving_time", 
            self.aggr_x_name),
                bbox_inches='tight')

        flowrate_plot = self._aggr_flowrate_plot()
        flowrate_plot.savefig("%s-%s-aggr-%s.pdf" % (prefix, "flowrate", 
            self.aggr_x_name),
                bbox_inches='tight')


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
