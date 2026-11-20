# 선생님 업무 도구함

초등학교 교사의 수업 및 교실 업무를 돕는 Windows 데스크톱 앱입니다.

## 포함 기능

- QR 코드 생성 및 PNG 저장
- Google Gemini API를 이용한 AI 대화
- 스톱워치와 수업 타이머
- 현재 시계와 알람
- 학생 이름 무작위 선정 (중복 없이 한 바퀴)

## GitHub에서 Windows 실행 파일 자동 빌드

1. 이 ZIP 파일을 풀고 안에 있는 **파일과 폴더 전체**를 GitHub 저장소의 최상위(root)에 업로드합니다. `.github` 폴더도 반드시 포함해야 합니다.
2. 저장소의 **Actions** 탭에서 `Build Windows EXE` 작업이 실행되는지 확인합니다. 기본 브랜치가 `main` 또는 `master`라면 파일을 올릴 때 자동 실행됩니다. 필요하면 Actions 탭에서 직접 실행할 수도 있습니다.
3. 작업이 끝나면 해당 실행 기록의 **Artifacts**에서 `TeacherToolkit-Windows`를 내려받아 압축을 풉니다. 안에 `TeacherToolkit.exe`가 있습니다.

빌드 결과는 GitHub Actions 실행 후 30일 동안 보관됩니다. 공개 저장소라면 내려받을 수 있는 사람도 저장소 공개 범위에 따릅니다.

## AI 대화 설정

1. [Google AI Studio](https://aistudio.google.com/apikey)에 Google 계정으로 로그인합니다.
2. API 키 페이지에서 `API 키 만들기`를 눌러 Gemini API 키를 발급하고 복사합니다.
3. 앱의 `AI 대화` 탭에서 `Google Gemini API 키` 칸에 붙여넣습니다.
4. 모델 기본값은 `gemini-3.8-flash`입니다. 계정에서 사용할 수 있는 다른 모델 ID로 바꿀 수도 있습니다.

기본 설정에서는 앱이 API 키를 저장하지 않습니다. 개인용 실행 파일에 키를 미리 넣으려면 GitHub 저장소의 **Settings → Secrets and variables → Actions → New repository secret**에서 이름을 `GEMINI_API_KEY`로, 값에 발급받은 키를 입력하세요. 이 워크플로는 키를 소스 파일에 기록하지 않고 빌드 중 임시 설정으로 넣습니다. 키를 포함한 실행 파일은 키를 추출할 수 있으므로 본인 PC에서만 사용하고 공유하지 마세요. 사용량·요금·무료 제공 한도는 Google AI Studio의 Usage/Billing 페이지에서 확인하세요. 앱은 Gemini Interactions API를 사용합니다.

## 실행 중 참고

- QR 코드 생성에는 인터넷이 필요하지 않습니다.
- 시계 알람과 타이머는 앱이 켜져 있을 때 동작합니다.
- 학생 이름 목록은 앱을 닫으면 저장되지 않습니다.

## 로컬에서 직접 실행/빌드 (선택)

Python 3.12 이상에서:

```bash
python -m pip install -r requirements.txt
python app.py
```

Windows 실행 파일 직접 빌드:

```bash
python -m pip install pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name TeacherToolkit app.py
```

실행 파일은 `dist/TeacherToolkit.exe`에 생성됩니다.
