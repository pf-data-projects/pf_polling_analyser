document.addEventListener('DOMContentLoaded', () => {
    // Define the function to call the Django view
    function fetchTaskStatus(taskId) {
        // Construct the URL to your Django view. Replace `your-backend-url` and `endpoint` with your actual backend URL and the correct endpoint.
        const url = `https://your-backend-url.com/endpoint?task_id=${taskId}`;
    
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
            // Handle the response data here
            console.log('Task Status:', data);
    
            // Example of handling different states
            if (data.status === 'SUCCESS') {
                console.log('Result:', data.result); // Task completed successfully
            } else if (data.status === 'PENDING') {
                console.log('Task is still pending.'); // Task is still running
            } else if (data.status === 'FAILURE') {
                console.error('Task failed:', data.error); // Task failed
            }
        })
        .catch(error => {
            // Handle any errors that occurred during the fetch
            console.error('Failed to fetch task status:', error);
        });
    }
    // Example usage of the function
    // Replace 'your-task-id' with the actual task ID you want to check
    fetchTaskStatus('your-task-id');
})