/* Functions that add interactivty to the front end 
* without creating errors in the console.
*/

function messageTimeout() {
    setTimeout(function () {
        let message = document.getElementById("msg");
        if (message != null) {
            message.remove();
        }
    }, 5000);
}

document.addEventListener('DOMContentLoaded', function(){
    try {
        messageTimeout();
    } catch (error) {
        //pass - no errors reported to console
    }
});