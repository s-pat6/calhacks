import reflex as rx

def deploy_safety_measures() -> rx.Component:
    return rx.box(
        rx.box(
            rx.flex(
                rx.box(
                    rx.button("1",
                              color="#FFFFFF",
                              font_family="Rubik Bubbles",
                              width="100px",  # Button size
                              height="100px",
                              text_align="center",
                              background_color="#ff006c",
                              border_radius="50%",  # Rounder buttons
                              _hover={"background_color": "#000000"},  # Hover effect
                              transition="background-color 0.3s ease"  # Gradual hover
                              ),
                    width="20%",  # Box width
                    bg="#000000",  # Black background for the box
                    display="flex",  # Ensures button is centered inside
                    justify="center",
                    align_items="center"
                ),  # First button in box

                rx.box(
                    rx.button("2",
                              color="#FFFFFF",
                              font_family="Rubik Bubbles",
                              width="100px",
                              height="100px",
                              text_align="center",
                              background_color="#ff006c",
                              border_radius="50%",
                              _hover={"background_color": "#000000"},
                              transition="background-color 0.3s ease"
                              ),
                    width="20%",  # Box width
                    bg="#000000",  # Black background for the box
                    display="flex",
                    justify="center",
                    align_items="center"
                ),  # Second button in box

                rx.box(
                    rx.button("3",
                              color="#FFFFFF",
                              font_family="Rubik Bubbles",
                              width="100px",
                              height="100px",
                              text_align="center",
                              background_color="#ff006c",
                              border_radius="50%",
                              _hover={"background_color": "#000000"},
                              transition="background-color 0.3s ease"
                              ),
                    width="20%",  # Box width
                    bg="#000000",  # Black background for the box
                    display="flex",
                    justify="center",
                    align_items="center"
                ),  # Third button in box

                rx.box(
                    rx.button("4",
                              color="#FFFFFF",
                              font_family="Rubik Bubbles",
                              width="100px",
                              height="100px",
                              text_align="center",
                              background_color="#ff006c",
                              border_radius="50%",
                              _hover={"background_color": "#000000"},
                              transition="background-color 0.3s ease"
                              ),
                    width="20%",  # Box width
                    bg="#000000",  # Black background for the box
                    display="flex",
                    justify="center",
                    align_items="center"
                ),  # Fourth button in box

                rx.box(
                    rx.button("5",
                              color="#FFFFFF",
                              font_family="Rubik Bubbles",
                              width="100px",
                              height="100px",
                              text_align="center",
                              background_color="#ff006c",
                              border_radius="50%",
                              _hover={"background_color": "#000000"},
                              transition="background-color 0.3s ease"
                              ),
                    width="20%",  # Box width
                    bg="#000000",  # Black background for the box
                    display="flex",
                    justify="center",
                    align_items="center"
                ),  # Fifth button in box

                justify="space-between",  # Spacing between the boxes
                width="100%",  # Full width of the container
                align="center",  # Align boxes vertically in the center
            ),
            height="auto",  # Rectangle height
            width="100%",  # Full width of the rectangle
            position="relative",  # Position relative to its parent container
        ),
        width="90%",  # Width of the outer container
        margin="0 auto",  # Center the entire component horizontally
        padding="10px",  # Padding around the box
        align="center",
        border="2px solid #ff006c",  # Border color and thickness
        border_radius="15px",  # Rounded corners
    )
