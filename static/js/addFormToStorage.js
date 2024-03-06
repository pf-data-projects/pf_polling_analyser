document.addEventListener('DOMContentLoaded', () => {
    console.log("Hello World!")
    const form = document.getElementById('table-form');

    // Save form data to localStorage
    function saveFieldData(event) {
        const element = event.target;
        if (element.name) {
          // Retrieve existing formData object from localStorage, or initialize a new one if it doesn't exist
          const savedFormData = localStorage.getItem('formData');
          const formDataObject = savedFormData ? JSON.parse(savedFormData) : {};
      
          // Update formData object with the new value of the changed field
          formDataObject[element.name] = element.value;
      
          // Save the updated formData object back to localStorage
          localStorage.setItem('formData', JSON.stringify(formDataObject));
        }
    }

    function retrieveFormData() {
        const savedFormData = localStorage.getItem('formData');
      
        if (savedFormData) {
          const formDataObject = JSON.parse(savedFormData);
          Array.from(form.elements).forEach(element => {
            if (element.name && formDataObject.hasOwnProperty(element.name)) {
              element.value = formDataObject[element.name];
            }
          });
        }
    }

    // Add change event listener to each form field
    Array.from(form.elements).forEach(element => {
        if (element.name) {
            element.addEventListener('change', saveFieldData);
        }
    });

    // Use window.onload to retrieve and pre-fill form data when the page loads
    window.onload = retrieveFormData;
});