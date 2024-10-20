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
        # Outer container with border (the "frame")
        rx.box(
            # Inner container with the image and curved inner corners
            rx.image(src=ImageState.image, on_mount=ImageState.run_my_task),
            width="100%",  # Full width of the inner container
            height="100%",  # Full height of the inner container
            border_radius="15px",  # Apply curved corners to the inner image
            overflow="hidden",  # Ensure the image doesn't overflow outside the box
        ),
        width="50%",  # Set width of the camera feed box
        height="auto",  # Auto height to match the image
        border_radius="10px",  # Border radius for the outer container (frame)
        overflow="hidden",  # Ensure no overflow outside the container
        border="15px solid #ff006c",  # Set border with color and width for the frame
    )


# State to keep track of the current step
class ButtonState(rx.State):
    current_step: int = 0  # Initially set to 0

    # Method to go to the next step
    def next_button(self):
        self.current_step = (self.current_step + 1) % 5  # Loop through 5 steps

# Function to display the safety measure deployment interface
def deploy_safety_measures() -> rx.Component:
    return rx.box(
        rx.spacer(),
        rx.text(
            "...Let's Deploy Safety Protocol!",
            font_size='36px',
            font_family="Rubik Bubbles",
            color="#ff006c",
            text_align="center",
        ),
        rx.spacer(),
        rx.flex(
            # First button
            rx.cond(
                ButtonState.current_step % 5 == 0,  # Conditionally render based on step
                rx.button(
                    "Gaslight!",
                    on_click=ButtonState.next_button,  # Clickable only if it's the current step
                    color="#FFFFFF",
                    background_color="#ff006c",
                    border_radius="50px",
                    _hover={"background_color": "#000000"},
                    transition="background-color 0.3s ease",
                    width="150px",
                    height="50px",
                    margin="0 20px",
                    border="2px solid #ff006c",  # Outline for the active button
                ),
                rx.button(
                    "Gaslight!",
                    color="#FFFFFF",
                    background_color="#000000",  # Not clickable, black background for others
                    border_radius="50px",
                    width="150px",
                    height="50px",
                    margin="0 20px",
                    cursor="not-allowed",  # Indicate it's not clickable
                    border="2px solid #ff006c",  # Pink outline for inactive buttons
                )
            ),

            # Second button
            rx.cond(
                ButtonState.current_step % 5 == 1,  # Conditionally render based on step
                rx.button(
                    "Love Letter!",
                    on_click=ButtonState.next_button,  # Clickable only if it's the current step
                    color="#FFFFFF",
                    background_color="#ff006c",
                    border_radius="50px",
                    _hover={"background_color": "#000000"},
                    transition="background-color 0.3s ease",
                    width="150px",
                    height="50px",
                    margin="0 20px",
                    border="2px solid #ff006c",  # Outline for the active button
                ),
                rx.button(
                    "Love Letter!",
                    color="#FFFFFF",
                    background_color="#000000",  # Not clickable, black background for others
                    border_radius="50px",
                    width="150px",
                    height="50px",
                    margin="0 20px",
                    cursor="not-allowed",  # Indicate it's not clickable
                    border="2px solid #ff006c",  # Pink outline for inactive buttons
                )
            ),

            # Third button
            rx.cond(
                ButtonState.current_step % 5 == 2,  # Conditionally render based on step
                rx.button(
                    "Flowers",
                    on_click=ButtonState.next_button,  # Clickable only if it's the current step
                    color="#FFFFFF",
                    background_color="#ff006c",
                    border_radius="50px",
                    _hover={"background_color": "#000000"},
                    transition="background-color 0.3s ease",
                    width="150px",
                    height="50px",
                    margin="0 20px",
                    border="2px solid #ff006c",  # Outline for the active button
                ),
                rx.button(
                    "Flowers",
                    color="#FFFFFF",
                    background_color="#000000",  # Not clickable, black background for others
                    border_radius="50px",
                    width="150px",
                    height="50px",
                    margin="0 20px",
                    cursor="not-allowed",  # Indicate it's not clickable
                    border="2px solid #ff006c",  # Pink outline for inactive buttons
                )
            ),

            # Fourth button
            rx.cond(
                ButtonState.current_step % 5 == 3,  # Conditionally render based on step
                rx.button(
                    "3D Print",
                    on_click=ButtonState.next_button,  # Clickable only if it's the current step
                    color="#FFFFFF",
                    background_color="#ff006c",
                    border_radius="50px",
                    _hover={"background_color": "#000000"},
                    transition="background-color 0.3s ease",
                    width="150px",
                    height="50px",
                    margin="0 20px",
                    border="2px solid #ff006c",  # Outline for the active button
                ),
                rx.button(
                    "3D Print",
                    color="#FFFFFF",
                    background_color="#000000",  # Not clickable, black background for others
                    border_radius="50px",
                    width="150px",
                    height="50px",
                    margin="0 20px",
                    cursor="not-allowed",  # Indicate it's not clickable
                    border="2px solid #ff006c",  # Pink outline for inactive buttons
                )
            ),

            # Fifth button
            rx.cond(
                ButtonState.current_step % 5 == 4,  # Conditionally render based on step
                rx.button(
                    "Home",
                    on_click=ButtonState.next_button,  # Clickable only if it's the current step
                    color="#FFFFFF",
                    background_color="#ff006c",
                    border_radius="50px",
                    _hover={"background_color": "#000000"},
                    transition="background-color 0.3s ease",
                    width="150px",
                    height="50px",
                    margin="0 20px",
                    border="2px solid #ff006c",  # Outline for the active button
                ),
                rx.button(
                    "Home",
                    color="#FFFFFF",
                    background_color="#000000",  # Not clickable, black background for others
                    border_radius="50px",
                    width="150px",
                    height="50px",
                    margin="0 20px",
                    cursor="not-allowed",  # Indicate it's not clickable
                    border="2px solid #ff006c",  # Pink outline for inactive buttons
                )
            ),

            justify="center",
            align="center",
            width="100%",  # Ensures the buttons are evenly spaced across the full width
            padding="20px",
        ),
        width="100%",
        align="center",
        padding="10px",
    )

