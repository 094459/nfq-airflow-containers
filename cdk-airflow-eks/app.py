# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#!/usr/bin/env python3

import aws_cdk as cdk 

from airflow_cdk.airflow_cdk_vpc import AirflowCdkStackVPC
from airflow_cdk.airflow_cdk_eks import AirflowCdkStackEKS
from airflow_cdk.airflow_cdk_rds import AirflowCdkStackRDS
from airflow_cdk.airflow_cdk_mwaa import AirflowCdkStackMWAA

env=cdk.Environment(region="ap-southeast-1", account="xxxxx")
airflow_props = {'airflow_env' : 'nfq-airflow-demo', 'dagslocation' : 'nfq-airflow-dags' , 'rds_name' : 'nfqrdsdemo'}


app = cdk.App()

airflow_eks_cluster_vpc = AirflowCdkStackVPC(
    scope=app,
    id="airflow-nfq-vpc",
    env=env
)

airflow_mwaa = AirflowCdkStackMWAA(
    scope=app,
    id="airflow-nfq-mwaa",
    env=env,
    vpc=airflow_eks_cluster_vpc.vpc,
    airflow_props=airflow_props
)

airflow_eks_cluster_rds = AirflowCdkStackRDS(
    scope=app,
    id="airflow-nfq-rds",
    env=env,
    vpc=airflow_eks_cluster_vpc.vpc,
    airflow_props=airflow_props
)

airflow_eks_cluster = AirflowCdkStackEKS(
    scope=app,
    id="airflow-nfq-eks",
    env=env,
    vpc=airflow_eks_cluster_vpc.vpc,
    airflow_props=airflow_props
)

app.synth()
