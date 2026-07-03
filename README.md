# GitLab CI/CD와 Ansible을 활용한 자동화 창고관리시스템 구축

# 프로젝트 목적

본 프로젝트는 GitLab CI/CD와 Ansible을 활용한 자동화 창고관리시스템(WMS) 구축 프로젝트다.

GitLab Pipeline을 통해 소스 코드 관리부터 빌드, 테스트, 배포까지의 CI/CD 프로세스를 자동화하고, Ansible을 이용해 서버 환경 구성 및 애플리케이션 배포를 코드 기반으로 관리한다.

이를 통해 반복적인 수동 작업을 최소화하고, 안정적이고 일관된 운영 환경을 구축하여 창고관리시스템의 배포 효율성과 유지보수성을 향상시키는 것을 목표로 한다.

# 구현 범위

<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/f53cd3ee-d943-4cd0-93fa-f7cc3c5ae210" />
<br>
<br>

여러 대의 서버를 하나로 묶어 관리하는 환경 구성 , 파이썬 프로그램, 대용량 데이터 처리 장치(Kafka)를 연결해 만든 창고 관리 시스템


**핵심 트래픽 및 데이터 흐름**
- 사용자 진입: 직원이 PC나 모바일 웹 화면으로 접속하면, NGINX라는 프로그램이 가장 먼저 요청을 받아 안전하게 내부 서버들로 나누어 보낸다.

- 기능별 서버 분리: 입고, 출고, 재고(위치/이동), QR 스캔 기능이 각각 별도의 독립된 방(컨테이너)에서 실행한다. 하나의 기능에 문제가 생기거나 사용자가 몰려도 다른 기능은 영향을 받지 않는다.

- 데이터 저장 방식: 중요한 마스터 정보는 메인 저장소(PostgreSQL)에 안전하게 저장하고, 자주 쓰는 정보는 초고속 임시 저장소(Redis)에 두어 화면이 빠르게 뜨도록 한다. 현장에서 QR 코드를 대량으로 찍을 때 발생하는 과부하는 중간 완충 장치(Kafka)가 받아주어 서버가 다운되는 것을 막는다.
<br>

**프로그램 개발 및 자동 설치 과정**

- 자동 배포: 개발자가 수정된 코드를 깃랩(GitLab)에 올리면, 시스템이 알아서 이를 포장하여 안전한 보관소(Harbor)에 저장한 뒤, 실제 운영 중인 서버에 사용자가 눈치채지 못하도록 멈춤 없이 자동으로 교체 및 설치한다.

# 담당 역할
앤서블을 이용하여 서버 자동 구축

