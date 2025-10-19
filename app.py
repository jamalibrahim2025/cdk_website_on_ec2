#!/usr/bin/env python3
import os
import aws_cdk as cdk
from cdk_website_on_ec2.network_stack import NetworkStack
from cdk_website_on_ec2.server_stack import ServerStack

app = cdk.App()

env = cdk.Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION"),
)

# Network Stack
network_stack = NetworkStack(app, "NetworkStack", env=env)

# Server Stack
server_stack = ServerStack(
    app, "ServerStack",
    vpc=network_stack.vpc,
    public_subnets=network_stack.public_subnets,
    private_subnets=network_stack.private_subnets,
    web_sg=network_stack.web_sg,
    rds_sg=network_stack.rds_sg,
    env=env
)

# Add dependency
server_stack.add_dependency(network_stack)

app.synth()
