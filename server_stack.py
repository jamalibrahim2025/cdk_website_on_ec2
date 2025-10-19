from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
)
from constructs import Construct

class ServerStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Web Server Security Group
        web_sg = ec2.SecurityGroup(
            self, "WebServerSG",
            vpc=vpc,
            allow_all_outbound=True,
            description="Allow HTTP inbound"
        )
        web_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP from anywhere"
        )

        # RDS Security Group
        db_sg = ec2.SecurityGroup(
            self, "DBSG",
            vpc=vpc,
            allow_all_outbound=True,
            description="Allow MySQL from web servers"
        )
        db_sg.add_ingress_rule(
            web_sg, ec2.Port.tcp(3306), "Allow MySQL from WebServerSG"
        )

        # EC2 Instances (one in each public subnet)
        for i, subnet in enumerate(vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC).subnets):
            ec2.Instance(
                self, f"WebServer{i+1}",
                instance_type=ec2.InstanceType("t3.micro"),
                machine_image=ec2.MachineImage.latest_amazon_linux2023(),
                vpc=vpc,
                vpc_subnets=ec2.SubnetSelection(subnets=[subnet]),
                security_group=web_sg,
                key_name="my-keypair"  # replace with your existing EC2 key pair
            )

        # RDS MySQL Instance
        rds.DatabaseInstance(
            self, "MySQLInstance",
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0_36
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            security_groups=[db_sg],
            instance_type=ec2.InstanceType("t3.micro"),
            allocated_storage=20,
            multi_az=True,
            deletion_protection=False,
            publicly_accessible=False,
            credentials=rds.Credentials.from_generated_secret("admin"),
            database_name="WebAppDB"
        )
