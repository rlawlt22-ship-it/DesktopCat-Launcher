# 🐾 Desktop Cat Launcher (나만의 데스크톱 펫 & 런처)

## 1. 프로젝트 개요 (Overview)
"삭막한 코딩 환경에 귀여운 힐링과 편리함을!"

이 프로젝트는 Python `tkinter` 라이브러리를 활용하여 개발한 데스크톱 컴패니언(Desktop Companion) 어플리케이션입니다.
단순히 화면에 떠 있는 캐릭터를 넘어, 사용자의 생산성을 높여주는 즐겨찾기 런처(Launcher) 기능을 결합했습니다.
특히 이미지 파일을 로드하는 방식이 아닌, 코드로 직접 그래픽을 그리는 방식을 채택하여 프로그램 용량을 최소화하고 실행 속도를 최적화했습니다.

## 2. 핵심 기능 및 기술적 특징 (Key Features)

### 🎨 1. Pure Code Graphic & Animation
* No Image Files : 외부 이미지(png, jpg) 없이 오직 Python 코드(`Canvas` 드로잉)만으로 고양이 캐릭터와 애니메이션을 구현했습니다.
* Transparent Window : `overrideredirect`와 `transparentcolor` 기술을 적용하여 윈도우 테두리를 없애고 배경을 투명하게 처리, 고양이가 실제 바탕화면 위에 존재하는 듯한 몰입감을 줍니다.

### 🚀 2. Smart Quick Launcher (기능성)
* Context Menu System: 고양이를 마우스 우클릭하면 커스텀 메뉴가 나타납니다.
* Shortcut Management: 구글, 유튜브 같은 웹사이트뿐만 아니라 계산기(`calc`), 메모장(`notepad`) 등 응용 프로그램도 실행 가능합니다.
* Data Persistence (데이터 영구 저장): 사용자가 추가/삭제한 메뉴는 `bookmarks.txt` 파일에 실시간으로 저장되어, 프로그램을 재실행해도 데이터가 유지됩니다.

### ⚙️ 3. Algorithm-based Interaction
* Drift Correction (좌표 보정): 애니메이션 반복 시 캐릭터의 위치가 미세하게 어긋나는 현상을 방지하기 위해, 상태 기반(State-based) 이동 로직을 구현했습니다.
* Interactive AI:
    * Drag & Drop: 마우스 드래그로 고양이를 원하는 위치로 옮길 수 있습니다.
    * Petting Effect: 클릭 시 랜덤한 대사와 함께 하트/별 등의 파티클 이펙트가 발생합니다.
    * Sleep Mode: 15초 이상 상호작용이 없으면 눈을 감고 조는 '절전 모드'로 자동 전환됩니다.

### 🎨 4. Customization
* Random Color Generation: 메뉴의 '색깔 바꾸기' 기능을 통해 고양이의 털 색상을 랜덤하게 변경할 수 있습니다.

## 3. 개발 환경 (Environment)
* OS : Windows 10/11
* Language : Python 3.12
* Modules :
    * `tkinter`: GUI 및 그래픽 렌더링
    * `os`, `webbrowser`: 시스템 명령어 및 웹 브라우저 제어
    * `random`, `time`: 난수 생성 및 애니메이션 타이밍 제어

## 4. 실행 결과 (Screenshots)

### 📌 메인 실행 화면
> 배경이 투명하게 처리되어 바탕화면 아이콘 위에 고양이가 자연스럽게 배치된 모습입니다.
![Main Screen](img/cat_main.png)

### 🖱️ 런처 메뉴 사용
> 우클릭을 통해 즐겨찾기 메뉴를 열고 관리하는 모습입니다.
![Menu Screen](img/cat_menu.png)

### 💤 졸음 모드 (Sleep Mode)
> 사용자가 15초 동안 아무런 동작을 하지 않으면, 고양이가 눈을 감고 조는 상태로 변합니다. (알고리즘 적용)
![Sleep Screen](img/cat_sleep.png)

## 5. 설치 및 실행 (How to Run)
1. 저장소를 다운로드(Clone) 합니다.
2. Python이 설치된 환경에서 `main.py`를 실행합니다.
   ```bash
   python main.py