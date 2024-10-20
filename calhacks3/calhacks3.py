import asyncio
import reflex as rx
from .views.navbar import navbar
from .views.email import email_gen_ui
from .views.table import main_table
from .views.camera import camera_feed, layout_with_video_and_another_component
from .views.deploysafetymeasures import deploy_safety_measures
from .backend.backend import State


## Function to capture the camera feed using OpenCV
#async def stream_camera():
#    cap = cv2.VideoCapture(0)  # Start capturing video from the first camera
#
#    while cap.isOpened():
#        ret, frame = cap.read()
#        if ret:
#            # Encode the frame as a JPEG
#            _, buffer = cv2.imencode('.jpg', frame)
#            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
#
#            # Send the image over a WebSocket
#            await rx.send('camera_feed', jpg_as_text)
#
#        await asyncio.sleep(0.03)  # Add a small delay to avoid sending too many frames
#
#    cap.release()
#
## Start the camera stream on a separate thread
##rx.create_background_task(stream_camera)
#
## WebSocket route to handle streaming
#@rx.route('/camera_feed', type='websocket')
#async def camera_feed(websocket):
#    await websocket.accept()
#    while True:
#        image = await rx.receive('camera_feed')
#        await websocket.send_text(image)

async def camera_task():
    from .face_recog import stuff
    try:
        await stuff()
    except asyncio.CancelledError:
        print('camera task ended')
        return




def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        layout_with_video_and_another_component(),
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