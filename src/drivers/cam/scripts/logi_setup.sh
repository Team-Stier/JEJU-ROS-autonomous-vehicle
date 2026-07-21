#!/bin/bash

# 1. 카메라 노드가 실행될 때까지 충분히 대기
sleep 3

echo "Starting Logitech C922 (cam_logi) hardware configuration..."

# 2. 전원 주파수 보정 (한국: 2=60Hz) - 실내 형광등 플리커 방지
v4l2-ctl -d /dev/cam_logi --set-ctrl=power_line_frequency=2

# 3. 화이트밸런스 자동 설정 활성화
v4l2-ctl -d /dev/cam_logi --set-ctrl=white_balance_automatic=1

# 4. 노출 기반 FPS 가변 해제 (0 설정 시 고정 FPS 유지에 유리)
# 출력 결과에서 현재 1로 되어 있으므로, 0으로 변경하여 어두운 곳에서도 FPS 저하 방지
v4l2-ctl -d /dev/cam_logi --set-ctrl=exposure_dynamic_framerate=0

# 5. 샤프니스 설정 (0~255 중 128이 기본값, 선명도를 위해 유지 또는 미세 조정)
v4l2-ctl -d /dev/cam_logi --set-ctrl=sharpness=128

# 6. 연속 오토포커스 활성화 (제공된 결과의 focus_automatic_continuous 명칭 사용)
v4l2-ctl -d /dev/cam_logi --set-ctrl=focus_automatic_continuous=1

# 7. 백라이트 보정 활성화 (역광 상황 대비)
v4l2-ctl -d /dev/cam_logi --set-ctrl=backlight_compensation=1

echo "Logitech C922 hardware settings applied successfully!"
