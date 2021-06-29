# Auth0 Python Web App Sample

This sample demonstrates how to add authentication to a Python Flask web app using Auth0.

# Running the App

This application is configured to run on a Ubuntu EC2 instance on AWS.

## Step 1: Deploy an EC2 instance

1. From the AWS EC2 console select `Launch Instance`
2. Select the Ubuntu 20.04 LTS instance family (type 'ubuntu' in the search field)
3. Select the t2.micro instance family
4. Select the proper VPC, Subnet and EC2 instance profile as necessary
5. Under 'Advanced Details', copy and paste the `userdata.sh` file found here in the `bootstrap` path
6. Add storage (minimum 8GB for Ubuntu) 
7. Add necessary tags
8. Select an existing security group, or create a new one using the wizard.  Ensure that ports 80 and 22 are open to your local IP address
9. Click "Review and Launch" and select your SSH keypair

When the deployment completes, make note of the IPv4 Public DNS name.

## Step 2: Create your Auth0 Application

(from the Auth0 Console)

Login to your Auth0 account and create a new application or use the default application that was created when you created your Auth0 account.

Configure your callback and logout URLs:

* The list of Callback URLs should contain `http://${EC2_IPv4_DNS_HERE}/callback`
* The list of Logout URLs should contain `http://${EC2_IPv4_DNS_HERE}/`

## Step 3: Configure App Constants

(from the EC2 command line)

SSH into your EC2 instance and edit the file `constants.py` with the following values:

Copy `.env.example` to `.env` and replace the placeholders with the correct values.  Callback URLs should reference your EC2 instance's Public IPv4 DNS address and not `localhost`.  **_Emphasis: this method of secrets injection is not secure and should not be implemented within a production environment.  Instead secrets should be managed by a bonafide secrets management utility_**

```
AUTH0_CLIENT_ID = '[Auth0 client ID goes here]'
AUTH0_CLIENT_SECRET = '[Auth0 client secret goes here'
AUTH0_CALLBACK_URL = 'http://[EC2_IPv4_DNS_HERE]/callback'
AUTH0_DOMAIN = '[Auth0 domain goes here]'
AUTH0_AUDIENCE = 'https://[AUTH0_DOMAIN_HERE]/api/v2/'
```

## Step 3: Configure NGINX and Gunicorn

(from the EC2 command line)

SSH into your EC2 instance

1. This Git repo should already be checked out in the directory `/home/ubuntu/app`
2. navigate to the `config` path and execute the script `config.sh`.  This will place both the nginx and gunicorn config files in the correct paths as well as start the application

```
cd app/config
sudo ./config.sh
```

## Usage Instructions

1. Once the application has been configured, hit the IPv4 Public DNS name of your EC2 instance.  This will present a default screen with a simple 'Login' button.
2. Click login and select 'Sign in with Google' or 'Sign Up'
    1. Sign Up: provide your email address and password.  This will generate an email validation request (sent to the email address used to sign up), and it will create a new user in your Auth0 application
    2. Sign up with Google: This will request your Google username and password and will also create a new user in your Auth0 application.
    3. Linked accounts: If the user signs in using thier email address and then later chooses 'Sign in with Google' (or visa versa), the [Auth0 account link extension](https://auth0.com/docs/extensions/account-link-extension) can be configured automatically detect a duplicate user and provide the user with the option to link both accounts.  If the user agrees, they will be prompted for the authentication information of the second account, and the accounts will be linked together presenting a single user within your Auth0 application.
3. Email verification: this application demonstrates how to detect if a user has verified their email address.  If the user has not validated thier email, then basic information is witheld from that user.  Once the user has verified, that information is shown.
4. Logout: Click the 'Logout' button to lot out

This application also uses an Auth0 Rule to detect users' country of origin as well as regional information.  See:

* [Auth0 Add Country Rule](auth0/)
* https://auth0.com/rules/add-country

