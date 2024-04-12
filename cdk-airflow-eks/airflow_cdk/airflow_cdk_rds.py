from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    RemovalPolicy, Stack, CfnOutput
)

from constructs import Construct

class AirflowCdkStackRDS(Stack):

    def __init__(self, scope: Construct, id: str, vpc, airflow_props, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        instance_type = ec2.InstanceType.of(ec2.InstanceClass.MEMORY5, ec2.InstanceSize.LARGE)

        engine_version = rds.MysqlEngineVersion.VER_8_0_35

        testdb = rds.DatabaseInstance(self, "MySqlInstance",
            database_name=f"{airflow_props['rds_name']}",
            engine=rds.DatabaseInstanceEngine.mysql(version=engine_version),
            instance_type=instance_type,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            vpc=vpc,
            port=3306,
            publicly_accessible=True,
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False
        )

        CfnOutput(
                self, "RDS_DNS_Endpoint",
                value=testdb.db_instance_endpoint_address,
                description="The DNS address of your RDS instance",
                export_name="RDSInstanceAddress"
            )
        CfnOutput(
                self, "RDS_Secret",
                value=testdb.secret.to_string(),
                description="The AWS Secret for your admin password",
                export_name="RDSAdminUserAWSSecret"
            )




