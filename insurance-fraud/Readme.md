# RPA(UiPath) & AI : Insurance Fraud Detection Use Cases

## Description:
Insurance Fraud Detection is a sample use case that integrates RPA (UiPath) & AI in solving real world business process.  
This use case uses an open source dataset for demo purpose. The description below explains how the workflow works.  

## File Description:  
**Main.xaml:** The main entry point. This is the main workflow to execute.  

**ConfigureKonduitServing.xaml:** This is the primary workflow to initiate Konduit-serving model server.
It handle model server folder exitstance, download, process id checking and start up model serving system.    

**ReadClaimForms.xaml:** This is the primary workflow for insurance fraud detection demo, it handle forms reading, 
features extraction, data convertion and result display.  

**GetInferenceResults.xaml:** This workflow handle the interaction between RPA and Konduit-serving system. 
It generated json format POST request and sent to model server, then it wait for server to return an response in json format.
Thats response will be inference result.  

**Take Note**  
If you intend to customize the workflow by leveraging this demo, do replace "ReadClaimForms.xaml" with your respective claim forms extraction workflow. You can continue to use "GetInferenceResults.xaml" but do remember to modify the POST request input variable.
 
## Model Serving :  
Konduit-Serving is a serving system and framework focused on deploying machine learning pipelines to production.  
The strength of konduit model serving system is it able to serve wide varieties of python machine learning framework and DL4J framework. 
These framework are included Tensorflow, Keras, DL4J and etc.  
If you wish to know more about Konduit model serving, please refer to the below github page:  
**https://github.com/KonduitAI/konduit-serving**  

### To customize your own script(python):  
&nbsp;  
&nbsp;  
Similar to how you perform inference(prediction), you can write a python script to serve your model.  
&nbsp;     
&nbsp;  
&nbsp;  
### Example in Python with Tensorflow Model
![Python Script Example](img/pythonscriptexample.png "Python Script Example")  
&nbsp;  
You will notice that in the picture above consist of red boxes and green boxes. These 2 boxes contain variable that is needed by konduit model serving system in  
insurance fraud detection demo.  
&nbsp;  
&nbsp;  
**Red box:**  
- **myinput** & **model_path** is the input variable that define when serving python script.  

**Green box:**  
- **PredictedClass** , **Confidence** &  **output** is the output variable that define when serving python script.  
&nbsp;  
*********** **These variable is needed to be specified in the konduit model serving config file(.json)**   ***********  
&nbsp;  
&nbsp;  
*********** **example (in konduit model serving config file) :** ***********  
&nbsp;  
&nbsp;  
&nbsp;  
![Konduit-Serving](img/konduitserving.png "Konduit-Serving")  
&nbsp;  
While these variable already specified in the konduit model serving configuration file, when client side is performing POST request to konduit model servering system,  
konduit model serving system will find for the specific variable (input variable) in python script and pass in value to it.  
During response phase, after konduit model serving system successfully execute the serving python script, it will gather variable content (output variable) that specified  
in the model serving configuration, return in json format to the client side (POST request).  
&nbsp;    
&nbsp;    
&nbsp;    
### **Sample POST request input (json) :**   
&nbsp;  
![Client Input Sample (json format)](img/jsonPOST.png "Client Input Sample (json format)")  
&nbsp;  
&nbsp;  
### **Sample POST request output (json) :**   
&nbsp;  
![Client Output Sample (json format)](img/jsonPOSToutput.png "Client Output Sample (json format)") 
&nbsp;  
&nbsp;  
&nbsp;  
## RPA(UiPath) Workflow :  
&nbsp;  
RPA workflow for Insurance fraud detection demo is created based on synthetic generated insurance claims form as actual form is highly confidential, this demo 
will only able to use open source dataset for the workflow. By applying the similar concept of extracting variable from various type of forms (excel, web forms, 
pdf & etc.), this demo intended to proof the feasiblity of RPAxAI workflow. If any user's intended to modify this demo to fit to their own business process, 
please follow the steps below.  
&nbsp;  
&nbsp;  
### Preserve Workflow (just use it) :  
&nbsp;  
![Preserve Workflow (mandatory)](img/preserveworkflow.png "Preserve Workflow (mandatory)")  
&nbsp;  
"Initiate_Model_Server.xaml" is a mandatory workflow that needed to be initiated before any other workflow started. There are nothing much needed to be change in 
"Initiate_Model_Server.xaml" workflow. if you are using your own python script to serve, please refer above "Model Serving" steps to understand how to configure your 
own script in serving.  
&nbsp;  
### Main.xaml Workflow :  
&nbsp;  
![Main Workflow](img/mainworkflow.png "Main Worflow")  
&nbsp;  
This is the start up point of whole workflow. You can see that the very first workflow to start with always to initiate konduit model serving system.
if you intended to create your own workflow, please do keep in mind that just leverage the "Initiate_Model_Server.xaml" and always start this workflow before any subsequence
workflow.  
&nbsp;  
### Read_Claims_forms workflow.xaml Workflow :  
&nbsp;  
![Read Claims forms Workflow](img/readclaimsform.png "Read Claims forms Workflow")  
&nbsp;  
This Workflow is customize base on current available claims forms format. Please do note that this workflow is not generic workflow. You should create your own
forms reading workflow to extract out features from your own forms format (web forms, PDF, excel and etc.). In this workflow, basically the main process incharge will be 
extract data table (Get_each_value.xaml) from excel form (refer to Sample Forms image)---> map each extracted feature with pre-instant dictionary list(Transformation.xaml)--->perform normalization (Transformation.xaml) --->
append all the features in an array list---> return the array list ---> sent to model server for inference (Konduit_model_server.xaml) ---> catagorize result(Result_Manipulation.xaml).  
&nbsp;  
![Sample Forms](img/sampleform.png "Sample Forms")  
&nbsp;  
### Konduit_model_server.xaml Workflow :  
&nbsp;  
![Client Prediction Workflow](img/serverprediction.png "Client Prediction Workflow")  
&nbsp;  
This workflow can be leverage as client https POST request workflow. The main function of this workflow is to sent a POST request to Konduit moder serving system 
and get a prediction result back from the system (in json format). The changes will happen on the body of POST request and the endpoint variable (if you change your port). As you changes your script input and 
and output serving variable, you will need to change the body of POST request (refer to Sample POST request input (json)).  
&nbsp;  

# Reach us for RPAxAI workflow customization
If you encounter roadblocks in customizing your RPA & AI workflow, we strongly encourage you to reach us anytime!  

### **Webpage @ https://konduit.ai/**  
### **contact page @ https://konduit.ai/contact/**  
### **enquiry @ hello@konduit.ai**  
