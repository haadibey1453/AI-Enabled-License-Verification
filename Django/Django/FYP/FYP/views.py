import base64
from datetime import datetime
import os
import time
from urllib.parse import urljoin
import cv2
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
from django.shortcuts import redirect, render
from django.http import StreamingHttpResponse
from django.http import FileResponse
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from models.login import Login
from models.driver_license_info import DriverLicenseInfo
from django.template.loader import render_to_string


api_response={}

output_folder = 'D:/Django/FYP/media'

output_image_access = 'D:/Django/FYP/media/input_image.jpg'

popBox = False
no_record_found = False
violation_found = False
video_capture = None
error_message = ""
found = False
image_boundary = False

#create output folder if it does't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def LoginPage(Request):
    error_message = None
    if Request.method == 'POST':
        username = Request.POST['username']
        password = Request.POST['password']

        user_check = Login.objects.filter(username=username, password=password)
        if user_check:
            Request.session['user'] = username
            return redirect('home')
        else:
            error_message = "Incorrect username or password"
    return render(Request, "login.html", {'error_message': error_message})

def logout(request):
    try:
        del request.session['user']
    except:
        return redirect('login')
    return redirect('login')


def Home(request):
    if 'user' in request.session:
        current_user = request.session['user']
        request.session['image_boundary'] = image_boundary
        user_data = {'current_user': current_user}
        # print(request.session['image_boundary'])
        return render(request, 'home.html', user_data)
    else:
        return redirect('login')


# Drawing Boundary around face
def detect_bounding_box(vid, request): 
    global frame_path, found
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))

    frame_path = os.path.join(output_folder, f'input_image.jpg')
    #corrected_image = cv2.flip(vid, 1)
    cv2.imwrite(img=vid, filename=frame_path)
    
    if len(faces) > 1:
        minx, miny, minw, minh = faces[0]
        for (x, y, w, h) in faces:
            if (minx+minw)>(x+w):
                minx = x
                minw = w
        for (x, y, w, h) in faces:
            if(x == minx):
                cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
        request.session['image_boundary'] = True
        return vid, True
    else: 
        for (x, y, w, h) in faces:
            cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
        # request.session['image_boundary'] = True
        return vid, True


# Face detection function
def video_stream(request):
    video_capture = cv2.VideoCapture(0)
    # request.session['image_boundary'] = False
    boundary_passed = False
    def generate():
        nonlocal boundary_passed
        while True:
            result, video_frame = video_capture.read()
            if not result:
                break
            # Flip the video frame horizontally
            video_frame = cv2.flip(video_frame, 1)
            video_frame, boundary_passed = detect_bounding_box(video_frame, request)
            _, jpeg = cv2.imencode('.jpg', video_frame)

            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            # if boundary_passed:
                # # cv2.destroyAllWindows()
                # print("CV destroy")
                # # # Render JavaScript code for redirecting
                # # redirect_script = render_to_string('redirect_script.js', {'redirect_url': reverse('display')})
                # # yield redirect_script.encode('utf-8')
                # cv2.destroyAllWindows()
                # print("CV destroy")
                # return redirect('display.html')
                

    # if request.session.get('image_boundary', False):
    #     cv2.destroyAllWindows()
    #     print("CV destroy")
    #     return render(request, 'display.html')
    
    # print(request.session['image_boundary'], "3")
    # if boundary_passed:
    #     return render(request, 'display.html')
    
    #         if boundary_passed:
    #             # request.session['image_boundary'] = True
    #             print(request.session['image_boundary'], "1")
    #             cv2.destroyAllWindows()
    #             print("CV destroy")
    #             # yield render(request, 'display.html')
    #             break
                
    # if boundary_passed:
    #     cv2.destroyAllWindows()
    #     print("CV destroy")
    #     return render(request, 'display.html')
    # print(request.session['image_boundary'], "3")
    
    response = FileResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')
    return response

