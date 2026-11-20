# 선생님 업무 도구함

초등학교 교사의 수업 및 교실 업무를 돕는 Windows 데스크톱 앱입니다.

## 포함 기능

- QR 코드 생성 및 PNG 저장
- OpenAI API를 이용한 AI 대화
- 스톱워치와 수업 타이머
- 현재 시계와 알람
- 학생 이름 무작위 선정 (중복 없이 한 바퀴)

## GitHub에서 Windows 실행 파일 자동 빌드

1. 이 ZIP 파일을 풀고 안에 있는 **파일과 폴더 전체**를 GitHub 저장소의 최상위(root)에 업로드합니다. `.github` 폴더도 반드시 포함해야 합니다.
2. 저장소의 **Actions** 탭에서 `Build Windows EXE` 작업이 실행되는지 확인합니다. 기본 브랜치가 `main` 또는 `master`라면 파일을 올릴 때 자동 실행됩니다. 필요하면 Actions 탭에서 직접 실행할 수도 있습니다.
3. 작업이 끝나면 해당 실행 기록의 **Artifacts**에서 `TeacherToolkit-Windows`를 내려받아 압축을 풉니다. 안에 `TeacherToolkit.exe`가 있습니다.

빌드 결과는 GitHub Actions 실행 후 30일 동안 보관됩니다. 공개 저장소라면 내려받을 수 있는 사람도 저장소 공개 범위에 따릅니다.

## AI 대화 설정

AI 대화 탭에서 OpenAI API 키를 입력하세요. 앱은 키를 파일에 저장하지 않습니다. API 이용료는 OpenAI 계정에 별도로 청구될 수 있습니다. 모델 칸에는 사용 가능한 모델명을 입력할 수 있고 기본값은 `gpt-4o-mini`입니다.

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
