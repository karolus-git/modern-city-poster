import osmnx as ox
import copy
from pathlib import Path
from PIL import Image as ImagePIL
from PIL import ImageOps, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPM
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Flowable, SimpleDocTemplate, BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.lib import colors, utils
from reportlab.lib.colors import PCMYKColor, PCMYKColorSep, Color, HexColor

from pdf2image import convert_from_bytes

import mapper
import utils

def convert_canvas_to_png(c, path):
    """Convert the canvas to a png


    Args:
        c (_type_): canvas
        path (_type_): filepath

    Returns:
        _type_: _description_
    """

    # Path for png file
    path_png = Path(path).with_suffix(".png")

    # Conversion and saving
    image = convert_from_bytes(c.getpdfdata())[0]
    image.save(path_png)

    return path_png

def build_png(
    places:tuple, 
    layers:dict, 
    path:str,
    dpi:int=500):
    
    
    fig, ax = mapper.set_figure()

    # The background is black, it will be updated during the poster build
    ax.set_facecolor("k")

    # For each layer, we get a graph and update it
    for layer in layers.values():
        graph = mapper.generate_graph(layer, places=places)
        mapper.add_graph(graph, ax, layer)

    # Save the graph
    fig.savefig(path, 
            dpi=dpi, 
            bbox_inches='tight', 
            pad_inches=0,
            format="png", 
            transparent=False,
        )

def plot_band(
    c,
    band_color:str="#156156",
    band_alpha:int=60,
    width:float=150,
    height:float=250, 
    x:float=0,
    y:float=0)->None:

    # Add the alpha part of the color
    bandColor_alpha = f"{band_color}{band_alpha:02x}"

    # Draw the band
    band_drawing = Drawing(width, height)
    band = Rect(x, y, width, height, 
            strokeWidth=0, 
            strokeColor=None,
            fillColor=HexColor(bandColor_alpha, hasAlpha=True)
            )
    # Add the band to the drawing
    band_drawing.add(band)

    #Add the drawing to the canvas
    band_drawing.drawOn(c, 0, 0)

def get_header_y(valign, page_height, margin, bounds, header_height):
    """Set the vertical position of the header

    Args:
        valign (_type_): _description_
        page_height (_type_): _description_
        margin (_type_): _description_
        bounds (_type_): _description_
        header_height (_type_): _description_

    Returns:
        float: vertical position
    """

    if valign == "top":
        return page_height - margin - header_height
    elif valign == "bottom":
        return margin
    elif valign == "center":
        return 0.5 * (page_height - header_height)
    elif valign == "above":
        return bounds[3]
    elif valign == "below":
        return bounds[1] - header_height
    elif valign == "inside-top":
        return bounds[3] - header_height
    elif valign == "inside-bottom":
        return bounds[1]

def plot_header(
    c,
    title:dict,
    subtitle:dict,
    bounds:tuple,
    pagesize:tuple=(210*mm, 297*mm),
    margin:float=15,
    valign:str="center",
    halign:str="right",
    band_color:str="#156489",
    band_alpha:int=255,
    
):

    SPACER_Y = 10
    Margin_y = 10
    page_width, page_height = pagesize

    # Calculate the height of the header 
    font_height = title.get("fontSize") + subtitle.get("fontSize") * 0.65
    header_height = (font_height + SPACER_Y + 2*Margin_y)

    # Get the vertical position of the header
    y = get_header_y(valign, page_height, margin, bounds, header_height)
    
    # Ajust its value according to the top and bottom limits
    y = max(min(y, page_height - margin - header_height), margin)

    # Plot a band
    plot_band(c,
        band_alpha=band_alpha,
        band_color=band_color,
        width=page_width-2*margin,
        height=header_height,
        x=margin,
        y=y)

    # Get a frame
    frame = Frame(
                    margin, 
                    y,
                    page_width-2*margin, 
                    header_height,
                    showBoundary=False,
                    )

    story = []
    
    y += Margin_y
    # For title and  subtitle, create a paragraph and add it to the story
    for conf in (subtitle, title):

        textColor_alpha = f"{conf.get('textColor')}{conf.get('textAlpha'):02x}"
        
        # style = ParagraphStyle('Body', 
        #     fontName=conf.get("fontName"), 
        #     fontSize=conf.get("fontSize"), 
        #     textColor=HexColor(textColor_alpha, hasAlpha=True),
        #     leading=conf.get("fontSize"), 
        #     alignment=conf.get("alignment"), 
        #     textAnchor="c",
        #     spaceBefore=10)


        # paragraph = Paragraph(conf.get("text"), style)

        text = conf.get("text")
        charspace = conf.get("charSpace", 0)
        alignment = conf.get("alignment")
        size = conf.get("fontSize")
        name = conf.get("fontName")
        
        # Get the size of the text
        textWidth = c.stringWidth(text, name, size)
        textWidth += charspace * (len(text)-1)

        # Adjust the position of the text according to its alignment
        if alignment == 0:
            x = margin + SPACER_Y
        elif alignment == 1:
            x = 0.5 * (page_width - textWidth)
        elif alignment == 2:
            x = page_width - margin - textWidth - SPACER_Y

        # Create the textobject
        textobject = c.beginText()
        textobject.setTextOrigin(x, y)
        textobject.setFont(name, size)
        textobject.setCharSpace(charspace)
        textobject.setFillColor(HexColor(textColor_alpha, hasAlpha=True))
        textobject.textLine(text)

        c.drawText(textobject)

        # Add a vertical space
        y += size
        y += SPACER_Y
    

