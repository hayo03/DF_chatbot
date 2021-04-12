# DF_chatbot

## Introduction 
In the following, we explain the required steps in order to configure DF-Chatbot and then interact with it. All these steps are demonstrated in this [video](https://drive.google.com/file/d/1_dwLW0SgkQHw-pU6RHTVlWK1JT-MCZIT/view?usp=sharing).
## How to configure Df-Chatbot? 
1. Go to [DialogFlow CX console](https://dialogflow.cloud.google.com/cx/projects)
2. Create a new google cloud project and enable DialogFlow API.
3. Create a new empty agent.
4. Download Study_Agent.blob file in this github project. The Study_Agent.blob file contains necessary intents, training phrases, and entities for this user study.
5. Go to "View all agents" in the current project and restore Study_Agent.
6. To have access to the webhook service for this study, create a new webhook "my_webhook_service" and use this URL [https://webhook-workshop.herokuapp.com/my_webhook](https://webhook-workshop.herokuapp.com/my_webhook). In the next section, we will show you how to deploy this webhook_service on heroku, it will allow you to use your own URL and update the code.
7. Congratulations! you just finish the configuration of the chatbot. Let's do a test.

## Test your Df-Chatbot
1. Click on "Start" page and create a new Route:
- Intent: GetWeather
- Tranistion: New Page "Get Weather"
3. Click on "Get Weather" page and create a new parameter:
- Parameter name: location
- Entity type: @sys.geo-city
- Check "Required"
- Fulfillement (Agent says): What is the location?
4. Click on "Get Weather" page and create a new Route:
- Condition: $page.params.status="FINAL"
- Check "Use Webhook"
- Select "my_webhook_service"
- Tag: GetWeather_fulfillment
5. Click on "Test Agent" and ask the agent for the weather in a city. The agent will give you the weather forecast in the given city.
6. Congratulations! You can now start the user study using this agent.

## How to deploy my own webhook_service
If you want/need to change the webhook_service code source you will need to deploy your own webhook_service. In the following, we explain the required steps to deploy the webhook_service on heroku:
1. Download webhook_service folder in this github project. This folder contains ...
2. 







