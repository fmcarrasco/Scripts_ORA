import numpy as np
import matplotlib.colors as c

def escala_tmax():
    c_pp = np.asarray([(128., 128., 126.), (51., 103., 151.), (51., 103., 101.),
                       (0., 103., 50.), (75., 114., 49.), (153., 128., 48.),
                       (177., 166., 48.), (204., 205., 49.), (229., 230., 100.),
                       (255., 255., 149.), (255., 232., 152.), (255., 206., 150.),
                       (254., 181., 126.), (255., 154., 100.), (255., 130., 74.),
                       (254., 103., 48.), (203., 52., 23.), (153., 1., 0.)])/255.
    cMap = c.ListedColormap(c_pp)
    bounds = np.array([-15., 10., 12., 14., 16., 18., 20., 22., 24., 26., 28., 30.,
                        32., 34., 36., 38., 40., 42., 100.])
    norm = c.BoundaryNorm(boundaries=bounds, ncolors=len(c_pp))

    return c_pp, cMap, bounds, norm


def escala_tmin():
    c_pp = np.asarray([(152., 52., 202.), (204., 53., 254.), (204., 104., 254.),
                       (205., 155., 254.), (204., 206., 254.), (231., 232., 227.),
                       (154., 206., 202.), (102., 154., 152.), (51., 103., 101.),
                       (0., 103., 50.), (102., 102., 50.), (153., 103., 50.),
                       (204., 103., 49.), (254., 103., 48.), (255., 1., 1.),
                       (153., 1., 0.)])/255.
    cMap = c.ListedColormap(c_pp)
    bounds = np.array([-100., -8., -6., -4., -2., 0., 2., 4., 6., 8., 10., 12., 14., 16., 18., 20., 100.])
    norm = c.BoundaryNorm(boundaries=bounds, ncolors=len(c_pp))

    return c_pp, cMap, bounds, norm


def escala_pp():
    c_pp = np.asarray([(255., 255., 251.), (255., 255., 201.), (231., 232., 227.),
                       (180., 180., 178.), (128., 128., 126.), (102., 154., 152.),
                       (154., 206., 202.), (155., 255., 255.), (204., 206., 254.),
                       (152., 154., 254.), (102., 103., 255.), (101., 103., 203.),
                       (0., 51., 152.), (1., 1., 101.), (101., 51., 0.), (153., 1., 0.),
                       (203., 51., 1.), (255., 1., 1.), (255., 0., 99.), (255., 103., 150.),
                       (248., 158., 246.), (150., 0., 150.)])/255.
    cMap = c.ListedColormap(c_pp)
    bounds = np.array([0., 1., 10., 20., 30., 40., 50., 60., 70., 80., 90., 100.,
                           110., 120., 130., 140., 150., 160., 170., 180., 190., 200.,
                           1000.])
    norm = c.BoundaryNorm(boundaries=bounds, ncolors=len(c_pp))

    return c_pp, cMap, bounds, norm

def escala_aa():
    c_pp = np.asarray([(154., 154., 152.), (102., 103., 255.), (152., 154., 254.),
                       (204., 206., 254.), (155., 255., 255.), (205., 255., 204.),
                       (255., 255., 149.), (255., 206., 150.), (255., 154., 48.),
                       (254., 103., 48.), (203., 51., 1.), (152., 53., 100.)])/255.
    cMap = c.ListedColormap(c_pp)
    bounds = np.array([-100., -10., -8., -6., -4., -2., 0., 2., 4., 6., 8., 10., 100])
    norm = c.BoundaryNorm(boundaries=bounds, ncolors=len(c_pp))

    return c_pp, cMap, bounds, norm


def escala_aa_extremas():
    c_pp = np.asarray([(0., 112., 255.), (255., 255., 251.), (255., 170., 0.)])/255.
    cMap = c.ListedColormap(c_pp)
    bounds = np.array([-100., -3., 3., 100])
    norm = c.BoundaryNorm(boundaries=bounds, ncolors=len(c_pp))

    return c_pp, cMap, bounds, norm


