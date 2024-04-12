from airflow import DAG
from datetime import datetime
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

default_args = {
   'owner': 'aws',
   'depends_on_past': False,
   'start_date': datetime(2019, 2, 20),
   'provide_context': True
}

dag = DAG('kubernetes_nfq_pizza_complete', default_args=default_args, schedule_interval=None)

kube_config_path = '/usr/local/airflow/dags/kube_config.yaml'

startPod = KubernetesPodOperator(
                       namespace="nfq-airflow", 
                       image="704533066374.dkr.ecr.ap-southeast-1.amazonaws.com/nfq-airflow-images:airflw-amd64",
                       cmds=["java"],
                       arguments=["-jar", "app/airflow-java-1.0-SNAPSHOT.jar" ],
                       labels={"foo": "bar"},
                       name="mwaa-pod-java",
                       image_pull_policy="Always",
                       task_id="start-demo",
                       get_logs=True,
                       dag=dag,
                       is_delete_operator_pod=False,
                       config_file=kube_config_path,
                       in_cluster=False,
                       cluster_context='aws'
                       )

podRun = KubernetesPodOperator(
                       namespace="nfq-airflow", 
                       image="704533066374.dkr.ecr.ap-southeast-1.amazonaws.com/nfq-airflow-images:airflw-amd64",
                       cmds=["java"],
                       arguments=["-jar", "app/airflow-java-1.0-SNAPSHOT.jar", "airflow-nfq-rds-mysqlinstance2cfb48f1-x9j3yhq6fny7.ckjnkmqlugio.ap-southeast-1.rds.amazonaws.com" , "nfqrdsdemo" , "SELECT * from pizza_orders;" , "nfq-airflow-dags" , "ap-southeast-1", "arn:aws:secretsmanager:ap-southeast-1:704533066374:secret:MySqlInstanceSecretE6DCC68A-VnDObuh9J4JO-649U5j", "all-pizza.csv"],
                       #arguments=["-jar", "app/airflow-java-1.0-SNAPSHOT.jar" ],
                       labels={"foo": "bar"},
                       name="mwaa-pod-java",
                       image_pull_policy="Always",
                       task_id="get-all-pizza",
                       get_logs=True,
                       dag=dag,
                       is_delete_operator_pod=False,
                       config_file=kube_config_path,
                       in_cluster=False,
                       cluster_context='aws'
                       )

podRun2 = KubernetesPodOperator(
                       namespace="nfq-airflow", 
                       image="704533066374.dkr.ecr.ap-southeast-1.amazonaws.com/nfq-airflow-images:airflw-amd64",
                       cmds=["java"],
                       arguments=["-jar", "app/airflow-java-1.0-SNAPSHOT.jar", "airflow-nfq-rds-mysqlinstance2cfb48f1-x9j3yhq6fny7.ckjnkmqlugio.ap-southeast-1.rds.amazonaws.com" , "nfqrdsdemo" , "SELECT * from pizza_orders WHERE pizza = 'Cheese';" , "nfq-airflow-dags" , "ap-southeast-1", "arn:aws:secretsmanager:ap-southeast-1:704533066374:secret:MySqlInstanceSecretE6DCC68A-VnDObuh9J4JO-649U5j", "cheese-pizza.csv"],
                       labels={"foo": "bar"},
                       name="mwaa-pod-java",
                       image_pull_policy="Always",
                       task_id="get-all-cheese-pizza",
                       get_logs=True,
                       dag=dag,
                       is_delete_operator_pod=False,
                       config_file=kube_config_path,
                       in_cluster=False,
                       cluster_context='aws'
                       )
podRun3 = KubernetesPodOperator(
                       namespace="nfq-airflow", 
                       image="704533066374.dkr.ecr.ap-southeast-1.amazonaws.com/nfq-airflow-images:airflw-amd64",
                       cmds=["java"],
                       arguments=["-jar", "app/airflow-java-1.0-SNAPSHOT.jar", "airflow-nfq-rds-mysqlinstance2cfb48f1-x9j3yhq6fny7.ckjnkmqlugio.ap-southeast-1.rds.amazonaws.com" , "nfqrdsdemo" , "SELECT * from pizza_orders WHERE pizza = 'Hawaiian';" , "nfq-airflow-dags" , "ap-southeast-1", "arn:aws:secretsmanager:ap-southeast-1:704533066374:secret:MySqlInstanceSecretE6DCC68A-VnDObuh9J4JO-649U5j", "hawaiian-pizza.csv"],
                       labels={"foo": "bar"},
                       name="mwaa-pod-java",
                       image_pull_policy="Always",
                       task_id="get-all-hawaiian-pizza",
                       get_logs=True,
                       dag=dag,
                       is_delete_operator_pod=False,
                       config_file=kube_config_path,
                       in_cluster=False,
                       cluster_context='aws'
                       )
startPod >> podRun
startPod >> podRun2
startPod >> podRun3
