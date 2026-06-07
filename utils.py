import pandas as pd
from rasterstats import zonal_stats
from pyproj import CRS
import numbers

def f3(df,d): 
    '''
    Generic function to filter a dataframe by column values passing a dict d with the required columns as keys,
    and values that might be lists or single values of string or numbers.
    '''
    aux = []
    for k,v in d.items():
        if isinstance(v, numbers.Number):
            aux.append(f'`{k}`=={v}')
        elif isinstance(v, list):    
            aux.append(f'`{k}` in {v}')
        else:
            aux.append(f'`{k}`=="{v}"')
    ref = ' and '.join(aux)
#     print(ref)
    return df.query(ref)
    
def f4(df,d): 
    '''
    Generic function to filter a dataframe by column values passing a dict d with the required columns as keys,
    and values that might be lists or single values of string or numbers.
    '''
    aux = []
    for k,v in d.items():
        if isinstance(v, numbers.Number):
            aux.append(f'`{k}`!={v}')
        elif isinstance(v, list):    
            aux.append(f'`{k}` not in {v}')
        else:
            aux.append(f'`{k}`!="{v}"')
    ref = ' and '.join(aux)
#     print(ref)
    return df.query(ref)

def get_grid_info(df,raster_path, agg='sum', col='VOL', all_touched=False):
	df_orig_crs = df.crs
    dataset = rasterio.open(raster_path)
    affine=dataset.transform
    nodata_value = dataset.nodata
    
    clean_crs = CRS.from_user_input(dataset.crs.to_wkt())

    df2 = df.to_crs(clean_crs)
    
    stats = zonal_stats(df2,raster_path, affine, nodata=nodata_value, stats=agg, all_touched=all_touched)
    df2[col] = [s[agg] if s[agg] is not None else 0 for s in stats]
    return df2.to_crs(df_orig_crs)