# Function to dynamically change the text based on the current step
def dynamic_text():
    return rx.cond(
        ButtonState.current_step == 1,
        rx.text(
            "Gaslight!",  # Change the text to "Gaslight!"
            font_family="Rubik Bubbles", 
            font_size="36px", 
            font_weight="thin",  
            color="#FFFFFF",
            text_align="left"
        ),
        rx.cond(
            ButtonState.current_step == 2,
            rx.text(
                "Love Letter!",  # Change the text to "Love Letter!"
                font_family="Rubik Bubbles", 
                font_size="36px", 
                font_weight="thin",  
                color="#FFFFFF",
                text_align="left"
            ),
            rx.cond(
                ButtonState.current_step == 3,
                rx.text(
                    "Flowers",  # Change the text to "Flowers"
                    font_family="Rubik Bubbles", 
                    font_size="36px", 
                    font_weight="thin",  
                    color="#FFFFFF",
                    text_align="left"
                ),
                rx.cond(
                    ButtonState.current_step == 4,
                    rx.text(
                        "3D Print",  # Change the text to "3D Print"
                        font_family="Rubik Bubbles", 
                        font_size="36px", 
                        font_weight="thin",  
                        color="#FFFFFF",
                        text_align="left"
                    ),
                    rx.cond(
                        ButtonState.current_step == 0,
                        rx.box(
                            rx.text(
                                "What! I'd never forget your...",  # Default text for "Home"
                                font_family="Rubik Bubbles", 
                                font_size="36px", 
                                font_weight="thin",  
                                color="#FFFFFF",
                                text_align="left"
                            ),
                            rx.text(
                                "Oh wait we're good :D",  # Secondary text for "Home"
                                font_weight="bold",
                                color="#ffffff",
                                text_align="left"
                            ),
                        ),
                        rx.text(  # Fallback if no condition matches
                            "What! I'd never forget your...", 
                            font_family="Rubik Bubbles", 
                            font_size="36px", 
                            font_weight="thin",  
                            color="#FFFFFF",
                            text_align="left"
                        )
                    )
                )
            )
        )
    )

def layout_with_video_and_another_component():
    return rx.flex(
        camera_feed(),  # Video on the left
        rx.box(
            rx.box(
            dynamic_text(),  # Dynamically changing text based on the button pressed
            bg="#ff006c",  # Background color of the text box
            width="50%",  # Take the remaining 50% width
            height="auto",  # Auto adjust height to match camera feed
            display="flex",  # Flexbox display
            flex_direction="column",  # Stack text items vertically
            justify="center",  # Center text vertically
            align="flex-end",  # Right-align the text box
            padding="15px",  # Add padding for inner spacing
            ),
            bg="#ff006c",  # Background color of the text box
            width="50%",  # Take the remaining 50% width
            height="auto",  # Auto adjust height to match camera feed
            display="flex",  # Flexbox display
            flex_direction="column",  # Stack text items vertically
            justify="center",  # Center text vertically
            align="flex-end",  # Right-align the text box
            padding="15px",  # Add padding for inner spacing
            border_radius="15px",  # Rounded corners
        ),
        flex_direction="row",  # Layout both components in a row (side by side)
        width="100%",  # The entire flex container takes up 100% width
        height="auto",  # Automatically adjust the height to fit both components
        align_items="stretch",  # Align items to stretch to the same height
        background="#ff006c",  # Background color
        border_radius="15px",  # Ensure rounded border effect for the entire layout
    )
