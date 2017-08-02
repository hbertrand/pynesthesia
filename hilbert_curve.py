import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import imread, imresize

from music import write_wav, convert_to_sound


def __hilbert(x, y, xi, xj, yi, yj, order):
    """
    http://www.fundza.com/algorithmic/space_filling/hilbert/basics/
    """
    if order <= 0:
        return np.array([x + (xi + yi) // 2, y + (xj + yj) // 2])
    else:
        p1 = __hilbert(x, y, yi / 2, yj / 2, xi / 2, xj / 2, order - 1)
        p2 = __hilbert(x + xi / 2, y + xj / 2, xi / 2, xj / 2, yi / 2, yj / 2, order - 1)
        p3 = __hilbert(x + xi / 2 + yi / 2, y + xj / 2 + yj / 2, xi / 2, xj / 2, yi / 2, yj / 2, order - 1)
        p4 = __hilbert(x + xi / 2 + yi, y + xj / 2 + yj, -yi / 2, -yj / 2, -xi / 2, -xj / 2, order - 1)

        return np.vstack((p1, p2, p3, p4))


def hilbert_curve_2d(order):
    return __hilbert(0, 0, 0, 2 ** order, 2 ** order, 0, order).astype(int)


def plot_hilbert_curve_2d(order):
    hc = hilbert_curve_2d(order)

    plt.plot(hc[:, 0], hc[:, 1])
    plt.show()


def flatten_array(arr):
    assert arr.shape[0] == arr.shape[1]
    order = np.log2(arr.shape[0])
    assert order == int(order)

    hc = hilbert_curve_2d(order)
    flat_arr = [arr[i, j] for i, j in hc]
    return flat_arr


if __name__ == '__main__':
    plot_hilbert_curve_2d(4)

    # filename = 'lena-64x64.jpg'
    filename = 'liver_dim2-64x64.jpg'
    filename = 'img/' + filename
    img = imread(filename)
    s = 32
    img = imresize(img, (s, s))
    flat_img = flatten_array(img)
    # plot_sound(flat_img)
    # plot_sound(convert_to_sound(flat_img))
    wav_file = 'sound' + filename[3:-3] + "wav"
    write_wav(convert_to_sound(flat_img), wav_file)

    # read_binary(wav_file)