def plot_image(
    c, 
    path:str, 
    pagesize:tuple=(210*mm, 297*mm),
    margin:float=15,
    valign:str="center",
    halign:str="center",
    crop:str="height",
    ratio:float=1.0,
    ):

    page_width, page_height = pagesize

    # Get the image of the image according to crop
    if crop == "width": # The image will take all the width of the page
        width = page_width - 2.0 * margin
        height = (width * ratio)

    elif crop == "height": # The image will take all the height of the page
        height = page_height - 2.0 * margin
        width = (height / ratio)
    
    # Set the vertical position of the image
    if valign == "top":
        y = page_height - 0.5 * height- margin
    elif valign == "bottom":
        y = margin + 0.5 * height
    elif valign == "center":
        y = 0.5 * page_height

    # Set the horizontal position of the image
    if halign == "center":
        x = 0.5 * page_width
    elif halign == "right":
        x = page_width - 0.5 * width - margin
    elif halign == "left":
        x = margin + 0.5 * width

    # Plot the image according to the configuration
    c.drawImage(
        path,
        showBoundary=False,
        anchorAtXY=True,        
        x=x,
        y=y,
        width=width, 
        height=height,
        anchor="c")

    return [x-width/2, y-height/2, x+width/2, y+height/2]

def image_update(
    path:str,
    path_colorized:str="",
    black:str="#000000",
    white:str="#ff222f",
    ext_colorized:str=".colorized"
):

    path_file = Path(path)
    ext_file = path_file.suffix

    # Create the path of the colorized picture if empty
    if not path_colorized:
        path_colorized = path_file.with_suffix(ext_colorized+ext_file)

    # Load the image
    img = ImagePIL.open(path).convert("L") 
    img_w, img_h = img.size

    # Convert back and white to your colors
    img = ImageOps.colorize(
        img, 
        black=black, 
        white=white
        )

    # Save the colorized image to the new path and return it
    img.save(path_colorized)

    return path_colorized, img_w, img_h

def plot_margins(
    c,
    pagesize:tuple=(210*mm, 297*mm),
    margin:float=15,
    color:str="#9AC6C0"
):

    page_width, page_height = pagesize

    draw_margin = Drawing(page_width, page_height)

    draw_margin.add(
        Rect(0.5 * margin, 0.5 * margin, 
            width=page_width-margin, 
            height=page_height-margin, 
            fillColor=None, 
            strokeWidth=margin, 
            strokeColor=HexColor(color)
            )
        )

    draw_margin.drawOn(c, 0, 0)


def plot_background(
    c,
    pagesize:tuple=(210*mm, 297*mm),
    margin:float=15,
    color:str="#154152"
):

    # Set height and width of the background
    background_width = pagesize[0] - 2.0 * margin
    background_height = pagesize[1] - 2.0 * margin

    # Colorize it
    c.setFillColor(HexColor(color))

    # Create a rectangle
    c.rect(margin, margin, 
        width=background_width, 
        height=background_height, 
        stroke=0, 
        fill=1,
        )

