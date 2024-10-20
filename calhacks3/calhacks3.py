import asyncio
import reflex as rx
from .views.navbar import navbar
from .views.email import email_gen_ui
from .views.table import main_table
from .views.camera import camera_feed, layout_with_video_and_another_component, deploy_safety_measures

from .views.timer import countdown_clock
from .backend.backend import State

from .voice.main import generate_and_speak, speak

import os
from .face_recog import get_emotions
from json import dump
def process_library_emotions(directory):
    for root, dirs, files in os.walk(directory):  # Recursively go through directories
        fs = []
        #print(f"Processing directory: {os.path.basename(root)}")
        for file in files:
            if file.endswith('.png'):
                file_path = os.path.join(root, file)
                #print(f"Processing file: {file_path}")
                # Your file processing logic here

                fs.append(get_emotions(file_path)[0])
                fs[-1]['path'] = file_path
        print(fs)
        dump(fs, open(os.path.join(root, 'meta.json'), 'w'))

process_library_emotions('./photodatabase')
process_library_emotions('./nicephotodatabase')

async def camera_task():
    from .face_recog import stuff
    try:
        await stuff()
    except asyncio.CancelledError:
        print('camera task ended')
        return

speak()

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        layout_with_video_and_another_component(),
        countdown_clock(100),
        
        deploy_safety_measures(),
        # rx.flex(
        #     rx.box(main_table(), width=["100%", "100%", "100%", "60%"]),
        #     # email_gen_ui(),
        #     spacing="6",
        #     width="100%",
        #     flex_direction=["column", "column", "column", "row"],
        # ),
        height="100vh",
        bg="#000000",
        width="100%",
        padding_x=["1.5em", "1.5em", "3em"],
        padding_y=["1em", "1em", "2em"],
        margin_top="5em",
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Rubik+Bubbles&display=swap",
    ],
    theme=rx.theme(
        appearance="dark",  # Set to "dark" if you want a dark-themed appearance
        has_background=True, 
        radius="large", 
        accent_color="plum",
        colors={
            "primary": "#ff006c",  # Custom pink for primary elements
            "secondary": "#000000",  # Black for secondary elements
            "accent": "#FF007F",  # Pink for accent elements
            "background": "#000000",  # Black background color
            "text": "#FFFFFF",  # White text for contrast
        },
    ),
    styles={
        "body": {
            "backgroundColor": "#000000",  # This forces the background color to black
            "color": "#FFFFFF",  # Text color set to white for contrast
        }
    }
)

app.add_page(
    index,
    # on_load=State.load_entries,
    title="ForgetMeNot",
    description="CalHacks 11.0",
)

app.register_lifespan_task(camera_task)
