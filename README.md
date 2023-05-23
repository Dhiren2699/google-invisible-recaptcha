## Implement Google Invisible ReCaptcha

Html page contains a single form that verifies google invisible captcha and triggers external API.
The External API is connected to API Gateway -> Lambda -> verifies the Google Captcha and then pushes the form element of HTML page in DynamoDB.

## Technologies used

* JS, HTML5
* AWS Lambda
* AWS DynamoDB

## How to use

* Make a google recaptcha account, add domain and generate captcha secret keys.
* Replace the site key in the html form.
* Replace the other secret key in AWS Lambda.