#!/usr/bin/env python3
import aws_cdk as cdk
from website_network_stack import WebsiteNetworkStack
from website_server_stack import WebsiteServerStack

app = cdk.App()

# Network Stack
network_stack = WebsiteNetworkStack(
    app, "WebsiteNetworkStack",
    env=cdk.Environment(
        account="YOUR_ACCOUNT_ID",  # Replace with your AWS account ID
        region="us-east-1"  # Change region as needed
    )
)

# Server Stack - depends on network stack
server_stack = WebsiteServerStack(
    app, "WebsiteServerStack",
    vpc=network_stack.vpc,
    public_subnets=network_stack.public_subnets,
    private_subnets=network_stack.private_subnets,
    web_sg=network_stack.web_sg,
    rds_sg=network_stack.rds_sg,
    env=cdk.Environment(
        account="YOUR_ACCOUNT_ID",  # Replace with your AWS account ID
        region="us-east-1"  # Change region as needed
    )
)

# Add dependency
server_stack.add_dependency(network_stack)

app.synth()
