import pandas as pd
from rasterstats import zonal_stats
from pyproj import CRS

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
