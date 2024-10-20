import asyncio
import reflex as rx
from PIL import Image


#class ImageState(rx.State):
#    url: str = "https://github.com/reflex-dev"
#    profile_image: str = (
#        "https://avatars.githubusercontent.com/u/104714959"
#    )
#
#    def set_profile(self, username: str):
#        if username == "":
#            return
#        github_data = requests.get(
#            f"https://api.github.com/users/{username}"
#        ).json()
#        self.url = github_data["url"]
#        self.profile_image = github_data["avatar_url"]

from ..face_recog import latestimg
class ImageState(rx.State):
    image = Image.frombytes("L", (100,100) ,b'\0' * (100 * 100))
    
    def run_my_task(self):
        print('executing my task')
        return ImageState.my_task
    @rx.background
    async def my_task(self):
        while True:
            async with self:
                #print('updating in loop', latestimg[0] is None, latestimg[0] == None, latestimg[0] == 'a')
                self.image = latestimg

            # Await long operations outside the context to avoid blocking UI
            await asyncio.sleep(0.5)


def camera_feed():
    return rx.box(
        rx.image(src=ImageState.image, on_mount=ImageState.run_my_task),
        width="100%",
        border_radius="15px",  # Inner box border-radius
        overflow="hidden",  # Ensures the content doesn't exceed the border radius
    )


def layout_with_video_and_another_component():
    return rx.flex(
        camera_feed(),  # Video on the left
        rx.box(
            rx.text("What! I'd never forget your...", 
                    font_family="Rubik Bubbles", 
                    font_size="36px", 
                    font_weight="thin",  # Correct use of font_weight
                    color="#FFFFFF"),  # Add text with custom font
            rx.text("Oh wait we're good :D",
                    font_weight = "bold",
                    color = "#ffffff"),
            bg="#ff006c",  # You can style this as needed
            width="50%",  # The other component takes the remaining 50% width
            height="auto",  # Match the height of the left camera feed box
            align="center",
            justify="center",
            padding="15px",  # Add padding if needed for consistent layout
            border_radius="15px",  # Ensure the right box has the same rounded borders
        ),
        flex_direction="row",  # Layout with both components in a row (side by side)
        width="100%",  # The entire flex container takes up 100% width
        height="auto",  # Automatically adjust the height to fit both components
        align_items="stretch",  # Align items to stretch them to the same height
        background="#ff006c",  # Background color to simulate the border effect
        border_radius="15px",
    )
