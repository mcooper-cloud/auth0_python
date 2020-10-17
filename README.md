# Auth0 Python Web App Sample

This sample demonstrates how to add authentication to a Python Flask web app using Auth0.

# Running the App

This application is configured to run on a Ubuntu EC2 instance on AWS.

## Step 1: Deploy an EC2 instance

1. From the AWS EC2 console select `Launch Instance`
2. Select the Ubuntu 18.04 LTS instance family (type 'ubuntu' in the search field)
3. Select the t2.micro instance family
4. Select the proper VPC, Subnet and EC2 instance profile as necessary
5. Under 'Advanced Details', copy and paste the `userdata.sh` file found here in the `bootstrap` path
6. Add storage (minimum 8GB for Ubuntu) 
7. Add necessary tags
8. Select an existing security group, or create a new one using the wizard.  Ensure that ports 80 and 22 are open to your local IP address
9. Click "Review and Launch" and select your SSH keypair

## Step 2: Configure NGINX and Gunicorn

1. Login to the newly created instance (this Git repo should already be checked out in the directory `/home/ubuntu`)
2. Edit constants.py and replace the placeholders with the correct values.  Callback URLs should reference your EC2 instance's Public IPv4 DNS address and not `localhost`.  **__Emphasis: this method of secrets injection is not secure and should not be implemented within a production environment.  Instead secrets should be managed by a bonafide secrets management utility __**
3. navigate to the `config` path and execute the script `config.sh`.  This will place both the nginx and gunicorn config files in the correct paths as well as start the application

```
cd config
./config.sh
```
