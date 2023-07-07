import requests
from airflow import DAG
from datetime import datetime
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


dag = DAG(
        dag_id='material_prices',
        start_date=datetime(2022, 1, 1),  # 날짜가 미래인 경우 실행이 안됨
        schedule='0 3 * * MON-FRI   ',  # 적당히 조절
        max_active_runs=1,
        catchup=False
)


def get_redshift_connection(autocommit=True):
    hook = PostgresHook(postgres_conn_id='redshift_dev_db')
    conn = hook.get_conn()
    conn.autocommit = autocommit
    return conn.cursor()


def material_extract(**context):
    """
    금, 은 데이터 API 호출
    """
    API_KEY = Variable.get('nasdaq_api_key')
    date = str(context['execution_date']).replace('-', '')[:8]
    material = context['params']['material']
    request_url = f"https://data.nasdaq.com/api/v3/datasets/LBMA/{material}.json?api_key={API_KEY}&start_date={date}&end_date={date}"
    gold_res = requests.get(request_url)
    context['ti'].xcom_push(key=material, value=gold_res.json()['dataset']['data'])


def redshift_load(**context):
    """
    금, 은 데이터 INSERT
    """
    cur = get_redshift_connection()
    material = context['params']['material']
    data = context['ti'].xcom_pull(key=material)
    for d in data:
        sql = f"INSERT INTO {material}_prices VALUES ('{d[0]}', '{d[1]}', '{d[2]}')"
        try:
            cur.execute(sql)

        except:
            continue


gold_extract = PythonOperator(
        task_id='gold_extract',
        python_callable=material_extract,
        params={'material': 'GOLD'},
        provide_context=True,
        dag=dag
    )

silver_extract = PythonOperator(
        task_id='silver_extract',
        python_callable=material_extract,
        params={'material': 'SILVER'},
        provide_context=True,
        dag=dag
    )


gold_load = PythonOperator(
        task_id='gold_load',
        python_callable=redshift_load,
        params={'material': 'GOLD'},
        provide_context=True,
        dag=dag
    )


silver_load = PythonOperator(
        task_id='silver_load',
        python_callable=redshift_load,
        params={'material': 'SILVER'},
        provide_context=True,
        dag=dag
    )


gold_extract >> gold_load
silver_extract >> silver_load
