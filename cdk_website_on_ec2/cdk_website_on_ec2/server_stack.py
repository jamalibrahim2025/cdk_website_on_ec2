from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    core
)

class ServerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str,
                 vpc,
                 public_subnets,
                 private_subnets,
                 web_sg,
                 rds_sg,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Launch one EC2 web server in each public subnet
        for i, subnet in enumerate(public_subnets):
            ec2.Instance(
                self, f"WebServer{i+1}",
                instance_type=ec2.InstanceType("t2.micro"),
                machine_image=ec2.AmazonLinuxImage(),
                vpc=vpc,
                vpc_subnets=ec2.SubnetSelection(subnets=[subnet]),
                security_group=web_sg
            )

        # Create RDS MySQL instance in private subnets
        rds.DatabaseInstance(
            self, "MySQLInstance",
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0_33
            ),
            instance_type=ec2.InstanceType("t2.micro"),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=private_subnets),
            security_groups=[rds_sg],
            allocated_storage=20,
            multi_az=False,
            publicly_accessible=False,
            database_name="WebsiteDB",
            removal_policy=core.RemovalPolicy.DESTROY
        )
