import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.backends.backend_nbagg import NavigationIPy, FigureManagerNbAgg

BUTTONS = ('Home', 'Back', 'Forward', 'Download')
default_facecolor = matplotlib.rcParams['axes.facecolor']

def on_click(event):
    if event.inaxes and event.button == 1:
        axes = event.inaxes
        sample_index = axes.get_figure().get_axes().index(axes)
        event.canvas.toolbar.selector.toggle_select(sample_index)
        event.canvas.toolbar.set_facecolor(axes.patch, sample_index)
        event.canvas.draw_idle()

class CustomNavigationToolbar(NavigationIPy):
    toolitems = [item for item in NavigationIPy.toolitems if item[0] in BUTTONS]
    selector = None  # filled by SubsetSelector

    def home(self, *args):
        self.selector.home()
        self._update_views()

    def forward(self, *args):
        try:
            self.selector.forward()
        except ValueError:
            self.set_message('No more subsets!')
        self._update_views()

    def back(self, *args):
        try:
            self.selector.back()
        except ValueError:
            self.set_message('Already at home!')
        self._update_views()

    def set_facecolor(self, patch, sample_index):
        facecolor = None
        index = (self.selector.subset_index, sample_index)
        if self.selector.selected[index]:
            facecolor = 'white'
        else:
            facecolor = default_facecolor
        patch.set_facecolor(facecolor)

    def _update_views(self):
        self.canvas.figure.clear()

        nrows = (len(self.selector.ydata[self.selector.subset_index]) + 1)/2
        figure, _ = plt.subplots(nrows, 2, num=self.canvas.figure.number)
        figure.set_size_inches(12, 2*nrows, forward=True)
        for sample_index, ax in enumerate(figure.get_axes()):
            index = (self.selector.subset_index, sample_index)
            line, = ax.plot(self.selector.xdata, self.selector.ydata[index])
            self.set_facecolor(ax.patch, sample_index)

FigureManagerNbAgg.ToolbarCls = CustomNavigationToolbar

class SubsetSelector(object):
    def __init__(self, xdata, ydata):
        self.xdata = xdata
        self.ydata = ydata
        self.selected = np.zeros(ydata.shape[:-1], dtype=bool)
        self.subset_index = 0

    def home(self):
        self.subset_index = 0

    def forward(self):
        new_index = self.subset_index + 1
        if new_index == len(self.ydata):
            raise ValueError
        self.subset_index = new_index

    def back(self):
        new_index = self.subset_index - 1
        if new_index == -1:
            raise ValueError
        self.subset_index = new_index

    def toggle_select(self, sample_index):
        index = (self.subset_index, sample_index)
        if self.selected[index]:
            self.selected[index] = False
        else:
            self.selected[index] = True

    def plot(self):
        figure = plt.figure()
        figure.canvas.mpl_connect('button_press_event', on_click)
        figure.canvas.toolbar.selector = self
        figure.canvas.toolbar._update_views()

    def get_ydata(self):
        return self.ydata[self.selected]
