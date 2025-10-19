from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

class NetworkStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # VPC with 2 AZs, 1 public + 1 private per AZ
        self.vpc = ec2.Vpc(
            self, "WebAppVPC",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="PublicSubnet",
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    name="PrivateSubnet",
                    cidr_mask=24
                )
            ]
        )
