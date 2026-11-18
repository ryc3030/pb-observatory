"""ko_style 회귀 시험: python3 scripts/test_ko_style.py"""
from ko_style import polish

CASES = [
    ("참여 예산 총회가 화요일 디지털 투표로 시작됩니다.", "참여예산 총회, 화요일 디지털 투표로 시작"),
    ("2026년 주민참여예산 사업 27건이 완료되었습니다.", "2026년 주민참여예산 사업 27건 완료"),
    ("소치에서는 교육 기관에서 20개의 주민참여예산제 프로젝트가 시행되고 있습니다.", "소치에서는 교육 기관에서 20개의 주민참여예산제 프로젝트 시행 중"),
    ("벨라코가 주민참여예산제 시행의 중심지가 될 것입니다.", "벨라코, 주민참여예산제 시행의 중심지가 될 전망"),
    ("시민 예산 - 투표를 시작합니다! • 그워구프시 정보 서비스", "시민예산 - 투표를 시작 • 그워구프시 정보 서비스"),
    ("포르투 알레그레: 주민참여예산제 회의가 시작됩니다.", "포르투알레그리: 주민참여예산제 회의 시작"),
    ("어린이 놀이터가 개장했습니다.", "어린이 놀이터 개장"),
    ("예산이 많습니다.", "예산이 많다"),
    ('기록적인 참여 예산: "이제 공사가 시작됩니다"', '기록적인 참여예산: "이제 공사가 시작됩니다"'),
]
PAPERS = [("권한이 위임된 정부에서의 참여적 예산 편성: 케냐 사례", "권한이 위임된 정부에서의 참여예산: 케냐 사례")]

if __name__ == "__main__":
    bad = 0
    for src, want in CASES:
        got = polish(src)
        if got != want:
            bad += 1
            print("FAIL", src, "\n  got ", got, "\n  want", want)
    for src, want in PAPERS:
        if polish(src, "paper") != want:
            bad += 1
            print("FAIL paper", src, polish(src, "paper"))
    print("ok" if not bad else f"{bad} failed")
