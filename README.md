# image-classifier

This was my first project that involved locally serving a ML algorithm via uvicorn, containerizing a ML program, and serving the program via minikube. The original project (by Chaimaa Zyani) was developed to utilize flask; however, I redesigned the project to function with fastAPI due to minikube being able to work with fastAPI better than flask. In this project the ML algorithm is containerized via docker and served via minikube. The ML algorithm is a deep learning NN that is used for image prediction. The model is pretrained using the CIFAR-10 image dataset. You can find more info about this ML algorithm here: https://cv.gluon.ai/build/examples_classification/demo_cifar10.html .

To use this project's programs, import all files in this repository into any directory on your local machine. To run the program locally, use:
> uvicorn fast_app:app

The server should then be connected to your localhost using port 8000. Check that it is working by using-> localhost:8000 , in any browser.

(Using Postman) To make a prediction based on an image you have (your image MUST be a .jpg and must be renamed 'image.jpg'), use the following-> localhost:8000/predict , in the url and make sure the image is attached in the body of a 'POST' request. (Note that the original request was using the GET method, while the prediction request uses the POST method). 


To containerize the model make sure docker is running on your machine. Now use the following commands in the same directory that you put the files:
> docker build -t fast_app .

> docker run -p 5000:100 fast_app

check that the container is working by using-> localhost:5000 , in any browser. 


[USING THE POD.YAML AND NODEPORTSERVICE.YAML FILES (delete the deployment.yaml,ingress.yaml and imclass-cluster-ip-service.yaml files)]

To serve the container via minikube, use the following:
> minikube start

> kubectl apply -f pod.yaml

> kubectl apply -f nodeportservice.yaml

and check to make sure both the pod and service are working properly by exposing both to localhost. To expose the pod, use:
> kubectl port-forward kube-pod 5000:100

To test if the pod was exposed properly, use-> localhost:5000 , in any browser. To expose the node-port-service use:
> kubectl port-forward service/kube-node-port 5000:100

To test if the node service was exposed properly use-> localhost:5000 , in any browser.


[USING THE DEPLOYMENT.YAML,INGRESS.YAML, AND IMCLASS-CLUSTER-IP-SERVICE.YAML FILES (delete the nodeportservice.yaml and pod.yaml files)]

To serve the container via minikube, use the following:
> minikube start

>kubectl apply -f image-classifier

>minikube addons enable ingress 

>minikube tunnel

and check that the port to the program is exposed by using -> localhost , in any browswer.

This Kubernetes cluster has not been deployed to any cloud service, but I plan to work on deploying the cluster in the near future.


