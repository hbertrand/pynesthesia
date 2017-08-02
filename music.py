import matplotlib.pyplot as plt
import numpy as np
import wave


def uint2freq(val):
    """
    http://celloweb.free.fr/textes/tableau_frequences_notes_hertz.htm
    """
    # 12*7+1 = 85, so we can map 3 values to 1 note
    # Start and end frequency have been chosen to be close to a piano range
    notes_freq = np.logspace(np.log10(27.500), np.log10(3520.000), 12*7+1)

    return notes_freq[int((val - 0.5) // 3)]


def freq_to_wav(val, framerate=44100, total_time=0.1, master_gain=0.05):
    t = np.linspace(0., total_time, int(framerate * total_time))
    res = np.sin(2 * np.pi * val * t)

    # Additive synthesis
    harmonics = 10
    for k in range(2, harmonics + 1):
        # There is no point adding harmonics above framerate / 2
        if k * val > framerate // 2:
            break

        if k % 2 == 0:
            continue
        res += (1. / k) * np.sin(2 * np.pi * k * val * t)
        # res += np.random.rand(1) * np.sin(2 * np.pi * k * val * t)
        # res += (1. / k) * np.sin(2 * np.pi * k * (k * np.random.normal(scale=0.01)) * val * t)

    res *= 1. / (100. * t + 1)
    res *= master_gain
    # return ((res + 1) * 127.5).astype(np.uint8)
    return (res * 32767).astype(np.int16)


def plot_sound(arr):
    arr = np.array(arr, dtype=np.int16)
    plt.plot(np.arange(len(arr)), arr - 127)
    plt.ylim([-130, 130])
    plt.show()


def convert_to_sound(arr):
    arr = np.array([freq_to_wav(uint2freq(i), total_time=0.1) for i in arr])
    return arr.flatten()


def write_wav(arr, sound_file_path):
    sound_file = wave.open(sound_file_path, 'wb')
    sound_file.setnchannels(1)
    sound_file.setsampwidth(2)
    sound_file.setframerate(44100)

    sound_file.writeframesraw(bytes(arr))

    sound_file.close()


def list2int(arr):
    res = 0
    for i, a in enumerate(arr):
        res += a << (8 * i)
    return res


def read_wav_header(file_path):
    content = []
    with open(file_path, 'rb') as f:
        for line in f:
            content.extend(line)

    print(content)
    print(''.join(chr(i) for i in content[:4]))
    print(list2int(content[4:8]))
    print(''.join(chr(i) for i in content[8:12]))
    print(''.join(chr(i) for i in content[12:16]))
    print(list2int(content[16:20]))
    print(list2int(content[20:22]))
    print(list2int(content[22:24]))
    print(list2int(content[24:28]))
    print(list2int(content[28:32]))
    print(list2int(content[32:34]))
    print(list2int(content[34:36]))
    print(''.join(chr(i) for i in content[36:40]))
    print(list2int(content[40:44]))
