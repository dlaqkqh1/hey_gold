# discord bot 헤이골드

## 프로젝트 소개
> ### 학습한 내용을 활용해 보기위해 만든 discord bot 채팅을 통해 데이터를 다루는 것이 목표이다.

<br>

## 제공 서비스
### 연도별 최대 금값 혹은 은값 추출 / 카프카 데이터 생성 및 S3로 적재

<br>

## 프로젝트 아키텍쳐
![제목 없는 다이어그램 drawio (1)](https://github.com/dlaqkqh1/hey_gold/assets/30038066/637cf258-44d0-43d1-9037-2fa30f0c5e30)

<br>

## 활용 기술 및 프레임워크
#### 1. Data ETL : `Airflow, Kafka`
    - 로컬 Docker 위에서 Airflow와 Kafka 컨테이너를 띄워 사용

#### 2. back-end : `Python, Discord Bot API`
    - 금, 은 데이터 추출에 pySpark의 SparkSQL을 사용

#### 3. Data Sotrage
    - 금, 은 데이터 보관용으로 Redshift 사용 / Kafka 데이터 저장을 위해 S3 사용

<br>

## 예시화면

### 금, 은 값 추출 커맨드
```
헤이골드 연도별최대
헤이실버 연도별최대
```
![image](https://github.com/dlaqkqh1/hey_gold/assets/30038066/c0835070-9e88-41fe-b528-1f5ffa65102c)

### 카프카 통신 커맨드
```
- 카프카 토픽에 메시지 전송 (s3 명령 제외)
헤이카프카 토픽에 전송할 메시지

- s3로 저장하는 커멘드
헤이카프카 s3 
```

### 금, 은 값 추출 커맨드
```
헤이골드 연도별최대
헤이실버 연도별최대
```
![image](https://github.com/dlaqkqh1/hey_gold/assets/30038066/c0835070-9e88-41fe-b528-1f5ffa65102c)

### 저장된 s3 스토리지
![image](https://github.com/dlaqkqh1/hey_gold/assets/30038066/cdef2e6f-893a-453b-997a-1ecaf9dfb2b3)

### 금, 은 가격 데이터를 가져오는 airflow의 web 서버 화면
![image](https://github.com/dlaqkqh1/hey_gold/assets/30038066/3079d0b3-b03f-4929-9172-33a6fa71aceb)


### 후기
    - 사실 금, 은 데이터와 Kafka 데이터를 다루는 것은 아무런 관련이 없지만, Kafka를 사용해 보고싶어서 끼워 넣었다.
    - 디스코드 봇도 한번 만들어보고 싶었는데 막상 무슨 기능을 넣을지 막막했던 것 같다.
    
#### 좋았던점
    - 데이터를 좋아하기도 하고 다루어 보고 싶었던 다양한 데이터 기술을 다루어서 매우 흥미로웠다.
    - 혼자 프로젝트를 진행해보는 경험이 소중했던 것 같다.
    - 부족한 부분을 깨달을 수 있었던 것 같다.
### 아쉬운점
    - Python 프로젝트 구조를 잡는것이 생각보다 힘들었다. 이 부분은 공부 디자인패턴 같은 것을 공부해봐야 겠다.
    - Spark와 Kafka는 각각 대용량과 실시간 데이터 처리를 위한 것인데, 그러한 환경을 만들지 못해 아쉽다.
    - Python 예외처리를 새부적으로 하지 못한 것이 아쉽다.
    
