import pandas as pd
from rasterstats import zonal_stats

def aggregate_raster_by_polygon(
    polygons_gdf,
    raster_path,
    agg="sum",
    band=1,
    nodata=None,
    all_touched=False,
):
    """
    Aggregate raster values within polygons.

    Parameters
    ----------
    polygons_gdf : geopandas.GeoDataFrame
        Polygon layer.
    raster_path : str
        Path to raster file.
    agg : str or callable
        Aggregation function. If str, must be one of:
        ['sum', 'mean', 'min', 'max', 'median', 'count', 'std'].
        If callable, it will be applied to the raster values.
    band : int
        Raster band to use.
    nodata : numeric, optional
        Override raster nodata value.
    all_touched : bool
        Whether to include all pixels touched by polygons.

    Returns
    -------
    pandas.Series
        Aggregated value for each polygon, indexed like polygons_gdf.
    """
    
    if isinstance(agg, str):
        stats = zonal_stats(
            polygons_gdf,
            raster_path,
            stats=[agg],
            band=band,
            nodata=nodata,
            all_touched=all_touched,
        )
        values = [s.get(agg) for s in stats]

    else:
        # Custom aggregation function
        stats = zonal_stats(
            polygons_gdf,
            raster_path,
            raster_out=True,
            band=band,
            nodata=nodata,
            all_touched=all_touched,
        )

        values = []
        for s in stats:
            arr = s["mini_raster_array"]
            arr = arr.compressed()  # remove masked/nodata pixels
            values.append(agg(arr) if len(arr) else None)

    return pd.Series(values, index=polygons_gdf.index)