def escala_tmin_extremas():
    c_pp = np.asarray([(76., 0., 115., 0.5*255.), (158., 170., 215., 0.5*255.), (255., 255., 255., 255.)])/255.
    cMap = c.ListedColormap(c_pp)
    bounds = np.array([-100., 0., 3., 100])
    norm = c.BoundaryNorm(boundaries=bounds, ncolors=len(c_pp))

    return c_pp, cMap, bounds, norm


def escala_tmax_extremas():
    c_pp = np.asarray([(255., 255., 255.), (255., 170., 0.), (168., 0., 0.)])/255.
    cMap = c.ListedColormap(c_pp)
    bounds = np.array([-100., 35., 40., 100])
    norm = c.BoundaryNorm(boundaries=bounds, ncolors=len(c_pp))

    return c_pp, cMap, bounds, norm

def escala_aa_pp():
    c_pp = np.asarray([(101., 51., 0.), (153., 103., 50.), (203., 154., 49.),
                       (255., 154., 48.), (255., 205., 0.), (153., 206., 152.),
                       (155., 255., 255.), (154., 206., 202.), (102., 154., 152.),
                       (51., 103., 101.)])/255.
    cMap = c.ListedColormap(c_pp)
    bounds = np.array([-2000., -200., -150., -100., -50., 0., 50., 100., 150., 200., 2000])
    norm = c.BoundaryNorm(boundaries=bounds, ncolors=len(c_pp))

    return c_pp, cMap, bounds, norm

def escala_palmer():
    c_pp = np.asarray([(97., 49., 0.), (155., 100., 46.), (207., 101., 46.),
                       (255., 99., 46.), (255., 157., 46.), (254., 208., 0.),
                       (255., 255., 155.), (255., 255., 251.), (205., 255., 96.),
                       (155., 207., 97.), (99., 157., 47.), (49., 99., 98.),
                       (0., 50., 155.), (1., 1., 99.), (49., 49., 47.)])/255.
    cMap = c.ListedColormap(c_pp)
    bounds = np.array([-50., -6., -5., -4., -3., -2., -1., -0.5, 0.5, 1., 2., 3., 4., 5., 6., 50])
    norm = c.BoundaryNorm(boundaries=bounds, ncolors=len(c_pp))

    return c_pp, cMap, bounds, norm


def escala_mapa_control_extr_pp():
    c_pp = np.asarray([(255., 255., 255., 255. ), (0., 255., 0., 0.), (169., 0., 230., 0.)])/255.
    cMap = c. ListedColormap(c_pp)
    bounds = np.array([-1000, 249.9999, 300, 1000.])
    norm = c.BoundaryNorm(boundaries=bounds, ncolors=len(c_pp))

    return c_pp, cMap, bounds, norm


def escala_mapa_control_extr_tmax():
    c_pp = np.asarray([(0., 197., 255., 0.), (255., 170., 0., 0.), (255., 255., 255., 255. ), (230., 0., 0., 0.)])/255.
    cMap = c. ListedColormap(c_pp)
    bounds = np.array([-1000, 0., 5., 45.,1000.])
    norm = c.BoundaryNorm(boundaries=bounds, ncolors=len(c_pp))

    return c_pp, cMap, bounds, norm


def escala_mapa_control_extr_tmin():
    c_pp = np.asarray([(0., 112., 255., 0.), (155., 223., 255., 0.), (255., 255., 255., 255. ), (255., 170., 0., 0.)])/255.
    cMap = c. ListedColormap(c_pp)
    bounds = np.array([-1000, -20., -15., 25.,1000.])
    norm = c.BoundaryNorm(boundaries=bounds, ncolors=len(c_pp))

    return c_pp, cMap, bounds, norm
