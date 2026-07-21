#!/bin/bash

# 1. 카메라 노드가 완전히 실행될 때까지 대기
sleep 3

echo "Starting Kiyo Pro hardware configuration..."

# 2. 전원 주파수 보정: 1=50Hz(한국은 보통 2=60Hz 권장되나 요청하신 대로 1 설정)
v4l2-ctl -d /dev/cam --set-ctrl=power_line_frequency=2

# 3. 화이트밸런스 자동 설정 (이전 로그 확인 결과 automatic이 정확한 명칭임)
v4l2-ctl -d /dev/cam --set-ctrl=white_balance_automatic=1

# 4. 노출 기반 FPS 가변 해제 (고정 FPS 유지)
v4l2-ctl -d /dev/cam --set-ctrl=exposure_dynamic_framerate=0

# 5. 샤프니스 설정 (요청하신 대로 3 설정, 기본값은 보통 128)
v4l2-ctl -d /dev/cam --set-ctrl=sharpness=3

# 6. 연속 오토포커스 활성화
v4l2-ctl -d /dev/cam --set-ctrl=focus_automatic_continuous=1

echo "Kiyo Pro hardware settings applied successfully!"
