
# Spectogram-to-STL Converter

**turns audio spectrograms into 3D models**

this tool transforms grayscale PNGs into 3D-printable STL meshes. brightness maps to height.

it was specifically intended for spectrograms of sound but it theoretically could take any greyscale input image.

---

## 🛠 features

- converts **spectrogram-style grayscale PNGs** into STL
- nonlinear height shaping via `spike_factor`
- customizable base + peak height
- renders full mesh with base + vertical walls
- command line friendly

---

## install

python is required to run the script, see [python.org](python.org) for installation details.

to install the required packages:

```bash
pip install numpy pillow numpy-stl
```

try this if that doesn't work:

```bash
pip3 install numpy pillow numpy-stl
```

## usage

```bash
python spec_to_stl.py input.png output.stl [base_height] [max_height] [spike_factor]
```

![86E49DA4-EBFF-4F57-A46D-6AD64E808045_1_105_c](https://github.com/user-attachments/assets/60998389-9d8e-48a5-a613-0e861e014c19)


> *originally created by jordan bevan and stella drinwkater for “Designing Creativity Support Tools” (CSC 413, UVIC), 2025.*
