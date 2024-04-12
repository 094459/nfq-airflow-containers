from aws_cdk.lambda_layer_kubectl_v29 import KubectlV29Layer
from aws_cdk import (
    aws_eks as eks,
    aws_ec2 as ec2,
    aws_iam as iam,
    Stack,
    CfnOutput
)

from constructs import Construct

class AirflowCdkStackEKS(Stack):

    def __init__(self, scope: Construct, id: str, airflow_props, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        eks_cluster_admin_role = iam.Role(
            self,
            "ClusterAdminRole",
            assumed_by=iam.CompositePrincipal(iam.AccountRootPrincipal(), iam.ServicePrincipal("ec2.amazonaws.com"))
            )
        
        cluster_admin_policy_statement_json_1 = {
                "Effect": "Allow",
                "Action": [
                    "eks:DescribeCluster",
                    "sts:GetCallerIdentity"
                ],
                "Resource": "*"
            }
        
        
        eks_cluster_admin_role.add_to_principal_policy(
                iam.PolicyStatement.from_json(cluster_admin_policy_statement_json_1))
        

        trusted_policy_statement_json2 = {
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Principal": {
                    "AWS": "arn:aws:iam::704533066374:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_AdministratorAccess_d61658aa9a839cbd/ricsue@amazon.co.uk"
                    },
                "Condition":{}
        }

        trusted_policy = iam.PolicyDocument()
        trusted_policy.add_statements(iam.PolicyStatement.from_json(trusted_policy_statement_json2))
        #eks_cluster_admin_role.assume_role_policy = trusted_policy
               
        cluster = eks.Cluster(
            self,
            "Airflow-EKS",
            vpc=vpc,
            version=eks.KubernetesVersion.V1_29,
            kubectl_layer=KubectlV29Layer(self, "kubectl"),
            default_capacity_instance=ec2.InstanceType("m5.large"),
            default_capacity=1,
            endpoint_access=eks.EndpointAccess.PUBLIC_AND_PRIVATE,
            vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)],
            masters_role=eks_cluster_admin_role
            )
        
        ##use if you do want to create a new user
        #admin_user = iam.User(self, "ops") 
        ## use if you want to use an existing user
        admin_user = iam.User.from_user_name(self,"Existing EKS Admin User", "ops")
        cluster.aws_auth.add_user_mapping(admin_user, groups=["system:masters"])
        ##role mapping if you are using IdC with SSO
        #admin_role = iam.Role.from_role_arn(self, "Existing EKS Admin Role", "arn:aws:sts::704533066374:assumed-role/AWSReservedSSO_AdministratorAccess_d61658aa9a839cbd/ricsue@amazon.co.uk")
        #cluster.aws_auth.add_role_mapping(admin_role, groups=["system:masters"])

        ng = cluster.add_nodegroup_capacity(
            "x86",
            desired_size=1, 
            instance_types=[ec2.InstanceType(it) for it in ['c4.2xlarge', 'c5.2xlarge', 'c5d.2xlarge', 'c5a.2xlarge', 'c5n.2xlarge']],
            nodegroup_name="x86",
            node_role=cluster.default_nodegroup.role
            )

        ng.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite"))
        ng.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        
        # for the purpose of the demo, we will add broad permissions to S3 and RDS - do NOT do this in production!

        ng.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"))
        ng.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonRDSFullAccess"))

        CfnOutput(
                self, "EKSClusterName",
                value=cluster.cluster_name,
                description="The name of the EKS Cluster",
                export_name="EKSClusterName"
            )
        # Output the EKS Cluster OIDC Issuer and Export it
        CfnOutput(
                self, "EKSClusterOIDCProviderARN",
                value=cluster.open_id_connect_provider.open_id_connect_provider_arn,
                description="The EKS Cluster's OIDC Provider ARN",
                export_name="EKSClusterOIDCProviderARN"
            )
        # Output the EKS Cluster kubectl Role ARN
        CfnOutput(
                self, "EKSClusterKubectlRoleARN",
                value=cluster.kubectl_role.role_arn,
                description="The EKS Cluster's kubectl Role ARN",
                export_name="EKSClusterKubectlRoleARN"
            )
        # Output the EKS Cluster SG ID
        CfnOutput(
                self, "EKSSGID",
                value=cluster.kubectl_security_group.security_group_id,
                description="The EKS Cluster's kubectl SG ID",
                export_name="EKSSGID"
            )




