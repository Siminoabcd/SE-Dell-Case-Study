let filters = ["This is Filter", "Hello World", "GrayScale"];

$(document).ready(function() {
    // Initial display of filters
    displayFilters(filters);
    
    // Event listener for submit button
    $('.submit-button').click(function() {
        // Get the value of the input field
        let inputValue = $('#input-filter').val();
        filters.push(inputValue);
        displayFilters(filters);
    });

    // Event listener for close button
    $(document).on('click', '.btn-close', function() {
        // Get the parent card-body element
        const cardBody = $(this).closest('.card-body');
        
        // Get the filter text inside the card-body
        const filterText = cardBody.find('p').text();

        // Find the index of the filter text in the filters array
        const index = filters.indexOf(filterText);
        
        // If index is found
        if (index !== -1) {
            // Remove the filter text from the filters array
            filters.splice(index, 1);
            
            // Update the display of filters
            displayFilters(filters);
        }
    });
});

// Function to display filters
const displayFilters = (filters) => {
    // Get the container element where filters will be displayed
    const container = $('.filter-container');
    
    // Clear any existing content in the container
    container.empty();

    // Loop through the filters array
    filters.forEach((filterText) => {
        // Create the card element
        const card = $('<div>').addClass('card filter-card');

        // Create the card body element
        const cardBody = $('<div>').addClass('card-body');

        // Create the paragraph element for filter text
        const paragraph = $('<p>').text(filterText);

        // Create the button element
        const closeButton = $('<button>').attr('type', 'button').addClass('btn-close').attr('aria-label', 'Close');

        // Append paragraph and button to the card body
        cardBody.append(paragraph).append(closeButton);

        // Append card body to the card
        card.append(cardBody);

        // Append the card to the container
        container.append(card);
    });
};
