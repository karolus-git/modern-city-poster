import osmnx as ox
import logging
import matplotlib.pyplot as plt
import geopandas
import networkx

def set_figure(figsize:tuple=[12,12]):
    """Initialize the figure

    Args:
        figsize (tuple, optional): size of the image. Defaults to [12,12].

    Returns:
        plt.subplots: figure
    """
    return plt.subplots(figsize=figsize, constrained_layout = True)

def add_graph(graph, ax, layer, background_color=None):
    """Add the graph to the figure ax

    Args:
        graph (_type_): _description_
        ax (_type_): _description_
        layer (_type_): _description_
        background_color (_type_, optional): _description_. Defaults to None.
    """
    
    if isinstance(graph, geopandas.geodataframe.GeoDataFrame):

        color = layer.get("options").get("color")
        width = layer.get("options").get("width")

        graph.plot(
            facecolor=color,
            edgecolor=color,
            linewidth=width,
            ax = ax)

    elif isinstance(graph, networkx.classes.multidigraph.MultiDiGraph):

        graph, widths = update_graph(graph, layer)

        ox.plot_graph(graph,
            #bgcolor=background_color,
            edge_color="w",
            edge_linewidth=widths,
            node_size=0,
            save=False, 
            show=False,
            ax=ax)
    
def update_graph(graph, layer):
    """Update the widths of elements of the graph

    Args:
        graph (_type_): _description_
        layer (_type_): _description_

    Returns:
        _type_: _description_
    """

    #ox_colors = []
    ox_widths = []
    errors_idx = []

    for idx, (u, v, data) in enumerate(graph.edges(keys=False, data=True)):

        filter_major = layer.get("filter_major")

        if filter_major in data.keys():
            
            data_minor = data.get(filter_major)

            if isinstance(data_minor, list):
                data_minor = data_minor[0]
            filter_options = layer.get("options")

            if data_minor in filter_options.keys():
                #color = filter_options.get(data_minor).get("color")
                width = filter_options.get(data_minor).get("width")
            elif 'other' in filter_options.keys():
                #color = filter_options.get("other").get("color")
                width = filter_options.get("other").get("width")
            else:
                #color = filter_options.get("color")
                width = filter_options.get("width")   

            #ox_colors.append("#ffffff")
            ox_widths.append(width)

        else:
            errors_idx.append([u, v])

    for error_idx in errors_idx:
        graph.remove_edge(*error_idx)

    return graph, ox_widths

def build_filter(
    config:dict,
    ):
    

    filter_ma = config.get("filter_major", None)
    filter_mi = config.get("filter_minor", None)

    if filter_ma and filter_mi:
        return f"""["{filter_ma}"~"{filter_mi}"]""" 
    else:
        return None

def get_geometry(config:dict, places:tuple=[]):
    return ox.geometries.geometries_from_place(places, tags = {config.get("filter_major"): config.get("filter_minor")})

def get_roads(config:dict, places:tuple=[]):

    custom_filter = build_filter(config)

    return ox.graph_from_place(places, 
                    network_type='all_private', 
                    simplify=True, 
                    retain_all=True, 
                    truncate_by_edge=True, 
                    clean_periphery=True, 
                    custom_filter=custom_filter)

def generate_graph(config:dict, places:tuple=[]):

    if config.get("type") == "roads":
        return get_roads(config, places=places)

    elif config.get("type") == "geometry":
        return get_geometry(config, places=places)