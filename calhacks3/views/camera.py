import reflex as rx


def camera_feed():
    return rx.box(
        rx.html("""
            <div style="position: relative; width: 100%; padding-top: 56.25%; overflow: hidden;">
                <img id="camera" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;" />
                <script>
                    const cameraElement = document.getElementById('camera');
                    const socket = new WebSocket('ws://localhost:8000/camera_feed');  // WebSocket URL
                    
                    // Listen for incoming image data from the server
                    socket.onmessage = function(event) {
                        cameraElement.src = 'data:image/jpeg;base64,' + event.data;
                    };
                </script>
            </div>
        """),
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
