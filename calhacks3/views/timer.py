import reflex as rx

def countdown_clock(time):
    return rx.box(
        rx.html("""
            <div id="countdown" style="font-family: Rubik Bubbles; font-size: 60px; color: #ff006c; text-align: center;"></div>
            <script>
                // Set the countdown time in seconds
                let countdownTime = """ + str(time) + """;  // For example, 60 seconds
                
                // Update the countdown every second
                let countdownInterval = setInterval(function() {
                    let minutes = Math.floor(countdownTime / 60);
                    let seconds = countdownTime % 60;

                    // Format minutes and seconds to display with leading zeros
                    minutes = minutes < 10 ? '0' + minutes : minutes;
                    seconds = seconds < 10 ? '0' + seconds : seconds;

                    // Display the result in the countdown div
                    document.getElementById('countdown').innerHTML = 'Countdown: ' + minutes + ':' + seconds;

                    // Decrease the time
                    countdownTime--;

                    // If the countdown reaches 0, display "Time's up!"
                    if (countdownTime < 0) {
                        clearInterval(countdownInterval);
                        document.getElementById('countdown').innerHTML = "Time's up!";
                    }
                }, 1000);  // Update every 1 second (1000 ms)
            </script>
        """),
        width="100%",
        align="center",
        padding="20px",
    )
