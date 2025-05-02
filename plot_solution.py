import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
import contextily as ctx

def plot_path_on_map(locations, path_order, save_path=None):
    """
    Plot a set of locations and a path connecting them over a real map.
    
    Args:
        locations: List of (longitude, latitude) tuples.  [(lon, lat), (lon, lat), ...]
        path_order: List of indices specifying the order to visit the locations.
        save_path: If given, saves the plot to this filepath.
    """
    # Create GeoDataFrame for points
    locations = [(lon, lat) for lat, lon in locations]  # Ensure correct order
    points = [Point(locations[i]) for i in path_order]
    gdf_points = gpd.GeoDataFrame(geometry=points, crs="EPSG:4326")
    
    # Create GeoDataFrame for path (LineString)
    path_coords = [locations[i] for i in path_order]
    line = LineString(path_coords)
    gdf_line = gpd.GeoDataFrame(geometry=[line], crs="EPSG:4326")
    
    # Project to Web Mercator (required for contextily map tiles)
    gdf_points = gdf_points.to_crs(epsg=3857)
    gdf_line = gdf_line.to_crs(epsg=3857)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    
    gdf_line.plot(ax=ax, color='red', linewidth=2, alpha=0.7, zorder=2)
    gdf_points.plot(ax=ax, color='blue', markersize=50, zorder=3)

    # Add numbers on each point
    for idx, row in gdf_points.iterrows():
        ax.text(row.geometry.x, row.geometry.y, str(idx+1), fontsize=9, ha='center', va='center', color='white', weight='bold')
    
    # Add map tiles
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Voyager)

    ax.set_axis_off()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    # Example locations (longitude, latitude)
    locations = [
        (7.5, 47.5),
        (7.6, 47.6),
        (7.7, 47.7),
        (7.8, 47.8)
    ]
    
    # Example path order
    path_order = [0, 2, 3, 1]  # the visiting sequence
    
    # Plot the path on map
    plot_path_on_map(locations, path_order)
# Example usage:
# locations = [(longitude1, latitude1), (longitude2, latitude2), ...]
# path_order = [0, 2, 3, 1]  # the visiting sequence
# plot_path_on_map(locations, path_order)
