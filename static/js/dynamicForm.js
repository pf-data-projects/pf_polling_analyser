document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add_more').addEventListener('click', function(event) {
        event.preventDefault();
        // Get the formset wrapper
        const wrapper = document.getElementById('formset-wrapper');
        // Clone the last form in the formset
        const newForm = wrapper.querySelector('.formset-form:last-child').cloneNode(true);
        
        // Get the current total forms count from the management form
        const totalForms = document.querySelector('input[name="weights-TOTAL_FORMS"]');
        const formNum = parseInt(totalForms.value);

        // Update the new form's input names to increment the index
        newForm.querySelectorAll('input, select, textarea').forEach(input => {
            input.name = input.name.replace('-' + (formNum - 1) + '-', '-' + formNum + '-');
            input.id = input.id.replace('-' + (formNum - 1) + '-', '-' + formNum + '-');

            // Clear the values of the cloned inputs
            if (input.tagName === 'INPUT') {
                input.value = '';
            }
        });

        // Save form number in local storage
        localStorage.setItem('wgt-count', formNum)

        // Append the new form to the formset
        wrapper.appendChild(newForm);

        // Update the TOTAL_FORMS count
        totalForms.value = formNum + 1;

        // Add a listener for the remove button of the newly added form
        newForm.querySelector('.remove-form').addEventListener('click', removeForm);
        updateRemoveButtons()
    });

    function removeForm(event) {
        // Prevent default behavior
        event.preventDefault();

        // Get the form to be removed
        const formToRemove = event.target.closest('.formset-form');

        // Update the TOTAL_FORMS count
        const totalForms = document.querySelector('input[name="weights-TOTAL_FORMS"]');
        totalForms.value = parseInt(totalForms.value) - 1;

        // Remove the form
        formToRemove.remove();

        // Re-index all forms after the removed form to ensure the form prefix is continuous
        const forms = document.querySelectorAll('.formset-form');
        forms.forEach((form, index) => {
            form.querySelectorAll('input, select, textarea').forEach(input => {
                input.name = input.name.replace(/-\d+-/, '-' + index + '-');
                input.id = input.id.replace(/_\d+_/, '_' + index + '_');
            });
        });
        updateRemoveButtons()
    }

    // Attach remove event to all existing remove buttons
    document.querySelectorAll('.remove-form').forEach(btn => {
        btn.addEventListener('click', removeForm);
    });

    function updateRemoveButtons() {
        const forms = document.querySelectorAll('#formset-wrapper .formset-form');
        forms.forEach((form, index) => {
            const removeButton = form.querySelector('.remove-form');
            if (removeButton) {
                removeButton.style.display = (forms.length === 1) ? 'none' : 'inline-block';
            }
        });
    }
    updateRemoveButtons()

    // Attempt to add form data to local storage
    document.querySelector('#formset-wrapper').addEventListener('change', (event) => {
        if (event.target.matches('input, select, textarea')) {
            localStorage.setItem(event.target.name, event.target.value);
        }
    });

    function addForm() {
        // Get the formset wrapper
        const wrapper = document.getElementById('formset-wrapper');
        // Clone the last form in the formset
        const newForm = wrapper.querySelector('.formset-form:last-child').cloneNode(true);
        
        // Get the current total forms count from the management form
        const totalForms = document.querySelector('input[name="weights-TOTAL_FORMS"]');
        const formNum = parseInt(totalForms.value);

        // Update the new form's input names to increment the index
        newForm.querySelectorAll('input, select, textarea').forEach(input => {
            input.name = input.name.replace('-' + (formNum - 1) + '-', '-' + formNum + '-');
            input.id = input.id.replace('-' + (formNum - 1) + '-', '-' + formNum + '-');

            // Clear the values of the cloned inputs
            if (input.tagName === 'INPUT') {
                input.value = '';
            }
        });

        // Save form number in local storage
        localStorage.setItem('wgt-count', formNum)

        // Append the new form to the formset
        wrapper.appendChild(newForm);

        // Update the TOTAL_FORMS count
        totalForms.value = formNum + 1;

        // Add a listener for the remove button of the newly added form
        newForm.querySelector('.remove-form').addEventListener('click', removeForm);
        updateRemoveButtons() 
    }

    // Loading data from local storage
    window.onload = () => {
        // Restore the form count
        const formCount = localStorage.getItem('wgt-count') || 1; // Default to 1 if nothing is stored
        for (let i = 0; i < formCount; i++) {
            addForm(); // Replace with your function to add a new form to the formset
        }

        // Restore the form values
        document.querySelectorAll('input, select, textarea').forEach(element => {
            if (localStorage.getItem(element.name)) {
                element.value = localStorage.getItem(element.name);
            }
        });
    };
    
});