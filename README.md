# Brine-task
 task to deploy a Python application with Docker, AWS ECR, ECS, and CodePipeline.

Prepare your environment
STEP 1 - Install AWS CLI and Docker
Install AWS CLI and Docker on your local machine. Make sure to configure AWS CLI with your AWS credentials.

Create a repository in Amazon ECR (Elastic Container Registry):

aws ecr create-repository --repository-name my-repo


STEP 2 - 
Build your Docker image and push it to ECR

First, create a Dockerfile in the root of your project:

This Dockerfile starts with a Python 3.10 image, sets the working directory to /app, copies the current directory into the container, installs any requirements, and then runs main.py.

Then, build your Docker image:
docker build -t my-python-app .

docker run -it --rm --name my-running-app my-python-app

You can also run your test cases in a similar way, but with the command to run your tests in the Dockerfile, like so:

Now build the docker image for test cases -
docker build -t testcases .

docker run -it --rm --name my-running-tests testcases

Alternatively, you could use docker-compose to simplify the running of your application and tests. For this, you'd need to create a docker-compose.yml file:

version: '3'
services:
  app:
    build: .
    command: python main.py
  test:
    build: .
    command: python -m unittest main.py

=================================================
now run the app and test cases using the following command -
docker-compose up app
docker-compose up test

==============================================================
now to build  build the image and push it to ECR:

$(aws ecr get-login --no-include-email --region region-name)  # log in to ECR

docker build -t my-repo .

docker tag my-repo:latest 123456789012.dkr.ecr.region-name.amazonaws.com/my-repo:latest  # replace with your info

docker push 123456789012.dkr.ecr.region-name.amazonaws.com/my-repo:latest  # replace with your info

STEP 3 -
Create an Amazon ECS (Elastic Container Service) cluster

Run the following command to create an ECS cluster:

aws ecs create-cluster --cluster-name my-cluster

Create a task definition

A task definition is a description of an application that contains one or more container definitions. You can create this as a JSON file, for example task-definition.json:

{
    "family": "my-task-definition",
    "containerDefinitions": [
        {
            "name": "my-container",
            "image": "123456789012.dkr.ecr.region-name.amazonaws.com/my-repo:latest",
            "essential": true,
            "portMappings": [
                {
                    "containerPort": 80,
                    "hostPort": 80
                }
            ],
            "memory": 500,
            "cpu": 10
        }
    ]
}

Then register it with ECS:

aws ecs register-task-definition --cli-input-json file://task-definition.json

Create a service

A service is a configuration that enables you to run and maintain a specified number of instances of a task definition simultaneously in an Amazon ECS cluster. Run the following command to create a service:

aws ecs create-service --service-name my-service --task-definition my-task-definition --desired-count 1 --cluster my-cluster


Create a deployment pipeline with AWS CodePipeline

AWS CodePipeline is a continuous integration and continuous delivery service. It can be set up to automatically deploy your application whenever there's a change to your Docker image. You can set this up from the AWS Management Console:

Go to the AWS CodePipeline console.
Click on "Create Pipeline".
For the pipeline settings, choose a name for your pipeline and select a role. If no role exists, choose "New service role" to allow CodePipeline to create a role in IAM.
For the source stage, choose AWS ECR and select the repository and image tag you want to use.
For the deploy stage, choose Amazon ECS and select the cluster and service you created earlier.
Click on "Create Pipeline" to create your pipeline.
After this setup, your pipeline will run automatically whenever you push a change to your ECR repository.
