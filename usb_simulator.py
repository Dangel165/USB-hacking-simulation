import pygame
import random
import math
from enum import Enum

pygame.init()

WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("USB 충전기 보안 시뮬레이터")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLACK = (15, 15, 15)
BLUE = (66, 135, 245)
RED = (255, 71, 87)
GREEN = (52, 211, 153)
YELLOW = (255, 193, 7)
GRAY = (107, 114, 128)
DARK_GRAY = (31, 41, 55)
LIGHT_GRAY = (209, 213, 219)
CYAN = (34, 211, 238)
ORANGE = (251, 146, 60)
PURPLE = (147, 51, 234)

class SimState(Enum):
    MENU = 1
    SIMULATION = 2
    INFO = 3
    CREDITS = 4

class Charger:
    def __init__(self, x, y, is_infected, name):
        self.x = x
        self.y = y
        self.is_infected = is_infected
        self.name = name
        self.width = 70
        self.height = 90
        self.data_flow = []
        self.attack_counter = 0
    
    def draw(self, surface):
        color = RED if self.is_infected else GREEN
        pygame.draw.rect(surface, color, (self.x - self.width//2, self.y - self.height//2, self.width, self.height), 2)
        
        pygame.draw.circle(surface, YELLOW, (self.x - 15, self.y + self.height//2 - 10), 5)
        pygame.draw.circle(surface, YELLOW, (self.x + 15, self.y + self.height//2 - 10), 5)
        
        status = "악성" if self.is_infected else "정상"
        try:
            font = pygame.font.Font("C:\\Windows\\Fonts\\malgun.ttf", 13)
        except:
            font = pygame.font.Font(None, 13)
        text = font.render(status, True, color)
        surface.blit(text, (self.x - 20, self.y - 40))

class Device:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.width = 100
        self.height = 120
        self.status = "정상"
        self.infection_level = 0
        self.processes = []
        self.firewall_enabled = False
    
    def draw(self, surface):
        if self.status == "정상":
            color = GREEN
        elif self.status == "감염중":
            color = ORANGE
        else:
            color = RED
        
        pygame.draw.rect(surface, color, (self.x - self.width//2, self.y - self.height//2, self.width, self.height), 2)
        
        pygame.draw.rect(surface, DARK_BLACK, (self.x - self.width//2 + 5, self.y - self.height//2 + 10, self.width - 10, 50))
        pygame.draw.rect(surface, DARK_GRAY, (self.x - self.width//2 + 5, self.y - self.height//2 + 10, self.width - 10, 50), 1)
        
        try:
            font = pygame.font.Font("C:\\Windows\\Fonts\\malgun.ttf", 11)
        except:
            font = pygame.font.Font(None, 11)
        
        infection_text = font.render(f"감염도: {self.infection_level}%", True, RED if self.infection_level > 0 else GREEN)
        surface.blit(infection_text, (self.x - 45, self.y - 30))
        
        bar_width = self.width - 10
        pygame.draw.rect(surface, DARK_GRAY, (self.x - bar_width//2, self.y + 30, bar_width, 8), 1)
        if self.infection_level > 0:
            pygame.draw.rect(surface, RED, (self.x - bar_width//2, self.y + 30, bar_width * self.infection_level // 100, 8))
        
        if self.firewall_enabled:
            pygame.draw.circle(surface, GREEN, (self.x, self.y), self.width//2 + 20, 2)

def draw_text(surface, text, x, y, size=24, color=WHITE, bold=False):
    try:
        font = pygame.font.Font("C:\\Windows\\Fonts\\malgun.ttf", size)
    except:
        try:
            font = pygame.font.Font("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", size)
        except:
            font = pygame.font.Font(None, size)
    rendered = font.render(text, True, color)
    surface.blit(rendered, (x, y))

def draw_background(surface):
    surface.fill(DARK_BLACK)
    # 상단 배너
    pygame.draw.rect(surface, DARK_GRAY, (0, 0, WIDTH, 60))
    pygame.draw.line(surface, BLUE, (0, 60), (WIDTH, 60), 2)

def draw_menu(surface):
    draw_background(surface)
    
    draw_text(surface, "USB 충전기 보안 시뮬레이터", 50, 15, 32, BLUE)
    
    # 메인 컨텐츠
    draw_text(surface, "어떤 시뮬레이션을 실행하시겠습니까?", 250, 180, 36, WHITE)
    
    # 버튼 영역
    button_y = 320
    
    # 시뮬레이션 버튼
    pygame.draw.rect(surface, DARK_GRAY, (150, button_y, 280, 140), 1)
    pygame.draw.rect(surface, DARK_GRAY, (150, button_y, 280, 140), 2)
    draw_text(surface, "시뮬레이션 실행", 195, button_y + 35, 26, GREEN)
    draw_text(surface, "클릭으로 시작", 225, button_y + 75, 16, GRAY)
    
    # 정보 버튼
    pygame.draw.rect(surface, DARK_GRAY, (550, button_y, 280, 140), 1)
    pygame.draw.rect(surface, DARK_GRAY, (550, button_y, 280, 140), 2)
    draw_text(surface, "정보 (I)", 620, button_y + 35, 26, CYAN)
    draw_text(surface, "USB 해킹 원리", 610, button_y + 75, 16, GRAY)
    
    # 제작자 정보 버튼
    pygame.draw.rect(surface, DARK_GRAY, (950, button_y, 280, 140), 1)
    pygame.draw.rect(surface, DARK_GRAY, (950, button_y, 280, 140), 2)
    draw_text(surface, "제작자 정보 (C)", 995, button_y + 35, 26, PURPLE)
    draw_text(surface, "크레딧", 1055, button_y + 75, 16, GRAY)
    
    # 하단 안내
    draw_text(surface, "아무 곳이나 클릭하여 시뮬레이션을 시작하세요", 350, 750, 16, GRAY)

def draw_info(surface):
    draw_background(surface)
    
    draw_text(surface, "USB 충전기 해킹 원리", 50, 15, 32, CYAN)
    
    y = 100
    info_lines = [
        ("1. 공격 방식", BLUE, 22),
        ("   악성 충전기는 기기와의 통신 중 악성 펌웨어를 전송합니다", GRAY, 18),
        ("   공격자는 기기의 민감한 정보를 탈취합니다", GRAY, 18),
        ("", WHITE, 18),
        ("2. 악성 충전기 제작 방법", RED, 22),
        ("   교육용 정보입니다. 불법 사용은 범죄입니다.", ORANGE, 16),
        ("   1) 일반 USB 충전기를 분해하여 회로기판 접근", GRAY, 18),
        ("   2) 마이크로컨트롤러(Arduino, Raspberry Pi)를 추가", GRAY, 18),
        ("   3) USB 데이터 라인(D+, D-)에 악성 펌웨어 설치", GRAY, 18),
        ("   4) 기기 연결 시 자동으로 악성코드 전송하도록 프로그래밍", GRAY, 18),
        ("   5) 정상적인 충전 기능도 유지하여 적발 회피", GRAY, 18),
        ("", WHITE, 18),
        ("4. 위험한 시나리오", BLUE, 22),
        ("   공항, 카페, 도서관 등 공용 충전소에서 감염 위험 증가", GRAY, 18),
        ("   기기가 감염되면 개인정보 유출, 악성코드 설치 가능", GRAY, 18),
        ("", WHITE, 18),
        ("4. 방어 방법", BLUE, 22),
        ("   신뢰할 수 있는 제조사의 정품 충전기 사용", GREEN, 18),
        ("   공용 충전소 사용 최소화", GREEN, 18),
        ("   USB 디버깅 모드 비활성화", GREEN, 18),
        ("   정기적인 보안 업데이트 설치", GREEN, 18),
        ("   방화벽 및 보안 소프트웨어 활성화", GREEN, 18),
    ]
    
    for line, color, size in info_lines:
        if line:
            draw_text(surface, line, 80, y, size, color)
        y += 35
    
    draw_text(surface, "Press 'M' to Menu | Press 'C' for Credits", 550, 820, 14, GRAY)

def draw_credits(surface):
    draw_background(surface)
    
    draw_text(surface, "제작자 정보", 50, 15, 32, PURPLE)
    
    y = 100
    credits_lines = [
        ("USB 충전기 보안 시뮬레이터", 26, BLUE),
        ("", 18, WHITE),
        ("개발자 정보", 22, PURPLE),
        ("개발자:Dangel", 18, GRAY),
        ("", 18, WHITE),
        ("프로젝트 정보", 22, PURPLE),
        ("이 프로젝트는 USB 충전기 해킹의 위험성을 시각화하고", 18, GRAY),
        ("사용자들의 보안 인식을 높이기 위해 만들어졌습니다.", 18, GRAY),
        ("", 18, WHITE),
        ("주요 기능", 22, PURPLE),
        ("• 실시간 악성 데이터 전송 시뮬레이션", 18, GRAY),
        ("• 공격자의 데이터 탈취 과정 시각화", 18, GRAY),
        ("• 방화벽 활성화/비활성화 효과 비교", 18, GRAY),
        ("• 감염도 리얼타임 추적", 18, GRAY),
        ("", 18, WHITE),
        ("기술 스택", 22, PURPLE),
        ("Language: Python 3.x", 18, GRAY),
        ("Graphics: Pygame", 18, GRAY),
        ("", 18, WHITE),
        ("사용 방법", 22, PURPLE),
        ("[F] - 방화벽 ON/OFF", 18, GRAY),
        ("[R] - 시뮬레이션 리셋", 18, GRAY),
        ("[M] - 메뉴로 돌아가기", 18, GRAY),
        ("[I] - 정보 보기", 18, GRAY),
        ("[C] - 제작자 정보", 18, GRAY),
    ]
    
    for line, size, color in credits_lines:
        if line:
            draw_text(surface, line, 100, y, size, color)
        y += 32
    
    draw_text(surface, "Press 'M' to Menu | Press 'I' for Info", 550, 820, 14, GRAY)

def draw_simulation(surface, chargers, device, time_passed, data_packets, intercepted_data):
    draw_background(surface)
    
    draw_text(surface, "실시간 시뮬레이션", 50, 15, 32, YELLOW)
    
    # 좌측 정보 패널
    info_x = 50
    info_y = 100
    
    draw_text(surface, "┌─ 시뮬레이션 정보", info_x, info_y, 16, BLUE)
    draw_text(surface, f"│ 경과 시간: {time_passed // 60:02d}초 {time_passed % 60:02d}프레임", info_x + 10, info_y + 35, 16, CYAN)
    draw_text(surface, f"│ 충전기 상태: {'악성 감지' if chargers[1].is_infected else '정상'}", info_x + 10, info_y + 60, 16, RED if chargers[1].is_infected else GREEN)
    draw_text(surface, f"│ 방화벽: {'활성화' if device.firewall_enabled else '비활성화'}", info_x + 10, info_y + 85, 16, GREEN if device.firewall_enabled else RED)
    draw_text(surface, "└─", info_x, info_y + 110, 16, BLUE)
    
    # 충전기 시뮬레이션 영역
    sim_y = 280
    draw_text(surface, "충전기", 80, sim_y - 50, 16, LIGHT_GRAY)
    
    for i, charger in enumerate(chargers):
        charger.x = 180 + i * 220
        charger.y = sim_y
        charger.draw(surface)
    
    # 연결선 및 기기
    device_sim_y = sim_y + 150
    draw_text(surface, "기기", 1200, sim_y - 50, 16, LIGHT_GRAY)
    
    device.x = 1350
    device.y = device_sim_y
    device.draw(surface)
    
    for charger in chargers:
        pygame.draw.line(surface, CYAN, (charger.x, charger.y + 50), (device.x - 60, device.y), 1)
        pygame.draw.circle(surface, CYAN, (charger.x, charger.y + 50), 3)
    
    # 데이터 패킷 표시
    for packet in data_packets:
        progress = packet['progress']
        start_x, start_y = packet['start_x'], packet['start_y']
        end_x, end_y = device.x - 60, device.y
        
        current_x = start_x + (end_x - start_x) * progress
        current_y = start_y + (end_y - start_y) * progress
        
        color = RED if packet['is_malicious'] else GREEN
        pygame.draw.circle(surface, color, (int(current_x), int(current_y)), 4)
    
    # 우측 데이터 탈취 정보
    right_x = 900
    right_y = 100
    
    draw_text(surface, "┌─ 탈취된 정보", right_x, right_y, 16, RED)
    
    if len(intercepted_data) > 0:
        y_offset = right_y + 35
        for data in intercepted_data[-5:]:
            draw_text(surface, f"│ • {data}", right_x + 10, y_offset, 15, ORANGE)
            y_offset += 30
    else:
        draw_text(surface, "│ 아직 탈취된 정보 없음", right_x + 10, right_y + 35, 15, GRAY)
    
    draw_text(surface, "└─", right_x, right_y + 185, 16, RED)
    
    # 하단 통계
    stats_y = 670
    pygame.draw.rect(surface, DARK_GRAY, (50, stats_y, WIDTH - 100, 180), 1)
    
    draw_text(surface, "통계", 70, stats_y + 15, 16, YELLOW)
    
    col1_x = 100
    col2_x = 500
    col3_x = 900
    stat_y = stats_y + 55
    
    draw_text(surface, f"감염도: {device.infection_level}%", col1_x, stat_y, 16, RED if device.infection_level > 50 else YELLOW if device.infection_level > 0 else GREEN)
    draw_text(surface, f"활성 패킷: {len(data_packets)}", col2_x, stat_y, 16, CYAN)
    draw_text(surface, f"탈취 데이터: {len(intercepted_data)}개", col3_x, stat_y, 16, ORANGE)
    
    # 제어 안내
    draw_text(surface, "[F] 방화벽 | [R] 리셋 | [M] 메뉴", col1_x, stat_y + 50, 14, GRAY)
    
    # 감염 100% 이벤트
    if device.infection_level >= 100:
        # 배경 어둡게
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # 경고 박스
        box_width = 800
        box_height = 300
        box_x = (WIDTH - box_width) // 2
        box_y = (HEIGHT - box_height) // 2
        
        pygame.draw.rect(surface, RED, (box_x, box_y, box_width, box_height), 3)
        pygame.draw.rect(surface, DARK_BLACK, (box_x, box_y, box_width, box_height))
        
        draw_text(surface, "시스템 감염 완료!", box_x + 150, box_y + 30, 32, RED)
        draw_text(surface, "", box_x + 50, box_y + 80, 18, WHITE)
        draw_text(surface, "기기가 100% 감염되었습니다!", box_x + 150, box_y + 80, 20, ORANGE)
        draw_text(surface, "", box_x + 50, box_y + 110, 18, WHITE)
        draw_text(surface, f"탈취된 정보: {len(intercepted_data)}개 항목", box_x + 150, box_y + 110, 18, YELLOW)
        draw_text(surface, f"개인정보 유출 위험 수준: 매우 높음", box_x + 150, box_y + 145, 18, RED)
        draw_text(surface, f"악성코드 설치 상태: 활성화", box_x + 150, box_y + 180, 18, RED)
        draw_text(surface, "", box_x + 50, box_y + 210, 18, WHITE)
        draw_text(surface, "[R] 리셋 | [M] 메뉴로 돌아가기", box_x + 180, box_y + 240, 16, CYAN)

def main():
    state = SimState.MENU
    time_passed = 0
    data_packets = []
    intercepted_data = []
    attack_rate = 60
    
    sensitive_data = [
        "연락처 목록",
        "문자 메시지",
        "이메일 주소",
        "결제 정보",
        "비밀번호",
        "위치 정보",
        "사진",
        "통화 기록",
    ]
    
    chargers = [
        Charger(0, 0, False, "정상 충전기 1"),
        Charger(0, 0, True, "악성 충전기"),
        Charger(0, 0, False, "정상 충전기 2"),
    ]
    
    device = Device(1100, 500, "스마트폰")
    
    running = True
    while running:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == SimState.MENU:
                    # 시뮬레이션 버튼 (250~500, 350~470)
                    if 250 <= mx <= 500 and 350 <= my <= 470:
                        state = SimState.SIMULATION
                        time_passed = 0
                        data_packets = []
                        intercepted_data = []
                        device.infection_level = 0
                        device.firewall_enabled = False
                    # 정보 버튼 (550~800, 350~470)
                    elif 550 <= mx <= 800 and 350 <= my <= 470:
                        state = SimState.INFO
                    # 제작자 정보 버튼 (850~1100, 350~470)
                    elif 850 <= mx <= 1100 and 350 <= my <= 470:
                        state = SimState.CREDITS
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    state = SimState.MENU
                elif event.key == pygame.K_i:
                    state = SimState.INFO
                elif event.key == pygame.K_c:
                    state = SimState.CREDITS
                elif event.key == pygame.K_r:
                    if state == SimState.SIMULATION:
                        time_passed = 0
                        data_packets = []
                        intercepted_data = []
                        device.infection_level = 0
                        device.firewall_enabled = False
                elif event.key == pygame.K_f:
                    if state == SimState.SIMULATION:
                        device.firewall_enabled = not device.firewall_enabled
        
        if state == SimState.SIMULATION:
            time_passed += 1
            
            for charger in chargers:
                if charger.is_infected and time_passed % attack_rate == 0:
                    for _ in range(random.randint(1, 3)):
                        data_type = random.choice(sensitive_data)
                        data_packets.append({
                            'is_malicious': True,
                            'progress': 0,
                            'start_x': charger.x,
                            'start_y': charger.y + 50,
                            'label': '악성'
                        })
                        if not device.firewall_enabled:
                            if data_type not in intercepted_data:
                                intercepted_data.append(data_type)
                
                if not charger.is_infected and time_passed % (attack_rate * 2) == 0:
                    data_packets.append({
                        'is_malicious': False,
                        'progress': 0,
                        'start_x': charger.x,
                        'start_y': charger.y + 50,
                        'label': '정상'
                    })
            
            for packet in data_packets[:]:
                packet['progress'] += 0.02
                
                if packet['progress'] >= 1:
                    if packet['is_malicious']:
                        if not device.firewall_enabled:
                            device.infection_level = min(100, device.infection_level + 5)
                        else:
                            device.infection_level = max(0, device.infection_level - 2)
                    
                    data_packets.remove(packet)
            
            if device.infection_level == 0:
                device.status = "정상"
            elif device.infection_level < 100:
                device.status = "감염중"
            else:
                device.status = "감염됨"
        
        if state == SimState.MENU:
            draw_menu(screen)
        elif state == SimState.INFO:
            draw_info(screen)
        elif state == SimState.CREDITS:
            draw_credits(screen)
        elif state == SimState.SIMULATION:
            draw_simulation(screen, chargers, device, time_passed, data_packets, intercepted_data)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()