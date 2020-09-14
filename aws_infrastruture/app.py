import os
from aws_cdk import core as cdk
from stacks.web_api import WebApi

app = cdk.App()

dev_env = cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ['CDK_DEFAULT_REGION'])
prod_eu_west_2_env = cdk.Environment(account='AKIA4YCOFKCYAHITQJM', region='eu-west-2')
#prod_us_east_1_env = cdk.Environment(account='876337254576', region='us-east-1')

WebApi(app, 'WebApiDev', env=dev_env)
WebApi(app, 'WebApiProdEuWest2', env=prod_eu_west_2_env)
#WebApi(app, 'WebApiProdUsEast1', env=prod_us_east_1_env)

app.synth()