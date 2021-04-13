# DF-Chatbot

## Introduction 
In the following, we explain the required steps in order to configure DF-Chatbot and then interact with it. All these steps are demonstrated in this [video](https://drive.google.com/file/d/1_dwLW0SgkQHw-pU6RHTVlWK1JT-MCZIT/view?usp=sharing).
## How to configure DF-Chatbot? 
1. Go to [DialogFlow CX console](https://dialogflow.cloud.google.com/cx/projects) and connect to the console with your gmail
2. Create a new google cloud project and enable DialogFlow API.
3. Create a new empty agent.
4. Download Study_Agent.blob file in this github project. The Study_Agent.blob file contains necessary intents, training phrases, and entities for this user study.
5. Go to "View all agents" in the current project and restore Study_Agent.
6. To have access to the webhook service for this study, create a new webhook "my_webhook_service" and use this URL [https://webhook-workshop.herokuapp.com/my_webhook](https://webhook-workshop.herokuapp.com/my_webhook). In the next section, we will show you how to deploy this webhook_service on heroku, it will allow you to use your own URL and modify the source code.
7. Congratulations! you just finish the configuration of the chatbot. Let's do a test.

## Test your DF-Chatbot
1. Click on "Start" page and create a new Route:
   - Intent: GetWeather
   - Tranistion: New Page "Get Weather"
2. Click on "Get Weather" page and create a new parameter:
   - Parameter name: location
   - Entity type: @sys.geo-city
   - Check "Required"
   - Fulfillement (Agent says): What is the location?
3. Click on "Get Weather" page and create a new Route:
   - Condition: $page.params.status="FINAL" (meaning all required parameters are fulfilled)
   - Check "Use Webhook"
   - Select "my_webhook_service"
   - Tag: GetWeather_fulfillment
4. Click on "Test Agent" and ask the agent for the weather in a city. The agent will give you the weather forecast in the given city.
5. Congratulations! You can now start the user study using this agent.

## Deploy your own webhook_service
If you want/need to change the webhook_service source code you will need to deploy your own webhook_service. In the following, we explain the required steps to deploy the webhook_service on heroku:
1. Create a Heroku account on [https://signup.heroku.com/login](https://signup.heroku.com/login)
2. Download webhook_service folder in this github project.
3. Open a terminal and execute the following commands:
```
cd webhook_service
pipenv shell
git init 
git add .
heroku login
heroku create your_app_name %Create a unique name for your Web app
git commit -m "initial commit"
git push heroku master
```
4. On DialogFlow CX go to webhooks and change the previous URL ([https://webhook-workshop.herokuapp.com/my_webhook](https://webhook-workshop.herokuapp.com/my_webhook)) by your new URL (some thing like [https://your_app_name.herokuapp.com/my_webhook](https://your_app_name.herokuapp.com/my_webhook)).
5. Click on "Test Agent" and ask the agent for the weather in a city. The agent will give you the weather forecast in the given city.


## Modify webhook_service source code
Once you finished to deploy your  own webhook_service on heroku, you can modify the webhook_service code source as following:
1. There are three file inside webhook_service/app:
- **main.py**: this file contains two functions: 
  * **post_webhook_dialogflow()**: this function get the session_id, fulfillment (target intent), and parameters (slots) from DialogFlow. Itn calls **invoke_api** a function defined in **api_manager.py** file to get an answer and returns this answer in json format.
  * **answer_webhook()**: to return the answer in json format.
- **API_credentials.json**: To fulfill some intents, the chatbot invokes specific APIs, namely [here](https://developer.here.com/); [openweathermap](https://openweathermap.org/api); [Yelp](https://www.yelp.com/developers/documentation/v3). We put our own credential information but you can get your own credential information and put them in this file. Getting credential information requires creating accounts in these APIs.
- **api_manager.py**: the **invoke_api** function in this file returns a string (the answer) depending on a given fulfillment. For example if the fulfillment is *GetWeather_fulfillment* we call *OpenWeatherMap* API using the **API_crendentials** (*getAPI_credential('api.openweathermap','appid')*) and using the given parameters values (*slots_values_list*). The **invoke_api** function returns a dynamic answer (*reply = "There is {} in there.".format(weatherCondition)*).
2. Let's modify the code by changing *reply = "There is {} in there.".format(weatherCondition)* to *reply = "There is {} in there. Have a good day :)".format(weatherCondition)* in the **api_manager.py** file
3. Open a terminal and execute the following commands:
```
cd webhook_service
git init 
git add .
git commit -m "make it better"
git push heroku master
```
4. On DialogFlow CX, click on "Test Agent" and ask the agent for the weather in a city. The agent will give you the weather forecast in the given city by answering *There is {something} in there. Have a good day :)*
5. You can now modify the source code and deploy your own webhook_service. Don't forget to execute commands in step 3 to apply the updates. You can also use the following command to show logs:
```
heroku logs --tail --app your_app_name
```





