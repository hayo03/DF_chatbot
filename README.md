# DF_chatbot

## Introduction 
In the following, we explain the required step in order to configure DF-Chatbot and then interact with it. All these steps are demonstrated in this [video](https://drive.google.com/file/d/1_dwLW0SgkQHw-pU6RHTVlWK1JT-MCZIT/view?usp=sharing).
## How to configure Df-Chatbot? 
1. Download the source code in this github project. The source code includes the following files:

  *Study_Agent.zip
  
  *Chatbot folder
  
2. Create a new empty agent using  [DF console](https://dialogflow.cloud.google.com/)

3. Go to "Export and Import" option in the agent setting

4. Click on RESTORE FROM ZIP and select the downloaded file Study_Agent.zip
5. To fulfill some intents, the chatbot invokes specific APIs, namely [here](https://developer.here.com/); [openweathermap](https://openweathermap.org/api); [Yelp](https://www.yelp.com/developers/documentation/v3). To use these APIs you need to get credential information mentioned in API_credentials.json file in the chatbot folder and complete them. Getting credential information requires creating accounts in these APIs.

6. Once you get the required credentials and complete API_credentials.json file, open terminal, create a virtual environment and install required packages
```
cd Main 
bash run.sh
```
Open new terminal to run ngrok server

```

ngrok http 8081 (or ./ngrok http 8081 if the first one does not work) 
```
if you don't have ngrok configured in your laptop, just Download it from [ngrok](https://ngrok.com/download), unzip it, and in the terminal just run (cd Pathtounzipedfolder)  and then run (ngrok http 8081).

6. Copy the HTTPS URL (some thing like https://25e5bc5277ea.ngrok.io) and go back to the created agent, click on "Fulfillment" option, enable "Webhook" option and paste the URL in URL* filed and add "/my_webhook" at the end of URL 

7.If it is not enabled by default, enable the "log interactions to dialogflow" option in the agent setting

8. Share your agent in dialogflow with us by entreing our emails (brabra.hayeet@gmail.com/ bougueliasara@gmail.com) in the "Share" option (it is in the agent setting) and add us Reviewer

9. Congratulations !!! you just finish the configuration of your chatbot.

## How to interact with Chatbot1?  

1. Open the demo web interface provided by Dialogflow by clicking first on "Integrations" option and then on the "Web Demo" option

2. Start chatting with the chatbot

## What you should send us?
No there is no need to send as a particular file just be sure you have already shared your agent in Dialogflow with us (Instruction 8)!!!!

## Any problem
Please contact us at brabra.hayeet@gmail.com/ bougueliasara@gmail.com
