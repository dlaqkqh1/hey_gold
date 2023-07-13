import boto3
from discord_bot.config.environment import AWSS3Connect
from datetime import datetime
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
from kafka import KafkaAdminClient, KafkaConsumer, TopicPartition, OffsetAndMetadata
from kafka.producer import KafkaProducer


def create_topic(bootstrap_servers, name, partitions, replica=1):
    client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    try:
        topic = NewTopic(
            name=name,
            num_partitions=partitions,
            replication_factor=replica)
        client.create_topics([topic])
    except TopicAlreadyExistsError as e:
        print(e)
        pass
    finally:
        client.close()


def send_data_to_topic(bootstrap_servers, name, text):
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        client_id="hey_kafka_producer",
    )

    producer.send(
        topic=name,
        key=text.encode('utf-8'),
        value=text.encode('utf-8'))

    producer.flush()


def upload_file_to_s3(file_name, object_name=None):
    bucket_name = 'hey-kafka'
    file_path = f'{AWSS3Connect.PATH}{file_name}'

    # S3 클라이언트 생성
    s3_client = boto3.client('s3',
                             aws_access_key_id=AWSS3Connect.ACCESS_ID,
                             aws_secret_access_key=AWSS3Connect.ACCESS_KEY,
                             region_name=AWSS3Connect.REGION
                             )

    s3_client.upload_file(file_path, bucket_name, file_name)


def upload_data_to_s3():
    topic_name = "hey_kafka"
    bootstrap_servers = ["localhost:9092"]
    consumer_group_id = "hey_kafka_consumer"

    consumer = KafkaConsumer(
        bootstrap_servers=bootstrap_servers,
        group_id=consumer_group_id,
        key_deserializer=lambda x: x.decode('utf-8'),
        value_deserializer=lambda x: x.decode('utf-8'),
        auto_offset_reset='earliest',
        consumer_timeout_ms=10000,  # 타임아웃을 5초로 설정
        enable_auto_commit=False)

    current_time = datetime.now()
    consumer.subscribe([topic_name])
    data = []

    try:
        for record in consumer:
            print(f"""데이터 {record.value} 를 파티션 {record.partition} 의 {record.offset} 번 오프셋에서 읽어옴""")
            data.append(record.value)
            topic_partition = TopicPartition(record.topic, record.partition)
            offset = OffsetAndMetadata(record.offset + 1, record.timestamp)
            consumer.commit({
                topic_partition: offset
            })
        consumer.close()

        with open(f'discord_bot/s3_data/{current_time}.txt', 'w') as file:
            for text in data:
                file.write(text + '\n')
        file.close()

        upload_file_to_s3(f'{current_time}.txt')
    except:
        pass
