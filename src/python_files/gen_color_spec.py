#---------
#generating a color spectrum
#---------
#for finding the colormaps associated with the names bellow, refer to the
#following link:
# http://matplotlib.org/examples/color/colormaps_reference.html
import numpy
#from pylab import *
import pylab
import matplotlib.pyplot as plt

cmaps = [('Perceptually Uniform Sequential',
                            ['viridis', 'inferno', 'plasma', 'magma']),
         ('Sequential',     ['Blues', 'BuGn', 'BuPu',
                             'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
                             'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
                             'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd']),
         ('Sequential (2)', ['afmhot', 'autumn', 'bone', 'cool',
                             'copper', 'gist_heat', 'gray', 'hot',
                             'pink', 'spring', 'summer', 'winter']),
         ('Diverging',      ['BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
                             'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral',
                             'seismic']),
         ('Qualitative',    ['Accent', 'Dark2', 'Paired', 'Pastel1',
                             'Pastel2', 'Set1', 'Set2', 'Set3']),
         ('Miscellaneous',  ['gist_earth', 'terrain', 'ocean', 'gist_stern',
                             'brg', 'CMRmap', 'cubehelix',
                             'gnuplot', 'gnuplot2', 'gist_ncar',
                             'nipy_spectral', 'jet', 'rainbow',
                             'gist_rainbow', 'hsv', 'flag', 'prism'])]

def gen_color(n_colors, cmap_name):
    for i in range(n_colors):
        cmap = pylab.get_cmap(cmap_name)
        color = cmap(1.*i/n_colors)  # color will now be an RGBA tuple
        cgen = [cmap(1.*i/n_colors) for i in range(n_colors)]

    return cgen


def test():
    fig, ax = plt.subplots()
    n_colors = 80
    colr_spec = gen_color(n_colors, 'seismic')
    print colr_spec
    
    #--- generate data 
    x = numpy.random.normal(100, 20, n_colors)
    y = numpy.random.normal(100, 20, n_colors)
    l_x = [[el] for el in sorted(x)]
    l_y = [[el] for el in sorted(y)]
    counter = 0  
    for el1, el2 in zip(l_x , l_y):
        ax.scatter(el1, el2, c = colr_spec[counter])
        counter +=1
    plt.show()

def main():
    test()

if __name__ == "__main__":
    main()