def video_feed(request):
    return StreamingHttpResponse(video_stream(request), content_type='multipart/x-mixed-replace; boundary=frame')

def loading(request):
    calling_api_function = True
    return render(request, 'loading.html', {'call_func': calling_api_function})

def license_check():
    url = 'http://127.0.0.1:5000/process_image'
    print("API CALL")
    global api_response, no_record_found, violation_found, popBox, error_message
    try:
        files = {'image': open(output_image_access, 'rb')}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            api_response = response.json()
            #Assuming api_response is your JSON response
            image_path = api_response['image']

            # Replace the local file path with the XAMPP local host URL
            xamp_url = 'http://localhost/'

            # Assuming the path starts with C:\xampp\htdocs\
            if image_path.startswith('C:\\xampp\\htdocs\\'):
                relative_path = image_path.replace('C:\\xampp\\htdocs\\', '')
                url = xamp_url + relative_path.replace('\\', '/')
                #print(url)
                api_response['image'] = url
            else:
                print("The image path doesn't start with C:\\xampp\\htdocs\\")
            no_record_found = False
        elif response.status_code == 404:
            print("No previous record found.")
            no_record_found = True
            time.sleep(1)
            #open pop up with No record Found text (checking previous record)
            test_get_previous_record_api()
        else:
            #Error on Response
            print("Error:", response.text)
            popBox = True
            error_message = "Error occured during Response"
            no_record_found = True 
    except requests.exceptions.RequestException as e:
        print("Error occurred during API call:", e)
        popBox = True
        error_message = "Error occurred during API call"
        no_record_found = True 

def test_get_previous_record_api():
    api_url = 'http://127.0.0.1:5000/get_previous_record'
    print("API call for previous record")
    global api_response, violation_found, no_record_found, popBox,error_message
    try:
        api_response = requests.get(api_url)
        if api_response.status_code == 200:
            print("API call successful")
            api_response = api_response.json()
            #print(api_response)
            for violation in api_response['violation_data']:
                #Assuming api_response is your JSON response
                image_path = violation['path']

                # Replace the local file path with the XAMPP local host URL
                xamp_url = 'http://localhost/'

                # Assuming the path starts with C:\xampp\htdocs\
                if image_path.startswith('C:/xampp/htdocs/'):
                    relative_path = image_path.replace('C:/xampp/htdocs/', '')
                    url = xamp_url + relative_path
                    #print(url)
                    violation['path'] = url
                else:
                    print("The image path doesn't start with C:\\xampp\\htdocs\\")
            violation_found = True
            popBox = False
        elif api_response.status_code == 404:
            #No Previous Record Found
            popBox = True
            print("popBox is set to True")
        else:
            #Error in api_response
            popBox = True
            error_message = "Error occured during Reponse"
            no_record_found = True 
    except requests.exceptions.RequestException as e:
        print("Error occurred during API call:", e)
        popBox = True
        error_message = "Error occurred during API call"
        no_record_found = True 

def Display(request):
    global no_record_found, violation_found, api_response, popBox, error_message
    license_check()
        
    context = {
        'response': api_response,
        'no_record_found': no_record_found,
        'popBox': popBox, 
        'error': error_message,
    }
    print(context)
    return render(request, "display.html", context)

def search_records(request):

    if request.method == "POST":
        cnic = request.POST['cnic']
        license_no = request.POST['license_no']

        if cnic:
            results = DriverLicenseInfo.objects.filter(cnic=cnic)
    
        elif license_no:
            results = DriverLicenseInfo.objects.filter(license_no=license_no)

        else:
            results=[]
        for result in results:
            # Construct the URL by joining the base URL with the relative file path
            result.image = urljoin("http://localhost/", result.image.replace("C:\\xampp\\htdocs\\", ""))
        print(results)
        if results:
            return render(request, 'display.html', {'search_results': results, 'no_record_found': False})
        else:
            return render(request, 'display.html', {'search_results': results, 'no_record_found': True, 'popBox': True})
