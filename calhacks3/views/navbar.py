import reflex as rx


def navbar():
    return rx.flex(
        rx.spacer(),  # Spacer to push content from the left
        rx.hstack(
            rx.image(src="/ForgetMeNotLogo.png", width="60px", height="60px"),  # Logo
            rx.text("ForgetMeNot", 
                    font_family="Rubik Bubbles", 
                    font_size="36px", 
                    font_weight="thin",  # Correct use of font_weight
                    color="#ff006c"),  # Add text with custom font
            align="center",
            spacing="3",
        ),
        rx.spacer(),  # Spacer to push content to the right
        align="center",
        spacing="2",
        flex_direction="row",  # Horizontal alignment for the flex container
        width="100%",
        background_color='#000000',  # Set background color to black
        
        padding="10px",  # Padding for better spacing inside the navbar
        position="fixed",  # Keep the navbar fixed at the top
        top="0px",  # Position it at the very top
        left="0px",  # Ensure it spans the full width
        right="0px",  # Ensures the navbar stretches from left to right
        z_index="1000",  # Keep the navbar on top of other content
        margin="0",  # Remove any potential default margin
    )
