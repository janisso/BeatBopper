#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 18:32:50 2019

@author: mb
"""

import warnings

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# mpl.rc("savefig", dpi=200)
params = {#'figure.dpi' : 200,
          'figure.facecolor' : 'white',
          'axes.axisbelow' : True,
          'font.family' : 'serif',
          'font.serif' : 'Bitstream Vera Serif, New Century Schoolbook, Century Schoolbook L,\
                          Utopia, ITC Bookman, Bookman, Nimbus Roman No9 L, Times New Roman,\
                          Times, Palatino, Charter, serif',
          'lines.antialiased' : True,
          'savefig.facecolor' : 'white'}

for (k, v) in params.iteritems():
    plt.rcParams[k] = v
    
def check_df(x, y, df):
    if isinstance(df, pd.DataFrame):
        if type(x) is str and type(y) is str:
            x = df[x]
            y = df[y]
        else:
            raise TypeError('x and y must be type str')
    else:
        if df is None:
            pass
        else:
            raise TypeError('df must be a pd.DataFrame')
    return (to_nparray(x), to_nparray(y))

def to_nparray(container):
    if type(container) in (list, pd.core.index.Int64Index, pd.Series):
        container = np.array(container)
    elif type(container) is np.ndarray:
        pass
    else:
        raise TypeError('Container must be of type: list, np.ndarray, pd.core.index.Int64Index, or pd.Series')
    return container

def convert_ticks(data, labels):
    if all_ints(data):
        labels = cast_to('int', labels)
    else:
        labels = cast_to('float', labels)
    return labels

def all_ints(data):
    if isinstance(data, pd.DataFrame):
        d_temp = []
        for c in data.columns:
            d_temp = d_temp + data[c].tolist()
        data = d_temp
    if type(data) not in (list, np.ndarray, pd.Series):
        raise TypeError('Container must be of type: list, np.ndarray, or pd.Series')
    return sum([float(v).is_integer() for v in data]) == len(data)

def cast_to(kind=float, labels=None):
    if kind == 'float':
        labels = [round(float(v), 1) for v in labels]
    elif kind == 'int':
        labels = [int(v) for v in labels]
    else:
        raise TypeError('kind must be either float or int')
    return labels

def auto_rotate_xticklabel(fig, ax):
    figw = fig.get_figwidth()
    nticks = len(ax.xaxis.get_majorticklocs())
    tick_spacing = (figw / float(nticks))
    font_size = [v.get_fontsize() for v in ax.xaxis.get_majorticklabels()][0]
    FONT_RATE = 0.01
    char_width = font_size * FONT_RATE
    max_labelwidth = max([len(v.get_text()) for v in ax.xaxis.get_majorticklabels()]) * char_width
    if float(max_labelwidth) / tick_spacing >= 0.90:
        plt.xticks(rotation = 90)
    else:
        pass
    return fig, ax

def range_frame(fontsize, ax, x=None, y=None, dimension='both', is_bar=False):
    PAD = 0.05
    if dimension in ('x', 'both'):
        assert x is not None, 'Must pass in x value'
        xmin = x.min().min()
        xmax = x.max().max()
        xlower = xmin - ((xmax - xmin) * PAD)
        xupper = xmax + ((xmax - xmin) * PAD)
        ax.set_xlim(xmin=xlower, xmax=xupper)
        ax.spines['bottom'].set_bounds(xmin, xmax)
        xlabels = [xl for xl in ax.xaxis.get_majorticklocs() if xl > xmin and xl < xmax]
        xlabels = [xmin] + xlabels + [xmax]
        xlabels = convert_ticks(x, xlabels)
        ax.set_xticks(xlabels)
        ax.set_xticklabels(xlabels, fontsize=fontsize)
    if dimension in ('y', 'both'):
        assert y is not None, 'Must pass in y value'
        ymin = y.min().min()
        ymax = y.max().max()
        ylower = ymin - ((ymax - ymin) * PAD)
        yupper = ymax + ((ymax - ymin) * PAD)
        if is_bar:
            ax.set_ylim(ymin=0, ymax=yupper) 
            ax.spines['left'].set_bounds(0, ymax)
            ylabels = [yl for yl in ax.yaxis.get_majorticklocs() if yl < ymax]
            ylabels = ylabels + [ymax]
        else:
            ax.set_ylim(ymin=ylower, ymax=yupper) 
            ax.spines['left'].set_bounds(ymin, ymax)
            ylabels = [yl for yl in ax.yaxis.get_majorticklocs() if yl > ymin and yl < ymax]
            ylabels = [ymin] + ylabels + [ymax]
        ylabels = convert_ticks(y, ylabels)
        ax.set_yticks(ylabels)
        ax.set_yticklabels(ylabels, fontsize=fontsize)
    return ax


def bar(position, height, df=None, label=None, figsize=(16, 8), align='center', color='LightGray', edgecolor='none', width=0.5, gridcolor='white', ticklabelsize=10):
    position, height = check_df(position, height, df)
    fig, ax = plt.subplots(figsize=figsize)
    #plot_style(ax, plot_type='bar')
    ax.tick_params(axis='both', top='off', bottom='off', left='off', right='off', colors='#4B4B4B', pad=10)
    ax.xaxis.label.set_color('#4B4B4B')
    ax.yaxis.label.set_color('#4B4B4B')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_linewidth(0.75)
    ax.spines['bottom'].set_edgecolor('LightGray')
    ax.bar(position, height, align=align, color=color, edgecolor=edgecolor, width=width)
    xmin = position.min()
    xmax = position.max()
    xlist = ax.xaxis.get_majorticklocs()
    if align is 'center':
        lower_buffer = 0.5
        upper_buffer = 0.5
    elif 'edge':
        lower_buffer = 0.25
        upper_buffer = width + 0.25
    xlist = [xl for xl in ax.xaxis.get_majorticklocs() if xl >= xmin and xl <= xmax]
    xlist = [xmin - lower_buffer] + xlist[1:-1] + [xmax + upper_buffer]
    yticklocs = ax.yaxis.get_majorticklocs()
    yticklocs = convert_ticks(height, yticklocs)
    for y in yticklocs:
        ax.plot([xlist[0], xlist[-1]], [y, y], color=gridcolor, linewidth=1.25)
    ax.set_xlim(xmin=xlist[0], xmax=xlist[-1])
    if label is None:
        pass
    elif type(label) in (list, np.ndarray, pd.Series):
        label = np.array([str(lab) for lab in label])
        if len(label) == len(position):
            ax.set_xticks(position)
            ax.set_xticklabels(label)
            fig, ax = auto_rotate_xticklabel(fig, ax)
        else:
            raise ValueError('Labels must have the same first dimension as position and height')
    else:
        raise ValueError('Labels must be in: list, np.ndarray, or pd.Series')
    ax = range_frame(ticklabelsize, ax, x=None, y=height, dimension='y', is_bar=True)
    return fig, ax

bar(range(10),
          np.random.randint(1, 25, 10),
          label=['First', 'Second', 'Third', 'Fourth', 'Fifth',
                 'Sixth', 'Seventh', 'Eight', 'Ninth', 'Tenth'],
          figsize=(8, 4))