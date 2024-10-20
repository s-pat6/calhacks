import csv
import os
import reflex as rx

# Path to the flower_data.csv file (relative path from views to components)
csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'components', 'flower_data.csv')

# Function to read the CSV file and return its data
def read_flower_data():
    data = []
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            # Skip the header
            next(csv_reader)
            for row in csv_reader:
                data.append(row)
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    return data

# Example usage of the read_flower_data function
flower_data = read_flower_data()

class FlowerState(rx.State):
    purchased: bool = False  # Track if a purchase has been made
    current_step: int = 0  # Initially set to 0
    product_name:str = flower_data[current_step][0]
    original_price:str = flower_data[current_step][1]
    current_price:str = flower_data[current_step][2]
    image_url:str = flower_data[current_step][3]

    def next_button(self):
        self.purchased = False
        self.current_step = (self.current_step + 1) % 20  # Loop through 20 steps
        self.product_name = flower_data[self.current_step][0]
        self.original_price = flower_data[self.current_step][1]
        self.current_price = flower_data[self.current_step][2]
        self.image_url = flower_data[self.current_step][3]

    def prev_button(self):
        self.purchased = False
        self.current_step = (self.current_step - 1) % 20  # Loop through 20 steps
        self.product_name = flower_data[self.current_step][0]
        self.original_price = flower_data[self.current_step][1]
        self.current_price = flower_data[self.current_step][2]
        self.image_url = flower_data[self.current_step][3]

    @rx.var
    def current_index(self) -> int:
        return self.current_step
    
    purchased: bool = False  # Track if a purchase has been made

    # Function to indicate purchase
    def purchase(self):
        self.purchased = True  # Set the purchase flag to True
        rx.redirect('https://your-purchase-link.com')
        
def display_first_item():
    if flower_data:
        # index = int(FlowerState.current_step)
        first_item = flower_data[0]  # Get the first item
        product_name = FlowerState.product_name # Assuming first column is product name
        original_price = FlowerState.original_price  # Assuming second column is original price
        current_price = FlowerState.current_price  # Assuming third column is current price
        image_url = FlowerState.image_url  # Assuming fourth column is image URL

        # Return a Reflex component with a white card containing the image and price
        return rx.box(
        rx.text("4 Hour Delivery",
                color="#000000",  # Set the text color to white
                font_family="Rubik Bubbles",  # Set the font to Rubik Bubbles
                font_size = "36px",
                text_align = 'center',
                ),
        rx.hstack(
            rx.spacer(),
            # VStack for vertical stacking of image and text in the card
            rx.button(
                    "<", 
                    on_click=FlowerState.prev_button,
                    width="100px",
                    height="50px",
                    padding="10px",
                    border_radius="10px",  # Slightly curved button corners
                    background_color="#000000",  # Set the background color to black
                    color="#ffffff",  # Set the text color to white
                    font_family="Rubik Bubbles",  # Set the font to Rubik Bubbles
                    font_size = "36px",
                    transition="all 0.3s ease-in-out",  # Ensure smooth hover-out
                    _hover={
                    "background_color": "#330001",  # Change background color on hover
                    "transform": "scale(1.05)",  # Slightly increase size on hover
                    
                }
                )
                ,

            rx.box(
                rx.vstack(
                    rx.image(
                        src=image_url, 
                        alt=product_name, 
                        width="200px", 
                        height="200px", 
                        border_radius="15px",  # Curved corners for the image
                    ),
                    rx.text(
                        f"{product_name}", 
                        color="#ff006c",  # Pink text color
                        font_size="16px", 
                        font_family="Rubik Bubbles",  # Set font to Rubik Bubbles
                        text_align="center"  # Center the text
                    ),
                    rx.text(
                        f"Original Price: {original_price}", 
                        color="#000000", 
                        font_size="8px", 
                        text_decoration="line-through", 
                        font_family="Rubik Bubbles",  # Set font to Rubik Bubbles
                        text_align="center"  # Center the text
                    ),
                    rx.text(
                        f"Price: {current_price}", 
                        color="#000000",  # Black text color
                        font_size="16px", 
                        font_family="Rubik Bubbles",  # Set font to Rubik Bubbles
                        text_align="center"  # Center the text
                    ),
                    rx.button(
                        "Purchase",
                        font_family = "Rubik Bubbles",
                        font_size = "16px",
                        font_color = "ff006c",
                        align = "center",
                        background_color = "#000000",
                        on_click=rx.redirect(
                            "https://www.fromyouflowers.com/products/be_bold_on_your_birthday.htm",
                            external=True,
                        ),
                        transition="all 0.3s ease-in-out",  # Ensure smooth hover-out

                            # Hover effect
                            _hover={
                                "background_color": "#330001",  # Change background color on hover
                                "transform": "scale(1.05)",  # Slightly increase size on hover
                                
                            }
                    ),
                    spacing="15px",  # Space between elements in vstack
                    padding="10px",
                    align_items="center",  # Ensure all content inside the vstack is centered
                ),
                
                on_click=FlowerState.purchase,  # Correctly place the on_click handler
                width="auto",  # Allow the box to auto-adjust width
                max_width="400px",  # Set max width to match the image width
                bg="#ffffff",  # White background for the card
                border_radius="15px",  # Curved edges for the card
                shadow="lg",  # Add a shadow to make it look like a card
                cursor="pointer",  # Change cursor to pointer to indicate clickability
                # Add default transition (for smooth hover-out effect)
                transition="all 0.3s ease-in-out",  # Ensure smooth hover-out

                # Add hover effect for scaling
                _hover={
                    "transform": "scale(1.05)",  # Scale up to 105% on hover
                }

            ),
            # The "Next" button placed to the right of the card
            rx.button(
                ">", 
                on_click=FlowerState.next_button,
                width="100px",
                height="50px",
                padding="10px",
                border_radius="10px",  # Slightly curved button corners
                background_color="#000000",  # Set the background color to black
                color="#ffffff",  # Set the text color to white
                font_family="Rubik Bubbles",  # Set font to Rubik Bubbles
                font_size="36px",
                transition="all 0.3s ease-in-out",  # Ensure smooth hover-out

                # Hover effect
                _hover={
                    "background_color": "#330001",  # Change background color on hover
                    "transform": "scale(1.05)",  # Slightly increase size on hover
                    
                }
            ),
            rx.spacer()
            ,
            justify="flex-start",  # Align items to the left side horizontally
            align="center",  # Align items vertically in the middle
            spacing="10px",  # Space between the card and the button
            padding="10px",  # Padding around the hstack
            # border_color = "#000000",
            # border_width = '5px',
        ),
        # Show purchase message if purchased
        
        )
    else:
        return rx.text("No data available", color="#FFFFFF")

# In your layout or component call the display_first_item function
layout = display_first_item()
