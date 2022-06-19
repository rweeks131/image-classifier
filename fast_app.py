#import necessary packages
from __future__ import print_function
from gluoncv.model_zoo import get_model
from mxnet import gluon, nd, image
from mxnet.gluon.data.vision import transforms
from gluoncv import utils
from PIL import Image
import shutil
import os, io
from fastapi import FastAPI, Request, File, UploadFile
import uvicorn
import subprocess

#initiate fast api as the app
app = FastAPI()

#If a get request is pushed to this app, along with no further instruction, 
#then a simple message will be the response to the request
@app.get("/")
async def root():
    return {"message": "Hello from the otherside"}

#If a post request is pushed to this app, along with the instruction of /predict, 
#then a very simple and pretrained image classifier (CNN) will be called.  
@app.post("/predict")
def predict(request:Request,file:UploadFile=File(...)):
    print("app is running...")

    #get the image pushed by the user
    with open("image.jpg","wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        image = Image.open("image.jpg")
        print("Got the image!")
         
    #the pretrained NN requires a compact version of the image, so the image
    #gets transformed into a 32x32 pixel image
    transform_fn = transforms.Compose([
        transforms.Resize(32),
        transforms.CenterCrop(32),
        transforms.ToTensor(),
        transforms.Normalize([0.4914, 0.4822, 0.4465], [0.2023, 0.1994, 0.2010])])
    img = transform_fn(nd.array(image))

    #the pretrained model is retrieved
    net = get_model('cifar_resnet110_v1', classes=10, pretrained=True)

    #predicting the object in the image with very specific class names
    pred = net(img.expand_dims(axis=0))
    class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

    #retrieving the prediction confidence
    ind = nd.argmax(pred, axis=1).astype('int')
    prediction = 'The input picture is classified as [%s], with probability %.3f.'% (class_names[ind.asscalar()], 100*(nd.softmax(pred)[0][ind].asscalar()))

    print("prediction complete.")


    return prediction