[Ansible 작업 기록](https://app.notion.com/p/Ansible-390a48359dbb80f78483d187e0ede9c0?source=copy_link)

```
Role 구성 → Inventory 작성 → Playbook 작성 → site.yml 작성(전체 실행) → ansible-playbook 실행 → 서버 자동 구축 완료
```
<br>
<br>

깃랩 CI/CD 파이프라인 구축

[Gitlab 작업 기록](https://www.notion.so/Ansible-390a48359dbb80f78483d187e0ede9c0?source=copy_link)

```
Git Repository 구성 → .gitlab-ci.yml 작성 → Pipeline Stage 구성 → Build → Test →Docker Image Build
→ Harbor Push → Kubernetes Deploy → Pod Rolling Update
```
                      

# 기술 스택

<img width="1536" height="1024" alt="ChatGPT Image 2026년 6월 30일 오전 11_37_50" src="https://github.com/user-attachments/assets/de9642fa-0ad4-47f3-bbfc-8a6232e6169e" />


# 네트워크 구성 (Logical Architecture)

<img width="200" height="200" alt="pfsense" src="https://github.com/user-attachments/assets/c2241ae6-a962-4688-82a6-cc3fa011e0f7" />
<br>

Pfsense으로 적용한 프로토콜
- 방화벽

**서비스 네트워크 토폴로지 구성도**



# Ansible 서버 자동화 구성



Ansible은 Playbook을 실행하여 여러 Role을 순차적으로 호출하고, 각 Role이 담당하는 서버 구성을 자동으로 수행하는 구조로 구성되어 있다.

**Ansible 동작 과정**

`ansible-playbook` 실행 → **site.yml**이 전체 작업 시작 → **Playbook**이 **Role** 호출 → **Role**의 **Task(main.yml)** 실행 → 서버 구성 및 서비스 자동 구축 완료


```
ansible-infra/
├── ansible.cfg                
├── inventory/                 
│   └── hosts.ini
├── group_vars/               
│   └── all.yml
│
├── playbooks
│   ├── deploy.yml
│   ├── gitlab-install.yml
│   ├── init-server.yml
│   ├── k8s-master-init.yml
│   ├── k8s-worker-join.yml
│   ├── kubernetes-install.yml
│   ├── reset.yml
│   └── site.yml           
│
└── roles/                     
    ├── common/                
    ├── database/              
    ├── harbor/                
    ├── k8s-master/            
    └── k8s-worker/
    ├── gitlab / 
    └── gitlab-runner/

```
roles 파일 구성
각 서버의 role은 tasks, handlers, templates 으로 이루어 져있다
tasks은 ~~~
handlers은 ~~~
templates 은 ~~~ 의 역할을 한다.

특히 tasks 의 main.yml은 

```
1. 사전 준비
   - apt update
   - 필요한 패키지 설치
   - 사용자/디렉터리 생성

2. 프로그램 설치
   - Docker
   - Kubernetes
   - GitLab 등

3. 설정 적용
   - template
   - copy
   - lineinfile

4. 서비스 시작/활성화
   - systemd
   - service

5. 검증(선택)
   - 서비스 상태 확인
   - 명령 실행 확인
```

위의 과정을 기본 구조로 정하고 작성하였다.
자세한 코드 설명은 아래의 notion 링크에 정리하였으니 참고 하면된다.
[Ansible 작업 기록](https://app.notion.com/p/Ansible-390a48359dbb80f78483d187e0ede9c0?source=copy_link)





---

---
**inbentory 코드 예시**
네트워크 구성 끝나면 바로 작성 할 것

```
d
```

# CI/CD Pipeline

GitLab 서버와 GitLab Runner를 Ansible을 이용하여 자동화 방식으로 구축하였다.

CI/CD 배포를 담당하는 GitLab Runner를 설치 및 등록하였으며,

GitLab 서버는 http://10.1.201.127 환경으로 구성하였다.

```
GitLab CI/CD 동작 과정
GitLab CI/CD Pipeline을 통해 코드 변경 사항을 감지하고 자동으로 빌드 및 배포 과정을 수행한다.

Git push
  ↓
GitLab CI
  ↓
Docker build
  ↓
Harbor push (저장소)
  ↓
K8s deploy
```
<br>
위와 같은 파이프 라인을 구성하기 위해 .gitlab-ci.yml 파일을 작성하여 프로젝트의 웹을 배포 한다.
<br>

```
.gitlab-ci.yml 
stages:
  - test
  - build

variables:
  IMAGE_NAME: test-app
  TAG: $CI_COMMIT_SHORT_SHA

# 1. CI 정상 확인용
test:
  stage: test
  tags:
    - docker
  script:
    - echo "CI PIPELINE WORKING"
    - echo "Runner OK"
    - uname -a
    - echo "Network independent mode"

# 2. 가짜 build (외부 없음)
build:
  stage: build
  tags:
    - docker
  script:
    - echo "BUILD STAGE START"
    - echo "No Docker build yet (network not ready)"
    - echo "Simulating build process"
    - mkdir -p dist
    - echo "dummy artifact" > dist/app.txt
  artifacts:
    paths:
      - dist/
```

# 서비스 구성
(DB / Redis / Kafka 등)
쿠버네티스 구성하는 사람꺼 인용하기

# 트러블슈팅 / 장애 해결

# 결과 및 성과
웹 만든거 구현 화면 여기에 넣기
# 느낀점
