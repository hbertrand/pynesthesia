import matplotlib.pyplot as plt
import numpy as np


def __hilbert(x, y, xi, xj, yi, yj, order):
    """
    http://www.fundza.com/algorithmic/space_filling/hilbert/basics/
    """
    if order <= 0:
        return np.array([x + (xi + yi) / 2, y + (xj + yj) / 2])
    else:
        p1 = __hilbert(x, y, yi / 2, yj / 2, xi / 2, xj / 2, order - 1)
        p2 = __hilbert(x + xi / 2, y + xj / 2, xi / 2, xj / 2, yi / 2, yj / 2, order - 1)
        p3 = __hilbert(x + xi / 2 + yi / 2, y + xj / 2 + yj / 2, xi / 2, xj / 2, yi / 2, yj / 2, order - 1)
        p4 = __hilbert(x + xi / 2 + yi, y + xj / 2 + yj, -yi / 2, -yj / 2, -xi / 2, -xj / 2, order - 1)

        return np.vstack((p1, p2, p3, p4))


def hilbert_curve_2d(order):
    return __hilbert(0, 0, 0, 2 ** order, 2 ** order, 0, order)


if __name__ == '__main__':
    hc = hilbert_curve_2d(3)

    plt.plot(hc[:, 0], hc[:, 1])
    plt.show()
