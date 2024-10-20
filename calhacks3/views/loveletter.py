import reflex as rx

import reflex as rx

# Define the app state to track the selected option
class SelectorState(rx.State):
    selected_option: int = 0

    # Function to update the selected option
    def select_option(self, option: int):
        self.selected_option = option

def selector_component():
    return rx.hstack(
        rx.spacer(),  # Spacer before the first button
        rx.button("💌 Letter",
                  on_click=lambda: SelectorState.select_option(1),
                  background_color=rx.cond(SelectorState.selected_option == 1, "#007bff", "#ffffff"),
                  color=rx.cond(SelectorState.selected_option == 1, "#ffffff", "#000000"),
                  border="2px solid #000",
                  padding="10px 36px",
                  cursor="pointer",
                  transition="background-color 0.3s"),
        rx.spacer(),  # Spacer between buttons
        rx.button("None",
                  on_click=lambda: SelectorState.select_option(2),
                  background_color=rx.cond(SelectorState.selected_option == 2, "#007bff", "#ffffff"),
                  color=rx.cond(SelectorState.selected_option == 2, "#ffffff", "#000000"),
                  border="2px solid #000",
                  padding="10px 36px",
                  cursor="pointer",
                  transition="background-color 0.3s"),
        rx.spacer(),  # Spacer between buttons
        rx.button("Video 🎞️",
                  on_click=lambda: SelectorState.select_option(3),
                  background_color=rx.cond(SelectorState.selected_option == 3, "#007bff", "#ffffff"),
                  color=rx.cond(SelectorState.selected_option == 3, "#ffffff", "#000000"),
                  border="2px solid #000",
                  padding="10px 36px",
                  cursor="pointer",
                  transition="background-color 0.3s"),
        rx.spacer(),  # Spacer after the last button
        justify="center",  # Ensures spacing between the buttons
        align="center",
        width="100%",
        max_width="400px",
        margin="20px auto"
    )


# Display the selected option
def selected_display(txt=''):
    return rx.text(
        rx.cond(
            SelectorState.selected_option == 1,
            rx.text('"', txt,'"',
                    font_family = "Rubik Bubbles", 
                    font_color = "#ffffff",
                    font_size = "36px"),
            rx.cond(
                SelectorState.selected_option == 2,
                rx.text("Just exploring huh. Maybe you're not the thoughtful type afterall", 
                        font_family = "Rubik Bubbles", 
                        font_color = "#ffffff",
                        font_size = "36px"),  # Ensure the argument is wrapped in rx.text
                rx.cond(
                 
                SelectorState.selected_option == 3, 
                rx.vstack(rx.html('<video controls width="500"><source src="http://localhost:4000/generated_vid.mp4" type="video/mp4" /></video>'), 'Generated Video'),
                rx.text(f"Selected: Option {SelectorState.selected_option}")  # Wrap the output in rx.text
                ),
            ),
        ),
        font_size="18px",
        text_align="center"
    )

# The main app component
def love_letter_selector(txt=''):
    return rx.vstack(
        selector_component(),  # Add the 3-way selector
        selected_display(txt),    # Add the display for the selected option
        spacing="20px"
    )

