from flask import Flask, render_template,jsonify,request
from PIL import Image
import PIL
import io, sys
import base64
import numpy as np
import cv2

app = Flask(__name__)

@app.route("/maskImage",methods= ["POST"])
def mask_Image():
    print('This is in image_info method!!!')
    file = request.files['canvasImage'].read()
    npimg = np.fromstring(file, np.uint8)
    img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.flip(img, 1)
    
    cv2.putText(img, 'From Backend! Hurray!!!',  (10,30),  cv2.FONT_HERSHEY_SIMPLEX,  1,  (0, 255, 0),  3)
    img = Image.fromarray(img.astype("uint8"))
    

    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    return jsonify({'status':str(img_base64)})


@app.route("/")
def photoClick():
    return render_template('photoclick.html')


@app.route('/test' , methods=['GET','POST'])
def test():
	print("log: got at test" , file=sys.stderr)

	return jsonify({'status':'succces'})


@app.after_request
def after_request(response):
    print("log: setting cors" , file = sys.stderr)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
   app.run(debug = True, port=5050)
