# Git Copilot

Git Copilot은 개발자를 돕기 위해 지능형 코드 제안을 제공하고 반복적인 코딩 작업을 자동화하는 Python 기반 프로젝트입니다. 이 프로젝트는 AI를 활용하여 생산성을 높이고 개발 과정을 간소화합니다.

## 주요 기능

- 브랜치 간 커밋 데이터를 분석하고 CSV 파일로 저장
- 커밋 메시지를 요약하여 Markdown 파일로 생성
- AI를 활용한 커밋 요약 및 분석
- CLI를 통한 간편한 실행 및 옵션 제공

## 시작하기

저장소를 클론하고 설정 지침을 따라 시작하세요.

## 설치 방법

1. 저장소를 클론합니다:

   ```bash
   git clone https://github.com/<your-repo>/git-copilot.git
   ```

2. 프로젝트 디렉터리로 이동합니다:

   ```bash
   cd git-copilot
   ```

3. 필요한 패키지를 설치합니다:

   ```bash
   pip install -r requirements.txt
   ```

## 환경변수 설정

Git Copilot을 실행하기 전에 `.env` 파일을 설정해야 합니다. 아래는 필요한 환경변수 목록입니다:

- `OPENAI_API_KEY`: OpenAI API 키를 설정합니다.
- `GIT_REPOSITORY_PATH`: 분석할 Git 저장소의 경로를 설정합니다.

### `.env` 파일 예시

```dotenv
OPENAI_API_KEY="your-openai-api-key"
GIT_REPOSITORY_PATH="path-to-your-git-repository"
```

`.env_example` 파일을 참고하여 `.env` 파일을 생성하고 필요한 값을 입력하세요.

## 실행 방법 (CLI)

CLI를 사용하여 Git Copilot을 실행하려면 다음 명령을 입력하세요:

```bash
python main.py --before <이전-브랜치명 또는 커밋번호> --after <이후-브랜치 또는 커밋번호> --version <버전-이름>
```

예시:

```bash
python main.py --before main --after feature-branch --version v1.0
```

### 옵션 설명

- `--before`: 비교할 이전 브랜치의 이름을 지정합니다.
- `--after`: 비교할 이후 브랜치의 이름을 지정합니다.
- `--version`: 결과 파일에 사용할 버전 이름을 지정합니다.

### 실행 결과

- `data/<버전-이름>.csv`: 브랜치 간 커밋 데이터를 CSV 파일로 저장합니다.
- `data/<버전-이름>.md`: 요약된 커밋 내용을 Markdown 파일로 저장합니다.

## 프롬프트 커스터마이징

Git Copilot은 기본적으로 `prompts/summarize_commits.md` 파일에 정의된 프롬프트를 사용하여 커밋 요약을 생성합니다. 필요에 따라 이 파일을 수정하여 원하는 형식이나 내용을 반영할 수 있습니다.

### 기본 프롬프트 예시

```md
커밋 로그의 정보를 바탕으로, 카테고리별로 분류된 업데이트 스펙 문서를 작성해주세요. 

최대한 모든 커밋을 넣어주세요.

제가 제공하는 정보로만 작업내역을 정리해주세요.
```

### 커스터마이징 방법

1. `prompts/summarize_commits.md` 파일을 열어 내용을 수정합니다.
2. 원하는 형식과 지침을 추가하거나 변경합니다.
3. 저장 후 `main.py`를 실행하면 수정된 프롬프트가 적용됩니다.
