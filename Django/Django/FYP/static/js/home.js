// Home.html

let checkManually;
var matchFound;

(async function () {
    const video = document.getElementById('video');
    const captureButton = document.getElementById('capture-btn');
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        
        video.srcObject = stream;

        captureButton.addEventListener('click', () => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');

            // Flip the image horizontally
            ctx.translate(canvas.width, 0);
            ctx.scale(-1, 1);

            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            //Variable to stored captured image
            const imgDataUrl = canvas.toDataURL('image/png');

            // Save the captured image in localStorage
            localStorage.setItem('capturedImage', imgDataUrl);
            
            matchFound = true;

            if(matchFound){
                // Open a new window and display the captured image
                const newWindow = window.open("{% url 'display' %}", 'Captured Image');
                if (newWindow) {
                    newWindow.addEventListener('load', function () {
                        newWindow.document.getElementById('captured-image').src = imgDataUrl;
                    });
                }
            }else{
                
                const noRecordModal = document.getElementById('NoRecord');        
                const noRecord = new bootstrap.Modal(noRecordModal);
                noRecord.show();
            }
        });
    } catch (error) {
        console.error('Error accessing the webcam:', error);
    }

        // Instantiate the CheckManually modal
        checkManually = new bootstrap.Modal(document.getElementById('CheckManually'));
})();


//Search Button
const declineButton = document.getElementById('decline-button');
const searchButton = document.getElementById('search-button');

searchButton.addEventListener('click', function () {
    const cnic = document.getElementById('cnic').value.trim();
    const license_no = document.getElementById('license_no').value.trim();

    if (cnic === '' && license_no === '') {

        alert('Please enter either CNIC or License No.');

    } else {        
        
        matchFound = true;
        
        if (!matchFound) {
            if (checkManually._isShown) {
                checkManually.hide();
            }
            const noRecord = new bootstrap.Modal(document.getElementById('NoRecord'));
            noRecord.show();
        } else {
             // Open a new window and display the captured image
             const newWindow = window.open("{% url 'display' %}", 'Captured Image');
             if (newWindow) {
                 newWindow.addEventListener('load', function () {
                     newWindow.document.getElementById('captured-image').src = imgDataUrl;
                 });
                 document.getElementById('cnic').value = '';
                 document.getElementById('license_no').value = '';
                 if (checkManually._isShown) {
                    checkManually.hide();
                }
             }
        }
    }
});

//Decline Button
declineButton.addEventListener('click', function () {
    // Removing captured image from localStorage
    localStorage.removeItem('capturedImage');
});

//Logout Button
document.getElementById('logout-btn').addEventListener('click', function() {
    // Clear local storage
    localStorage.clear();
    // Redirect to the login
    window.location.href = 'login.html';
});
