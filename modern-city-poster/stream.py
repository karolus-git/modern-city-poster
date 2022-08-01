import streamlit as st
from reportlab.lib.units import inch, mm

import poster

st.set_page_config(
    layout="wide", 
    page_title="Modern City Poster")

# Initialisation of the session state
if 'poster_png' not in st.session_state:
    st.session_state.poster_png = 'assets/berlin.png'

if 'poster_pdf' not in st.session_state:
    st.session_state.poster_pdf = 'assets/berlin.pdf'

if 'places' not in st.session_state:
    st.session_state.places = "['Berlin, Germany']"

if 'background_color' not in st.session_state:
    st.session_state.background_color = "#e9ecef"

if 'street_color' not in st.session_state:
    st.session_state.street_color = "#151515"

if 'margin_color' not in st.session_state:
    st.session_state.margin_color = "#fafafa"

if 'title_color' not in st.session_state:
    st.session_state.title_color = "#B32E2C"

if 'subtitle_color' not in st.session_state:
    st.session_state.subtitle_color = "#000000"

if 'band_color' not in st.session_state:
    st.session_state.band_color = "#e0a022"

if 'title_font' not in st.session_state:
    st.session_state.title_font = "Helvetica-Bold"

if 'subtitle_font' not in st.session_state:
    st.session_state.subtitle_font = "Helvetica-Bold"

if 'title_size' not in st.session_state:
    st.session_state.title_size = 70

if 'subtitle_size' not in st.session_state:
    st.session_state.subtitle_size = 20

if 'title_space' not in st.session_state:
    st.session_state.title_space = 40

if 'subtitle_space' not in st.session_state:
    st.session_state.subtitle_space = 15

if 'title_text' not in st.session_state:
    st.session_state.title_text = "BERLIN"

if 'subtitle_text' not in st.session_state:
    st.session_state.subtitle_text = "GERMANY"

if 'title_alpha' not in st.session_state:
    st.session_state.title_alpha = 200

if 'subtitle_alpha' not in st.session_state:
    st.session_state.subtitle_alpha = 200

if 'title_alignment' not in st.session_state:
    st.session_state.title_alignment = 2

if 'subtitle_alignment' not in st.session_state:
    st.session_state.subtitle_alignment = 2

if 'band_alpha' not in st.session_state:
    st.session_state.band_alpha = 90

if 'page_width' not in st.session_state:
    st.session_state.page_width = 210

if 'page_height' not in st.session_state:
    st.session_state.page_height = 210

if 'page_auto' not in st.session_state:
    st.session_state.page_auto = False

if 'image_valign' not in st.session_state:
    st.session_state.image_valign = "center"

if 'header_valign' not in st.session_state:
    st.session_state.header_valign = "center"

if 'image_crop' not in st.session_state:
    st.session_state.image_crop = "height"

col_useless_l, col_poster, col_useless_r = st.columns([1, 2, 1])

col_useless_l.write("")
col_useless_r.write("")

col_poster.image(str(st.session_state.poster_png), 
        width=None, 
        use_column_width=None, 
        clamp=False, 
        channels="RGB", 
        output_format="auto")



def update_poster():

    st.session_state.poster_pdf, st.session_state.poster_png = poster.build(
            places=st.session_state.places,
            margin=25, #TODO add magin to streamlit
            auto=st.session_state.page_auto,
            pagesize = (st.session_state.page_width*mm, st.session_state.page_height*mm),
            background_color=st.session_state.background_color,
            street_color=st.session_state.street_color,
            margin_color=st.session_state.margin_color,
            band_color=st.session_state.band_color,
            band_alpha=st.session_state.band_alpha,
            image_valign=st.session_state.image_valign,
            image_halign="center",
            image_crop=st.session_state.image_crop,
            header_valign=st.session_state.header_valign,
            title= {
                'fontName': st.session_state.title_font,
                "text" : st.session_state.title_text,
                "textColor" : st.session_state.title_color,
                "textAlpha" : st.session_state.title_alpha,
                "fontSize" : st.session_state.title_size,
                "alignment" : st.session_state.title_alignment,
                "charSpace" : st.session_state.title_space,
            },
            subtitle = {
                'fontName': st.session_state.subtitle_font,
                "text" : st.session_state.subtitle_text,
                "textColor" : st.session_state.subtitle_color,
                "textAlpha" : st.session_state.subtitle_alpha,
                "fontSize" : st.session_state.subtitle_size,
                "alignment" : st.session_state.subtitle_alignment,
                "charSpace" : st.session_state.subtitle_space,
            },
        )