def get_canvas(
    path:str,
    pagesize:tuple=(210*mm, 297*mm),
):
    return canvas.Canvas(path,
            pagesize=pagesize)

def build_pdf(
    path_png:str,
    margin:float=25,
    auto:bool=False,
    pagesize:tuple=(297*mm, 210*mm),
    background_color:str="#f5e8d7",
    street_color:str="#ba897a",
    margin_color:str="#ffffff",
    band_color:str="#000000",
    band_alpha:int=10,
    image_valign:str="center",
    image_halign:str="center",
    image_crop:str="width",
    header_halign:str="center",
    header_valign:str="center",
    title:dict={
        'fontName': 'Helvetica-Bold',
        "text" : "CITY",
        "textColor" : "#ba897a",
        "textAlpha" : 255,
        "fontSize" : 55,
        "alignment" : 2
    },
    subtitle:dict={
        'fontName': 'Helvetica-Bold',
        "text" : "Country",
        "textColor" : "#ba897a",
        "textAlpha" : 255,
        "fontSize" : 14,
        "alignment" : 2
    }
):

    path_pdf = str(Path(path_png).with_suffix(".poster.pdf"))

    # Change the color of the map (streets and background)
    path_colorized, image_width, image_height = image_update(
        path_png,
        black=background_color,
        white=street_color,
        )

    # If auto is True, the page size will be the size of the image with margins
    if auto:
        
        max_image_width = min(1000*mm, image_width)
        max_image_height = min(1000*mm, image_height)
        print(image_width, max_image_width)
        pagesize = (max_image_width+margin, max_image_height+margin)

    # Create a canvas
    c = get_canvas(path_pdf,
        pagesize=pagesize,
        )

    # Plot the background
    plot_background(
        c,
        pagesize=pagesize,
        margin=margin,
        color=background_color,
        )

    #Plot the image
    bounds = plot_image(
        c,
        path_colorized,
        pagesize=pagesize,
        margin=margin,
        valign=image_valign,
        halign=image_halign,
        crop=image_crop,
        ratio=image_height/image_width
    )

    # Plot the header, band and title+subtitle
    plot_header(
        c,
        title,
        subtitle,
        bounds,        
        pagesize=pagesize,   
        margin=margin,     
        valign=header_valign,
        halign=header_halign,
        band_color=band_color,
        band_alpha=band_alpha,
    )

    #Plot the margins
    plot_margins(
        c,
        pagesize=pagesize,
        margin=margin,
        color=margin_color,
    )
    
    #Save the canvas to pdf
    c.save()

    # Convert it to png
    path_poster_png = convert_canvas_to_png(c, path_pdf)

    return path_pdf, path_poster_png
    
def build(*args, **kwargs):
    
    places = kwargs.get("places")
    street_color = kwargs.get("street_color")

    layers = {
        "street": {
            "type" : "roads",
            "filter_major" : "highway",
            "filter_minor" : "motorway|trunk|primary|secondary|tertiary|service|unclassified|pedestrian|footway|steps|residential|living_street",
            "options" : {
                "motorway" : {"width" : 1.5},
                "trunk" : {"width" : 1.5},
                "primary" : {"width" : 0.8},
                "secondary" : {"width" : 0.5},
                "tertiary" : {"width" : 0.5},
                "other" : {"width" : 0.3},
            }
        },
    }
    
    # We hash the config dictionary
    hash_conf = utils.make_hashable({"places" : f"{places}", "layers":layers})
    hash_str = utils.make_hash(hash_conf)

    # The path is build with this hash
    path = f"./data/{hash_str}.png"

    # If the path does not exists, we build the png. Otherwise, the png file for this configuration already exists
    if not Path(path).exists():

        # Build the graph
        build_png(
            places,
            layers,
            path,
            dpi=kwargs.get("dpi", 500)
        )

    # We drop the places key, cause we don't need it anymore
    kwargs.pop("places")

    # Build the pdf
    poster_pdf, poster_png = build_pdf(
        path,
        **kwargs)

    # Et voilà !
    return poster_pdf, poster_png


if __name__ == "__main__":

    import cities

    for name, conf in cities.conf.items():

        print(f"building your poster of {name} ")
        build(**conf)
        print(f"poster of {name} created ")

