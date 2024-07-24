/* Functions that add interactivty to the front end 
* without creating errors in the console.
*/

function messageTimeout() {

    const messages = document.querySelectorAll('#msg .message');

        messages.forEach(message => {
            console.log('Message Classes:', message.className)

            let displayTime = 5000; // default display time for success and other messages

            if (message.classList.contains('alert-danger')) {
                console.log("Hannah 2")
                displayTime = 10000; // longer display time for error messages
            }

            setTimeout(() => {
                let messageDiv = document.getElementById("msg");
                if (messageDiv != null) {
                    messageDiv.remove();
                }
            }, displayTime);
        });
}

document.addEventListener('DOMContentLoaded', function(){
    try {
        messageTimeout();
    } catch (error) {
        //pass - no errors reported to console
    }
});