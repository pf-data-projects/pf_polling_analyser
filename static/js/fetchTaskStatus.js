document.addEventListener('DOMContentLoaded', () => {
    // Define the function to call the Django view without a task ID parameter
function fetchTaskStatus() {
    // Construct the URL to your Django view. Replace `your-backend-url` and `endpoint` with your actual backend URL and the correct endpoint.
    const url = `/check_task/`;
  
    // Use the fetch API to call your Django view
    fetch(url)
      .then(response => {
        // Check if the request was successful
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response body
      })
      .then(data => {
        // Update the <p> element with the task status
        const progressElement = document.getElementById('progress');
        const firstBar = document.getElementById('bar-1');
        const firstWrapper = document.getElementById("bar-1-wrapper");
        const secondBar = document.getElementById('bar-2');
        const secondWrapper = document.getElementById("bar-2-wrapper");

        if (progressElement) {
            // Convert the JSON object to a string for display
            if (data.status === "No tasks have been run yet...") {
              console.log("nope")
              progressElement.textContent = "No data is currently processing"
            }
            else if (data.status === "PROGRESS" && data.details.Totals) {
              progressElement.textContent = "Calculating the totals..."
            }
            else if (data.status === "PROGRESS" && "StandardCB" in data.details) {
              progress = Number(data.details.StandardCB)
              total = Number(data.details.total)
              progressElement.textContent = `${progress} / ${total} standard crossbreaks done`
              // console.log(progress, total)
              firstBar.style.height = "100%"
              firstWrapper.style.height = "20px"
              firstWrapper.style.border = "solid 2px black"
              firstBar.style.width = `${progress/total * 100}%`
            }
            else if (data.status === "PROGRESS" && "nonStandardCB" in data.details) {
              progress = Number(data.details.nonStandardCB)
              total = Number(data.details.total)
              progressElement.textContent = `${progress} / ${total} non-standard crossbreaks done`
              // console.log(progress, total)
              firstBar.style.height = "100%"
              firstWrapper.style.height = "20px"
              firstWrapper.style.border = "solid 2px black"
              firstBar.style.width = `${progress/total * 100}%`
            }
            else if (data.status === "PROGRESS" && "rebaseStandardCB" in data.details) {
              progress = Number(data.details.rebaseStandardCB)
              total = Number(data.details.total)
              progressElement.textContent = `${progress} / ${total} standard crossbreaks rebased`
              // console.log(progress, total)
              firstBar.style.height = "100%"
              firstWrapper.style.height = "20px"
              firstWrapper.style.border = "solid 2px black"
              firstBar.style.width = `${progress/total * 100}%`
            }
            else if (data.status === "PROGRESS" && "rebaseNonStandardCB" in data.details) {
              progress = Number(data.details.rebaseNonStandardCB)
              total = Number(data.details.total)
              progressElement.textContent = `${progress} / ${total} non-standard crossbreaks rebased`
              // console.log(progress, total)
              firstBar.style.height = "100%"
              firstWrapper.style.height = "20px"
              firstWrapper.style.border = "solid 2px black"
              firstBar.style.width = `${progress/total * 100}%`
            }
            else if (data.status === "PENDING") {
              progressElement.textContent = "Waiting for processing to start..."
              console.log(data)
            }
            else if (data.status === "PROGRESS" && "CreatingHeaders" in data.details) {
              progressElement.textContent = "Creating rebase headers, preparing files for download."
              // console.log("WAITING")
            }
            else if (data.status === "SUCCESS") {
              progressElement.textContent = "Data processing complete. Please download your files!"
              progressElement.style.color = "darkgreen"
              progressElement.style.fontWeight = "700"
              progressElement.style.backgroundColor = "#c0fcd0"
              progressElement.style.padding = "20px"
              progressElement.classList.add('rounded')
              firstWrapper.style.height = "0px"
              firstWrapper.style.border = "none"
              secondWrapper.style.height = "0px"
              secondWrapper.style.border = "none"
              console.log("COMPLETED")
            }
            else if (data.status === "FAILURE") {
              console.log(data)
              html = `<p><strong>There was an error when running this code for crossbreaks.
                      The most likely cause of this error is entering a crossbreak that
                      doesn't exist in the data.
          
                      It could also be caused by changes in the wording of standard crossbreak
                      questions.
          
                      Here is the content of the error message:</strong></p>
                      <p>${data.traceback}</p>`
              progressElement.innerHTML = html
              progressElement.style.color = "darkred"
              progressElement.style.backgroundColor = "#ffcccb"
              progressElement.style.padding = "20px"
              progressElement.classList.add('rounded')

            }
            else {
              console.log("This one is always triggering")
              progressElement.textContent = JSON.stringify(data, null, 2);
            }
        }
  
        // Depending on your requirements, you may want to stop polling when the task completes
        if (data.status === 'SUCCESS' || data.status === 'FAILURE') {
          console.log('Task completed or failed:', data);
          clearInterval(pollingInterval); // Stop polling
        }
      })
      .catch(error => {
        // Handle any errors that occurred during the fetch
        console.error('Failed to fetch task status:', error);
      });
  }
  // Start polling the endpoint every half second (500 milliseconds)
  const pollingInterval = setInterval(fetchTaskStatus, 100);  
})