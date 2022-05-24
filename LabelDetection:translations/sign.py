from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel
from google.cloud import storage, vision
from google.cloud import translate_v2 as translate
import six
import argparse
#import os

CLOUD_STORAGE_BUCKET = 'oolong3'


class Sign(MethodView):
    def get(self):
        return render_template('sign.html')

    def post(self):
        
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        #CLOUD_STORAGE_BUCKET = os.getenv('CLOUD_STORAGE_BUCKET')
        photo = request.files["filePic"]

        # Create a Cloud Storage client.
        storage_client = storage.Client()

        # Get the bucket that the file will be uploaded to.
        bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)

        # Create a new blob and upload the file's content.
        blob = bucket.blob(photo.filename)
        blob.upload_from_string(photo.read(), content_type=photo.content_type)

        # Make the blob publicly viewable.
        blob.make_public()
        

        # Create a Cloud Vision client.
        vision_client = vision.ImageAnnotatorClient()

        # Put image in Bucket so we can access it for face Detection/explicit content
        source_uri = "gs://{}/{}".format(CLOUD_STORAGE_BUCKET, blob.name)
        image = vision.Image(source=vision.ImageSource(gcs_image_uri=source_uri))


        # Detect an object in our image
        response = vision_client.label_detection(image=image)
        labels = response.label_annotations

        # If a label is detected, save to Datastore
        # as determined by Google's Machine Learning algorithm.
        if labels[0] is not None:
            label1 = labels[0]
            text1 = label1.description
        if labels[1] is not None:
            label2 = labels[1]
            text2 = label2.description
        if labels[2] is not None:
            label3 = labels[2]
            text3 = label3.description
        if labels[3] is not None:
            label4 = labels[3]
            text4 = label4.description
        if  labels[4] is not None:
            label5 = labels[4]
            text5 = label5.description

   
        # Fill Datastore with labels of our image
        if labels[0] is not None:
            labels1= label1.description
        if labels[1] is not None:
            labels2= label2.description
        if labels[2] is not None:
            labels3= label3.description
        if labels[3] is not None:
            labels4= label4.description
        if labels[4] is not None:
            labels5= label5.description
    
        # Translate Language of labels to Afrikaans
        translate_client = translate.Client()

        # Set up our text so it can be translated
        if isinstance(text1, six.binary_type):
            text1 = text1.decode("utf-8")
        if isinstance(text2, six.binary_type):
            text2 = text2.decode("utf-8")
        if isinstance(text3, six.binary_type):
            text3 = text3.decode("utf-8")
        if isinstance(text4, six.binary_type):
            text4 = text4.decode("utf-8")
        if isinstance(text5, six.binary_type):
            text5 = text5.decode("utf-8")
    
        # Store different translated text in results
        result1 = translate_client.translate(text1,target_language='af')
        result2 = translate_client.translate(text2,target_language='zh-TW')
        result3 = translate_client.translate(text3,target_language='hi')
        result4 = translate_client.translate(text4,target_language='fr')
        result5 = translate_client.translate(text5,target_language='es')

  
        # Fill different translations by languge(
        # Afrikaans, Chinese (Traditional), Hindi, French, Spanish) into Datastore 
        translated1= result1["translatedText"]
        translated2= result2["translatedText"]
        translated3= result3["translatedText"]
        translated4= result4["translatedText"]
        translated5= result5["translatedText"]
        
        image_public_url = blob.public_url

        model = gbmodel.get_model()
        model.insert(labels1,labels2,labels3,labels4,labels5,translated1,translated2,translated3,translated4,translated5,image_public_url )
        return redirect(url_for('index'))
