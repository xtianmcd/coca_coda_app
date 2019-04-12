from flask import render_template, jsonify, Response, request
from app import app
import random
from camera import VideoCamera
from tensorflow import keras
from app import app
import random
import os
from keras.applications.mobilenetv2 import MobileNetV2
from keras.preprocessing import image
from keras.applications.mobilenetv2 import preprocess_input, decode_predictions
import numpy as np


app.config['UPLOAD_FOLDER'] = '/Users/xtian/Documents/GitHub/coca_coda_app/app/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/upload')
def upload_file2():
    return render_template('index.html')

@app.route('/uploaded', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files["file"]
        path = os.path.join(app.config['UPLOAD_FOLDER'],f.filename)
        base_model = tf.keras.applications.MobileNetV2(input_shape=(224,224,3),
                                                    include_top=False,
                                                    weights='imagenet')
        top = tf.keras.Sequential([tf.keras.layers.GlobalAveragePooling2D(),
                                    tf.keras.layers.Dense(1,activation='sigmoid')
                                    ])
        top.set_weights('my_model_weights.h5')
        model = tf.keras.Sequential([base_model,top])
        img = image.load_img(path, target_size=(224,224))
        x = image.img_to_array(img)
        x = np.expand_dims(x,axis=0)
        x = preprocess_input(x)
        preds = model.predict(img)
        # preds_decoded = decode_predictions(preds, top=3)[0]
        # print(preds_decoded)
        f.save(path)
        return render_template('index.html', title='Success',predictions=preds, user_image=f.filename)

@app.route('/index')
def index():
    return render_template('index.html', title='Inference Generator')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    #     # check if the post request has the file part
    #     if 'file' not in request.files:
    #         flash('No file part')
    #         return redirect(request.url)
    #     file = request.files['file']
    #     # if user does not select file, browser also
    #     # submit an empty part without filename
    #     if file.filename == '':
    #         flash('No selected file')
    #         return redirect(request.url)
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         return redirect(url_for('uploaded_file',
    #                                 filename=filename))
    # return render_template('index.html', title='Inference Generator')



# @app.route('/uploaded', methods = ['GET','POST'])
# def upload_file():
#     if request.method=='POST':
#         f = request.files['file']
#         path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
#         #model = ##model weights##
#         # img = image.load_img(f.filename)
#         #preds = ##run inference##
#         f.save(path)
#         return render_template('uploaded.html', title='Success')#,predictions=preds_decoded, user_image=f.filename)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/capture', methods=['GET','POST'])
def capture():
    if request.method == 'POST':
        return jsonify(request.form['file'])
    return render_template('capture.html', title='Upload a New Photo')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/record_status', methods=['POST'])
# def record_status():
#     global video_camera
#     if video_camera == None:
#         video_camera = VideoCamera()
#
#     json = request.get_json()
#
#     status = json['status']
#
#     if status == "true":
#         video_camera.start_record()
#         return jsonify(result="started")
#     else:
#         video_camera.stop_record()
#         return jsonify(result="stopped")
#
# def video_stream():
#     global video_camera
#     global global_frame
#
#     if video_camera == None:
#         video_camera = VideoCamera()
#
#     while True:
#         frame = video_camera.get_frame()
#
#         if frame != None:
#             global_frame = frame
#             yield (b'--frame\r\n'
#                     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#         else:
#             yield (b'--frame\r\n'
#                             b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')
#
# @app.route('/video_viewer')
# def video_viewer():
#     return Response(video_stream(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/capture')
# def video_feed():
#     return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')
