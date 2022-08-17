import cozmo
import time
import _thread
from cozmo.util import degrees
from pytesseract import pytesseract


    
    
def cozmo_image_extraction(robot: cozmo.robot.Robot):
    
    def input_thread(L):
        input()
        L.append(None)

    def process_image(image_name):
        image = cv2.imread(image_name)
        
        img = cv2.resize(image, (600, 600))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        denoise = cv2.fastNlMeansDenoising(blur)
        thresh = cv2.adaptiveThreshold(denoise, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        blur1 = cv2.GaussianBlur(thresh, (5, 5), 0)
        dst = cv2.GaussianBlur(blur1, (5, 5), 0)
        
        cv2.imwrite('processed_image.png', dst)

    def tesseract():
        path_to_tesseract = r"/usr/local/Cellar/tesseract/5.2.0/bin/tesseract"
        image_path = "processed_image.png"
        pytesseract.tesseract_cmd = path_to_tesseract
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
   
    pic_filename = "Cozmo_Captured_Image.png"
    
    robot.camera.image_stream_enabled = True
    
    robot.camera.color_image_enabled = False
    L = []   
    _thread.start_new_thread(input_thread, (L,))
    robot.set_head_angle(degrees(20.0)).wait_for_completed()
    while True:
        if L:    
            # récupération de l'image caméra
            latest_image = robot.world.latest_image.raw_image
            latest_image.convert('L').save(pic_filename)
            robot.say_text("Picture").wait_for_completed()
            
            process_image(pic_filename)
    
            text = tesseract()
            robot.say_text(text, use_cozmo_voice=True, duration_scalar=0.5).wait_for_completed()
            break

    print("Image Capture Completed Successfully..")
    time.sleep(5)

cozmo.robot.Robot.drive_off_charger_on_connect = False

#Cozmo Activation Method 
cozmo.run_program(cozmo_image_extraction)
