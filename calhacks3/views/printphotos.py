import reflex as rx

image_data = [
    {
        "name": "HandBag",
        "time": "1 hr 12 min",
        "link": "/handbag.jpg"
    },
    {
        "name": "Key Ring",
        "time": "12 min",
        "link": "/keyring.jpg"
    },
    {
        "name": "Tealight Holder",
        "time": "3 hr 46 min",
        "link": "/tealight holder.jpg"
    },
    {
        "name": "Wallet",
        "time": "18.5 min",
        "link": "/wallet.jpg"
    }
]

# Create a state to handle the image rotation
class ImageState(rx.State):
    purchased: bool = False  # Track if a purchase has been made
    current_step: int = 0  # Initially set to 0
    product_name: str = image_data[current_step]["name"]
    time_required: str = image_data[current_step]["time"]
    image_url: str = image_data[current_step]["link"]

    # Handle next button to move to the next image
    def next_button(self):
        self.purchased = False
        self.current_step = (self.current_step + 1) % len(image_data)  # Loop through the list
        self.product_name = image_data[self.current_step]["name"]
        self.time_required = image_data[self.current_step]["time"]
        self.image_url = image_data[self.current_step]["link"]

    # Handle previous button to move to the previous image
    def prev_button(self):
        self.purchased = False
        self.current_step = (self.current_step - 1) % len(image_data)  # Loop through the list
        self.product_name = image_data[self.current_step]["name"]
        self.time_required = image_data[self.current_step]["time"]
        self.image_url = image_data[self.current_step]["link"]

    @rx.var
    def current_index(self) -> int:
        return self.current_step

# Function to display the first item
def display_first_item_3d():
    if image_data:
        # Load the first item (initial)
        first_item = image_data[0]
        product_name = ImageState.product_name
        time_required = ImageState.time_required
        image_url = ImageState.image_url

        # Return the Reflex components for the card
        return rx.box(
            rx.text("4 Hour Delivery",
                    color="#000000",
                    font_family="Rubik Bubbles",
                    font_size="36px",
                    text_align='center',
            ),
            rx.hstack(
                rx.spacer(),
                # Previous Button
                rx.button(
                    "<", 
                    on_click=ImageState.prev_button,
                    width="100px",
                    height="50px",
                    padding="10px",
                    border_radius="10px",
                    background_color="#000000",
                    color="#ffffff",
                    font_family="Rubik Bubbles",
                    font_size="36px",
                    transition="all 0.3s ease-in-out",
                    _hover={
                        "background_color": "#330001",
                        "transform": "scale(1.05)",
                    }
                ),
                # Image and Text Card
                rx.box(
                    rx.vstack(
                        rx.image(
                            src=image_url, 
                            alt=product_name, 
                            width="200px", 
                            height="200px", 
                            border_radius="15px",
                        ),
                        rx.text(
                            f"{product_name}",
                            color="#ff006c",
                            font_size="16px",
                            font_family="Rubik Bubbles",
                            text_align="center"
                        ),
                        rx.text(
                            f"Time Required: {time_required}",
                            color="#000000",
                            font_size="16px",
                            font_family="Rubik Bubbles",
                            text_align="center"
                        ),
                        rx.button(
                            "Print",
                            font_family="Rubik Bubbles",
                            font_size="16px",
                            font_color="#ff006c",
                            background_color="#000000",
                            transition="all 0.3s ease-in-out",
                            _hover={
                                "background_color": "#330001",
                                "transform": "scale(1.05)",
                            }
                        ),
                        spacing="15px",
                        padding="10px",
                        align_items="center",
                    ),
                    width="auto",
                    max_width="400px",
                    bg="#ffffff",
                    border_radius="15px",
                    shadow="lg",
                    cursor="pointer",
                    transition="all 0.3s ease-in-out",
                    _hover={
                        "transform": "scale(1.05)",
                    }
                ),
                # Next Button
                rx.button(
                    ">", 
                    on_click=ImageState.next_button,
                    width="100px",
                    height="50px",
                    padding="10px",
                    border_radius="10px",
                    background_color="#000000",
                    color="#ffffff",
                    font_family="Rubik Bubbles",
                    font_size="36px",
                    transition="all 0.3s ease-in-out",
                    _hover={
                        "background_color": "#330001",
                        "transform": "scale(1.05)",
                    }
                ),
                rx.spacer(),
                justify="flex-start",
                align="center",
                spacing="10px",
                padding="10px",
            )
        )
    else:
        return rx.text("No data available", color="#FFFFFF")