# ############ Side bar ############
with st.sidebar:

    # --------- Buttons ---------
    cols_dls = st.columns(2)
    with open(st.session_state.poster_png, "rb") as file:
        cols_dls[0].download_button(
            label="Download Poster as PNG",
            data=file,
            file_name="poster.png",
            mime="image/png"
        )

    with open(st.session_state.poster_pdf, "rb") as file:
        cols_dls[1].download_button(
             label="Download Poster as PDF",
             data=file,
             file_name="poster.pdf",
             mime="application/pdf"
           )

    # --------- Places ---------
    st.write("#### Locations")
    exp_loc = st.expander(label="Locations")
    with exp_loc:
        places = st.text_input("Location", st.session_state.places)

        cols_text = st.columns(2)

        cols_text[0].text_input("Title", 
            key="title_text", 
            on_change=update_poster)

        cols_text[1].text_input("Subtitle", 
            key="subtitle_text", 
            on_change=update_poster)

    # --------- Colors ---------
    st.write("#### Colors")
    exp_col = st.expander(label="Colors configuration")
    with exp_col:
        cols_color = st.columns(6)
        
        cols_color[0].color_picker("Back", 
            key="background_color", 
            on_change=update_poster)

        cols_color[1].color_picker("Streets", 
            key="street_color", 
            on_change=update_poster)

        cols_color[2].color_picker("Margin", 
            key="margin_color", 
            on_change=update_poster)

        cols_color[3].color_picker("Title", 
            key="title_color", 
            on_change=update_poster)

        cols_color[4].color_picker("Subtitle", 
            key="subtitle_color", 
            on_change=update_poster)

        cols_color[5].color_picker("Header", 
            key="band_color", 
            on_change=update_poster)

        cols_alpha = st.columns(3)

        cols_alpha[0].slider('Header α', 0, 255, 
            step=5, 
            key="band_alpha", 
            on_change=update_poster)

        cols_alpha[1].slider('Title α', 0, 255, 
            step=5, 
            key="title_alpha", 
            on_change=update_poster)

        cols_alpha[2].slider('Subtitle. α', 0, 200, 
            step=5, 
            key="subtitle_alpha", 
            on_change=update_poster)

    # --------- Fonts ---------
    st.write("#### Fonts")

    exp_font = st.expander(label="Font configuration")
    with exp_font:
        cols_font = st.columns(2)

        cols_font[0].selectbox(
            'Title Font',
            ('Courier-Bold', 'Helvetica-Bold'),
            key="title_font",
            on_change=update_poster)

        cols_font[1].selectbox(
            'SubTitle Font',
            ('Courier-Bold', 'Helvetica-Bold'),
            key="subtitle_font",
            on_change=update_poster)

        cols_size = st.columns(2)

        cols_size[0].number_input('Title size', 
            key="title_size", 
            step=1, 
            max_value=100, 
            on_change=update_poster)

        cols_size[1].number_input('SubTitle size', 
            key="subtitle_size", 
            step=1, 
            max_value=100, 
            on_change=update_poster)

        cols_charspace = st.columns(2)

        cols_charspace[0].number_input('Title space', 
            key="title_space", 
            step=1, 
            max_value=100, 
            on_change=update_poster)

        cols_charspace[1].number_input('SubTitle space', 
            key="subtitle_space", 
            step=1, 
            max_value=100, 
            on_change=update_poster)

    # --------- Geometry ---------

    st.write("#### Geometry")
    exp_pos = st.expander(label="Positions")
    with exp_pos:
        cols_pos_t = st.columns(2)

        cols_pos_t[0].selectbox(
            'Image',
            ('center', 'bottom', 'top'),
            key="image_valign",
            on_change=update_poster)

        cols_pos_t[1].selectbox(
            'Header',
            ('center', 'top', 'above', 'inside-top', 'inside-bottom', 'below', 'bottom'),
            key="header_valign",
            on_change=update_poster)

        cols_pos_b = st.columns(2)

        aligment_hoptions = ('left', 'center', 'right')
        
        cols_pos_b[0].selectbox(
            'Title',
            range(len(aligment_hoptions)), 
            format_func=lambda x: aligment_hoptions[x],
            key="title_alignment",
            on_change=update_poster)

        cols_pos_b[1].selectbox(
            'Subtitle',
            range(len(aligment_hoptions)),
            format_func=lambda x: aligment_hoptions[x],
            key="subtitle_alignment",
            on_change=update_poster)

    # --------- Page ---------

    exp_page = st.expander(label="Page")
    with exp_page:
        cols_page = st.columns([3, 3])

        auto = st.checkbox('Autosize', 
            st.session_state.page_auto,
            key="page_auto",
            on_change=update_poster)

        cols_page[0].number_input("Width [mm]", 
        st.session_state.page_width,
            key="page_width",
            step=1, 
            on_change=update_poster)

        cols_page[1].number_input("Height [mm]", 
            st.session_state.page_height,
            key="page_height",
            step=1,
            on_change=update_poster)
        
        st.radio(
            "Crop",
            ('height', 'width'),
            key="image_crop",
            on_change=update_poster)