import numpy as np
from skimage.transform import rescale

def crop_img(img, x, y, scalef=1.0, sizef=1.0, spot_diameter=89.44476048022638, mask_circle=False, cval=0.0, **kwargs):
    """
    extract a crop from `img` centered at `x` and `y`. 
    Attrs:
        x (int): x coord of crop in `img`
        y (int): y coord of crop in `img`
        scalef (float): resolution of the crop (smaller -> smaller image)
        sizef (float): amount of context (1.0 means size of spot, larger -> more context)
        spot_diameter (float): standard size of crop, with sizef == 1.0, taken from 
            `adata.uns['spatial'][dataset_name]['scalefactors']['spot_diameter_fullres']`
        mask_circle (bool): mask crop to a circle
        cval (float): the value outside image boundaries or the mask
        kwargs: optional arguments passed to the `skimage.transform.rescale` function
    """
    assert y < img.shape[0], f"y ({y}) is outsize of image range ({img.shape[0]})"
    assert x < img.shape[1], f"x ({x}) is outsize of image range ({img.shape[1]})"
    
    # get image size to crop from fullres image
    s = np.round(spot_diameter*sizef).astype(int)
    assert s > 0, f"image size cannot be 0! spot_diameter: {spot_diameter}, sizef: {sizef}"
    if len(img.shape) == 3:
        crop = (np.zeros((s,s,img.shape[2]))+cval).astype(img.dtype)
    else:
        crop = (np.zeros((s,s))+cval).astype(img.dtype)
        
    # get crop coords
    x0 = x - s//2
    x1 = x + s - s//2
    y0 = y - s//2
    y1 = y + s - s//2
    
    # crop image and put in already prepared `crop`
    crop_x0 = min(x0, 0)*-1
    crop_y0 = min(y0, 0)*-1
    crop_x1 = s - max(x1 - img.shape[1], 0)
    crop_y1 = s - max(y1 - img.shape[0], 0)
    
    crop[crop_y0:crop_y1, crop_x0:crop_x1] = img[max(y0,0):y1, max(x0,0):x1]
    # scale crop
    if scalef != 1:
        multichannel = len(img.shape) > 2
        crop = rescale(crop, scalef, preserve_range=True, multichannel=multichannel, **kwargs)
        crop = crop.astype(img.dtype)
    return crop