#!/bin/bash

# 현재 스크립트가 있는 폴더 경로 확인
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RULES_PATH="$SCRIPT_DIR/../rules/99-stier-sensors.rules"

echo "--- [Team Stier] 센서 환경 설정 시작 ---"

# 1. 시리얼 그룹 추가 (재부팅 후 권한 영구 적용)
sudo usermod -aG dialout $USER

# 2. udev 규칙 파일을 시스템 폴더(/etc/udev/rules.d/)로 복사
if [ -f "$RULES_PATH" ]; then
    sudo cp "$RULES_PATH" /etc/udev/rules.d/
    echo "[성공] udev 규칙 파일이 시스템에 복사되었습니다."
else
    echo "[실패] 규칙 파일을 찾을 수 없습니다: $RULES_PATH"
    exit 1
fi

# 3. 규칙 새로고침 및 즉시 적용
sudo udevadm control --reload-rules
sudo udevadm trigger

echo "--- 모든 설정이 완료되었습니다! 센서를 다시 연결하세요. ---"
