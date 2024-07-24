    const capturedImage = document.getElementById('captured-image');
    const approveButton = document.getElementById('approve-button');
    const declineButton = document.getElementById('decline-button');
    const searchButton = document.getElementById('search-button');

    // Image Retrieving  from localStorage
    const capturedImageSrc = localStorage.getItem('capturedImage');
    if (capturedImageSrc) {
        capturedImage.src = capturedImageSrc;
    }

    approveButton.addEventListener('click', function () {
        alert('Approved!');
        // Removing captured image from localStorage
        localStorage.removeItem('capturedImage');
        // Close the page 
        window.close();
    });

    declineButton.addEventListener('click', function () {
        // Removing captured image from localStorage
        localStorage.removeItem('capturedImage');
        // Close the page 
        window.close();
    });

    searchButton.addEventListener('click', function () {
        const cnic = document.getElementById('cnic').value.trim();
        const license_no = document.getElementById('license_no').value.trim();
    
        if (cnic === '' && license_no === '') {
            alert('Please enter either CNIC or License No.');
        } else {
            const matchFound = true; 
    
            if (!matchFound) {
                const checkManuallyModalElement = document.getElementById('CheckManually');
                const checkManuallyModal = bootstrap.Modal.getInstance(checkManuallyModalElement);
    
                if (checkManuallyModal) {
                    document.getElementById('cnic').value = '';
                    document.getElementById('license_no').value = '';
                    checkManuallyModal.hide();
                    
                }
                const incorrectRecord = new bootstrap.Modal(document.getElementById('IncorrectRecord'));
                incorrectRecord.show();
            } else {
                window.location.href = 'display.html';
            }
        }
    });
    