from reportlab.lib.units import inch, mm

# Here are some examples of what you can do !
conf = {      
        #---------------------- Nairobi ----------------------
        "nairobi": {
                "places": ["Nairobi"],
                "margin" : 20,
                "auto" : False,
                "pagesize" : (297 * mm, 210 * mm),
                "background_color" : "#f5e8d7",
                "street_color":"#ba897a",
                "margin_color":"#ffffff",
                "band_color" : "#000000",
                "band_alpha" : 10,
                "image_valign":"center",
                "image_halign":"center",
                "image_crop":"width",
                "header_halign":"center",
                "header_valign":"inside-bottom", 
                "title" : {
                        'fontName': 'Helvetica-Bold',
                        "text" : "NAIROBI",
                        "textColor" : "#ba897a",
                        "textAlpha" : 99,
                        "fontSize" : 55,
                        "alignment" : 2,
                        "charSpace" : 10
                },
                "subtitle" : {
                        'fontName': 'Helvetica',
                        "text" : "Capital of Kenya",
                        "textColor" : "#ba897a",
                        "textAlpha" : 99,
                        "fontSize" : 20,
                        "alignment" : 2,
                        "charSpace" : 10
                }
        },
        #---------------------- Denver ----------------------
        "denver": {
                "places": ["Denver"],
                "margin" : 25,
                "auto" : False,
                "pagesize" : (210 * mm, 210 * mm),
                "background_color" : "#740000",
                "street_color":"#FFF3F3",
                "margin_color":"#FFF3F3",
                "band_color" : "#FFF3F3",
                "band_alpha" : 255,
                "image_valign":"top",
                "image_halign":"center",
                "image_crop":"width",
                "header_halign":"center",
                "header_valign":"below", 
                "title" : {
                        'fontName': 'Courier-Bold',
                        "text" : "DENVER",
                        "textColor" : "#740000",
                        "textAlpha" : 99,
                        "fontSize" : 45,
                        "alignment" : 0,
                        "charSpace" : 10
                },
                "subtitle" : {
                        'fontName': 'Courier-Bold',
                        "text" : """Colorado, 39° 44′ 21'' N, 104° 59′ 05'' W""",
                        "textColor" : "#740000",
                        "textAlpha" : 99,
                        "fontSize" : 12,
                        "alignment" : 0,
                        "charSpace" : 10
                }
        },
        # ---------------------- Helsinki ----------------------
        "helsinki": {
                "places": ["Helsinki"],
                "margin" : 0,
                "auto" : False,
                "pagesize" : (210 * mm, 297 * mm),
                "background_color" : "#151515",
                "street_color":"#F1F1F1",
                "margin_color":"#ffffff",
                "band_color" : "#e9ecef",
                "band_alpha" : 0,
                "image_valign":"bottom",
                "image_halign":"center",
                "image_crop":"width",
                "header_halign":"above",
                "header_valign":"above", 
                "title" : {
                        'fontName': 'Helvetica-Bold',
                        "text" : "HELSINKI",
                        "textColor" : "#ffffff",
                        "textAlpha" : 255,
                        "fontSize" : 60,
                        "alignment" : 1,
                        "charSpace" : 10
                },
                "subtitle" : {
                        'fontName': 'Helvetica-Bold',
                        "text" : "Finland",
                        "textColor" : "#ffffff",
                        "textAlpha" : 255,
                        "fontSize" : 18,
                        "alignment" : 1,
                        "charSpace" : 10
                }
        },
        # ---------------------- Berlin ----------------------
        "berlin": {
                "places": ["Berlin"],
                "margin" : 50,
                "auto" : False,
                "pagesize" : (210 * mm, 210 * mm),
                "background_color" : "#e9ecef",
                "street_color":"#151515",
                "margin_color":"#ffffff",
                "band_color" : "#000000",
                "band_alpha" : 55,
                "image_valign":"center",
                "image_halign":"center",
                "image_crop":"width",
                "header_halign":"center",
                "header_valign":"center", 
                "title" : {
                        'fontName': 'Courier-Bold',
                        "text" : "BERLIN",
                        "textColor" : "#ffffff",
                        "textAlpha" : 200,
                        "fontSize" : 55,
                        "alignment" : 2,
                        "charSpace" : 10
                },
                "subtitle" : {
                        'fontName': 'Courier-Bold',
                        "text" : "GERMANY",
                        "textColor" : "#ffffff",
                        "textAlpha" : 150,
                        "fontSize" : 12,
                        "alignment" : 2,
                        "charSpace" : 10
                }
        },
        "oslo": {
                "places": ["Oslo"],
                "margin" : 50,
                "auto" : False,
                "pagesize" : (210 * mm, 297 * mm),
                "background_color" : "#083D4B",
                "street_color":"#ffffff",
                "margin_color":"#ffffff",
                "band_color" : "#ffffff",
                "band_alpha" : 255,
                "image_valign":"top",
                "image_halign":"center",
                "image_crop":"height",
                "header_halign":"center",
                "header_valign":"top", 
                "title" : {
                        'fontName': 'Helvetica-Bold',
                        "text" : "O·S·L·O",
                        "textColor" : "#083D4B",
                        "textAlpha" : 255,
                        "fontSize" : 75,
                        "alignment" : 1,
                        "charSpace" : 30,
                },
                "subtitle" : {
                        'fontName': 'Helvetica-Bold',
                        "text" : "NORWAY",
                        "textColor" : "#083D4B",
                        "textAlpha" : 200,
                        "fontSize" : 22,
                        "alignment" : 1,
                        "charSpace" : -2
                }
        }
}
