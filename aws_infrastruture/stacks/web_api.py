import os

from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    core as cdk
)
from cdk_chalice import Chalice


class WebApi(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the DynamoDB table using CDK, and add its name to stack output.
        partition_key = dynamodb.Attribute(name='username',
                                           type=dynamodb.AttributeType.STRING)
        self.dynamodb_table = dynamodb.Table(
            self, 'UsersTable', partition_key=partition_key,
            removal_policy=cdk.RemovalPolicy.DESTROY)
        cdk.CfnOutput(self, 'UsersTableName', value=self.dynamodb_table.table_name)

        # The Lambda function invoked by API Gateway should have access to the DynamoDB table,
        # so I create an IAM role for it and grant the role access to the table.
        lambda_service_principal = iam.ServicePrincipal('lambda.amazonaws.com')
        self.api_handler_iam_role = iam.Role(self, 'ApiHandlerLambdaRole',
                                             assumed_by=lambda_service_principal)

        self.dynamodb_table.grant_read_write_data(self.api_handler_iam_role)

        # web_api_source_dir is a path to Chalice application source code.

        web_api_source_dir = os.path.join(os.path.dirname(__file__), os.pardir,
                                      os.pardir, 'flask')

        # The source code is used by cdk-chalice for packaging the app to
        # produce SAM template and ZIP file for deployment as Lambda function.
        chalice_stage_config = self._create_chalice_stage_config()
        self.chalice = Chalice(
            self, 'WebApi', source_dir=web_api_source_dir,
            stage_config=chalice_stage_config)

    # mapped the previously created IAM role to api_handler Lambda function,
    # and passed DynamoDB table name as environment variable. API Gateway stage name,
    # Lambda memory size and Lambda timeout are also defined here.
    def _create_chalice_stage_config(self):
        chalice_stage_config = {
            'api_gateway_stage': 'v1',
            'lambda_functions': {
                'api_handler': {
                    'manage_iam_role': False,
                    'iam_role_arn': self.api_handler_iam_role.role_arn,
                    'environment_variables': {
                        'DYNAMODB_TABLE_NAME': self.dynamodb_table.table_name
                    },
                    'lambda_memory_size': 128,
                    'lambda_timeout': 10
                }
            }
        }

        return chalice_stage_config
