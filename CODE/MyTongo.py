import tkinter as tk
import os
import folium
from PIL import Image, ImageTk
from tkinterweb import HtmlFrame
from customtkinter import set_appearance_mode, set_default_color_theme

window = None

def make_loading_screen():
    loading_frame = tk.Frame(window, bg="#001E2B")
    loading_frame.name = "loading"
    loading_frame.pack(fill="both", expand=True)
    try:
        MyTongo_logo = "../IMAGES/MyTongo_black.png"
        image = Image.open(MyTongo_logo).resize((350, 197), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        iso_label = tk.Label(loading_frame, image=photo, bg="#001E2B")
        iso_label.image = photo
        iso_label.pack(expand=True)
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    return loading_frame

def make_action_bar():
    action_bar = tk.Frame(window, bg="#001E2B", width=380, height=50)
    action_bar.name = "action_bar"
    action_bar.pack(side="top", fill="x")
    try:
        MyTongo_logo = "../IMAGES/MyTongo_black.png"
        logo_image = Image.open(MyTongo_logo).resize((120, 67), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(action_bar, image=logo_photo, bg="#001E2B")
        logo_label.image = logo_photo
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception as e:
        print(f"Error al cargar el Logo: {e}")
    return action_bar

# Frame del mapa
def make_start_frame():
    start_frame = tk.Frame(window, bg="#001E2B")
    start_frame.name = "start"
    mapa = folium.Map(
        location=[-17.7833, -63.1821],
        zoom_start=15,
        width=380,
        height=700
    )
    folium.Marker(
        location=[-17.7833, -63.1821],
        popup="Cristo Redentor - Santa Cruz",
        tooltip="Haz clic para más info",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(mapa)
    map_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css"/>
        <script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js"></script>
        
        <style>
            html, body {{
                width: 100%;
                height: 100%;
                margin: 0;
                padding: 0;
            }}
            #map {{
                position: absolute;
                top: 0;
                bottom: 0;
                width: 100%;
                height: 100%;
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        {mapa.get_root().render()}
        <script>
            var map = L.map(
                'map',
                {{
                    center: [-17.7833, -63.1821],
                    zoom: 15,
                    zoomControl: true,
                    preferCanvas: false,
                }}
            );
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '© OpenStreetMap contributors'
            }}).addTo(map);
            
            var marker = L.marker([-17.7833, -63.1821])
                .addTo(map)
                .bindPopup("Cristo Redentor - Santa Cruz")
                .bindTooltip("Haz clic para más info");
        </script>
    </body>
    </html>
    """
    ruta_mapa = os.path.abspath("mapa.html")
    with open(ruta_mapa, 'w', encoding='utf-8') as f:
        f.write(map_html)
    map_frame = HtmlFrame(
        start_frame,
        horizontal_scrollbar="auto",
        vertical_scrollbar="auto",
        messages_enabled=False
    )
    map_frame.pack(fill="both", expand=True)
    ruta_mapa_url = f"file:///{ruta_mapa}".replace("\\", "/")
    map_frame.load_file(ruta_mapa_url)
    return start_frame

def show_frame(frame_to_show):
    global all_frames, action_bar, current_frame
    current_frame = frame_to_show
    for frame in all_frames:
        frame.pack_forget()
    if hasattr(frame_to_show, "name") and frame_to_show.name == "loading":
        action_bar.pack_forget()
    else:
        action_bar.pack(side="top", fill="x")
    frame_to_show.pack(fill="both", expand=True)

def main():
    global window, all_frames, start_frame, action_bar, loading_frame
    set_appearance_mode("dark")
    window = tk.Tk()
    window.title("MyTongo")
    window.geometry("380x750+120+10")
    window.resizable(False, False)
    window.configure(bg="#001E2B")
    try:
        window.iconbitmap("../IMAGES/MyTongo_logo.ico")
    except Exception:
        print("Error al cargar el Icono")
    
    loading_frame = make_loading_screen()
    action_bar = make_action_bar()
    start_frame = make_start_frame()
    
    all_frames = [loading_frame, start_frame]
    show_frame(loading_frame)
    window.after(1500, lambda: show_frame(start_frame))
    window.mainloop()

if __name__ == "__main__":
    main()