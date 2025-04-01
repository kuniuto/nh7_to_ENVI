# Converting nh7 file to reflectance ENVI file

## Introduction

This project is for converting nh7 file (measured by Eba Jpans's NH-7 hyperspectral sensor) to reflectance data in more general ENVI file that is a standard hyperspectral data format.

## How does it work?
1. **After installing necessary dependencies, specify `fname1` (nh7 file name with white reference) and `fname2` (nh7 file name with/without white reference) in `nh72envi_demo.py`, then run the following command:
```bash
python nh72envi_demo.py
```

2. **
- Input: nh7 file
- Output: ENVI file (reflecntace, interleave=BSQ, data type=32-bit single-precision, byte order=host (Intel))

data format
| | nh7 format | ENVI format|
| ---- | ---- | ---- |
