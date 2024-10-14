# The Great Unicity Deployment Challenge
DevOps Skills Take-Home Challenge

At any step of this process, if you feel blocked, please reach out to derek.hansen@unicity.com for support. The goal of this challenge is to have you perform something similiar to common DevOps tasks in small fashion and to have something that you can demo for us and discuss together.

## Step 0: Dependencies

Development environment:
- Editor
- Browser
- Docker (including docker compose) ([Docker](https://docs.docker.com/))
- Terraform  ([Terraform](https://developer.hashicorp.com/terraform))

Please reach out if you have any questions on setting up these tools.

## Step 1: Run Application in Docker

`docker compose up`

Then in your in browser go to `http://localhost:8080`.

Experiment with the application and ensure it is working.

Docker compose will also run the localstack container which is a mock AWS service that you can use for testing. [LocalStack](https://docs.localstack.cloud/overview/)

You may want to review the documents there to get an idea of it's capabilities.

## Step 2: Create an s3 bucket and deploy the terraform code to localstack

For the application to be able to upload images, you need to create a s3 bucket within localstack.
Create a bucket to store the uploaded images using terraform.

The bucket will need to allow uploads and allow the uploaded images to be access via public url.

Update the app Dockerfile and docker compose file with the needed environment variables to allow the python app to upload images and use the stored images.

There is a sample in `terraform/example/` of creating a s3 bucket, but it doesn't have all it needs for upload and public access. It is primarily there as an example of how to use terraform with localstack. See the `providers.tf` file.

The goal here is to have you create a terraform module to create a s3 bucket with the roles/policies/permissions that would be needed for production.


## Step 3: Technical Review and Interview

Schedule an interview with your Unicity contact. [Booking Link](https://koalendar.com/e/technical-challenge-review)

You will be asked to walk us through your solution to Step 2. You don't need to create a PR 

Then we will ask you to do an additional step live with us. It should be a somewhat simplier version of the step 2 task.

Any additional interview time will be used to deep dive into your technical background and to discuss any questions you have.