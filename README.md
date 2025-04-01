# Converting nh7 file to reflectance ENVI files

## Introduction

This project is for converting nh7 file (measured by Eba Jpans's NH-7 hyperspectral sensor) to reflectance data in more general ENVI files that is a standard hyperspectral data format.

## How does it work?
1. **Installing necesary dependencies**
   - Install necessary dependencies by referring to `nh72envi.py` and `nh72envi_demo.py`.
   
2. **Running code**
   - Specify `fname1` (nh7 file name with white reference) and `fname2` (nh7 file name with/without white reference) in `nh72envi_demo.py`, then run the following command:
```bash
python nh72envi_demo.py
```

3. **Selecting area of white diffuse reflectance standard**
   - Select area of white diffuse reflectance standard. Type `space` key and, then, `Enter` key.

**Selecting area (blue bbox) of white diffuse reflectance standard**:
![RoI WDRS](asset/RoI_selection.png)

4. **Generating reflectance ENVI file**
   - Reflectance ENVI files (heder (.hdr) and data (.dat) files) and color image (jpeg) are generated.

---
## Data format
| | nh7 format | converted ENVI format|
| ---- | ---- | ---- |
| Data | Digital Number after dark current subtraction | reflectance |
| Data type | uint16 | float32 |
| Interleave | BIL | BSQ |

## Specification of sensor (NH-7, Eva Japan)
Attribute | Value
---|---
Image resolution | 1280×1024
Wavelength band | 350-1100 nm
Spectral resolution | 5 nm
Data output | 10 bit

