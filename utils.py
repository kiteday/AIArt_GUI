import cv2
import requests
import os

from io import BytesIO
from PIL import Image,ImageTk
# import Image
from datetime import datetime
import logging

_img = None
_name = None
_email = None

def get_cap():
    return cv2.VideoCapture(0)

# Define function to show frame
def show_frames(cap, label):
    global _img

    ret, _img = cap.read()

    if ret:
        # Get the latest frame and convert into Image
        cv2image = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)
        cv2image = cv2.resize(cv2image, (480, 360))

        img = Image.fromarray(cv2image)
        # Convert image to PhotoImage
        imgtk = ImageTk.PhotoImage(image = img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        # Repeat after an interval to capture continiously
        label.after(33, show_frames, cap, label)

def capture(win, cap, label):
    global _img

    cv2.imwrite("tmp.png", _img)

    name, email = get_name_email()
    now = datetime.now()

    _path = f"{name}__{email}.png"
    path = os.path.join("photo", _path)
    cv2.imwrite(path, _img)

    cv2image = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)
    cv2image = cv2.resize(cv2image, (480, 360))

    img = Image.fromarray(cv2image)

    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image=img, master=win)
    label.imgtk = imgtk
    label.config(image=imgtk)

def http_request(url, data=None, headers=None, file=None, num_of_seconds_to_wait=3):
    try:
        res = requests.post(   url,
                               verify=False,
                               data=data,
                               files=file,
                               headers=headers,
                               timeout=15
                               )
        if res.status_code not in (200, 204, 202):
            if random_num_of_seconds <= 50:
            # 50초가 넘어가면 멈춘다.
                random_num_of_seconds = random.randint(num_of_seconds_to_wait, num_of_seconds_to_wait + 3)
                time.sleep(random_num_of_seconds)
                return http_request(method, url, data, headers=headers, num_of_seconds_to_wait=num_of_seconds_to_wait + 3)
            else:
            	raise Exception(f'Your request failed with the following error: {res.status_code}')
    except Exception as e:
        logging.warning(f'Http request failed with url={url}\tdata={data}')
        logging.warning(e)
        raise e
    return res

def session_get(url):
    rs = requests.session()
    rs.mount('http://', requests.adapters.HTTPAdapter(pool_connections=3, pool_maxsize=10, max_retries=3))
    rs.mount('https://', requests.adapters.HTTPAdapter(pool_connections=3, pool_maxsize=10, max_retries=3))
    rs.headers = {'Content-Type': 'application/json'}
    response = rs.get(url)
    print(response.text)

def request_portrait(win, label):
    url = "http://117.16.43.105:8000/uploadfile/"
    # url = 'http://127.0.0.0:8000/uploadfile/'
    file = "tmp.png"

    # session_get(url)
    r = requests.post(url, files={"file": open(file, 'rb')})

    # http_request(url, file={"file": open(file, 'rb')})

    img = Image.open(BytesIO(r.content))
    imgtk = ImageTk.PhotoImage(image=img, master=win)
    label.imgtk = imgtk
    label.config(image=imgtk)

    name, email = get_name_email()

    now = datetime.now()
    f = open('portraits/info.txt', 'a')
    f.write(f'{name}, {email}, {now.time()} \n')
    
    with open(os.path.join("portraits", f"{name}__{email}.png"), "wb") as f:
        f.write(r.content)

def set_name_email(name, email, name_label, email_label):
    global _name, _email

    _name = name
    _email = email

    if _name :
        name_label.configure(text=f"name\t{_name}")
        email_label.configure(text=f"email\t{_email}")
        name_label.pack(side="bottom")
        email_label.pack(side="bottom")

    print(_name, _email)

def get_name_email():
    global _name, _email
    return _name, _email
    


    