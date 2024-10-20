import reflex as rx

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
