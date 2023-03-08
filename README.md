# pykinect-recorder

## 가상환경 구축 및 패키지 설치
```bash
python -m venv .env
pip install -r requirements.txt

python main.py
```

```bash
ufmt format .
black .
```

## Setup process
### 1. Azure Kinect camera 연결 후 SDK 설치
SDK 설치 링크 : https://github.com/microsoft/Azure-Kinect-Sensor-SDK/blob/develop/docs/usage.md

### 2. "Azure Kinect 1.4.1/tools" 아래 record_with_mic.py 복사

### 3. "Azure Kinect 1.4.1/" 폴더에 권환 부여 (저장때문인데, "Videos/" 에 저장하면 굳이 필요 없을듯 함.)
### 4. Visual C++ 설치

- Build Tools 설치 링크 : https://www.microsoft.com/ko-KR/download/details.aspx?id=48159 <br>
- C++ Desktop 설치 링크 : https://visualstudio.microsoft.com/ko/ 

### 5. 가상 환경 설치 및 관련 패키지 설치
```bash
conda create -n azure python=3.8 -y
conda activate azure

pip install -r requirements.txt
pip install pyk4a --no-use-pep517 --global-option=build_ext --global-option="-IC:\Program Files\Azure Kinect SDK v1.4.1\sdk\include" --global-option="-LC:\Program Files\Azure Kinect SDK v1.4.1\sdk\windows-desktop\amd64\release\lib"
```

### 6. 실행.ps1파일 생성
- 메모에 아래 코드 작성 후 확장자 .ps1으로 저장
    ```bash
    conda activate azure
    python .\tools\record_with_mic.py
    ```