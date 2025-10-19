from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    core
)

class NetworkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC with two AZs
        self.vpc = ec2.Vpc(
            self, "WebsiteVPC",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ]
        )

        # Separate public/private subnets
        self.public_subnets = self.vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC).subnets
        self.private_subnets = self.vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED).subnets

        # Security group for web servers
        self.web_sg = ec2.SecurityGroup(
            self, "WebServerSG",
            vpc=self.vpc,
            allow_all_outbound=True,
            description="Allow HTTP traffic from anywhere"
        )
        self.web_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP from anywhere")

        # Security group for RDS
        self.rds_sg = ec2.SecurityGroup(
            self, "RDSSG",
            vpc=self.vpc,
            allow_all_outbound=True,
            description="Allow MySQL access from web servers"
        )
        # Only allow access from web servers
        self.rds_sg.add_ingress_rule(self.web_sg, ec2.Port.tcp(3306), "Allow MySQL from web servers")

