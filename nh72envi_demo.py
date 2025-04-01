import nh72envi

# nh7 file name with white reference
fname1 = "F:/bridge/data/nh7/20240925/EC3_rice_white_Img-d(s20,g50,49.97ms,350-1100)_20240925_141233.nh7"
# nh7 file name without white reference
fname2 = "F:/bridge/data/nh7/20240925/EC3_rice_Img-d(s20,g50,49.97ms,350-1100)_20240925_141104.nh7"

nh72envi.ref(fname1,fname2)

