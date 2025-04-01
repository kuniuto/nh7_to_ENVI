# Converting nh7 file to reflectance ENVI file

## Introduction

This project is for converting nh7 file to reflectance data in more general ENVI file that is a standard hyperspectral data format.

## How does it work?
After installing necessary dependencies, specify `fname1` and `fname2` in `nh72envi_demo.py`, then run the following command:
```bash
python nh72envi_demo.py
```
- Input: nh7 file
- Output: ENVI file (reflecntace, interleave=BSQ, data type=32-bit single-precision, byte order=host (Intel))

