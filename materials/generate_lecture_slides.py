#!/usr/bin/env python3
"""중학교 선생님 대상 AI 실습 연수 — 10매 PPT + PDF 생성"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

OUT_DIR = Path(__file__).parent
PPTX_PATH = OUT_DIR / "AI_lecture_script.pptx"
PDF_PATH = OUT_DIR / "AI_lecture_script.pdf"
FONT_PATH = OUT_DIR / "fonts" / "NotoSansKR.ttf"
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf"


def ensure_font():
    if FONT_PATH.exists():
        return
    FONT_PATH.parent.mkdir(parents=True, exist_ok=True)
    import urllib.request
    print("Downloading Noto Sans KR font...")
    urllib.request.urlretrieve(FONT_URL, FONT_PATH)

# 브랜드 컬러 (웹 가이드와 통일)
BLUE = RGBColor(0x3B, 0x82, 0xF6)
BLUE_DARK = RGBColor(0x1E, 0x40, 0xAF)
PINK = RGBColor(0xF4, 0x72, 0xB6)
SLATE = RGBColor(0x33, 0x41, 0x55)
SLATE_LIGHT = RGBColor(0x64, 0x74, 0x8B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
EMERALD = RGBColor(0x05, 0x96, 0x69)

SLIDES = [
    {
        "title": "AI와 함께 스마트하게 일하기",
        "subtitle": "중학교 선생님 대상 생성형 AI 실습 연수",
        "bullets": [
            "광주아이온(AI-ON) · Gemini · NotebookLM",
            "연수 시간: 50분  |  실습 중심",
        ],
        "type": "title",
        "notes": (
            "안녕하세요, 선생님. 오늘은 생성형 AI를 수업과 학교 업무에 어떻게 활용할 수 있는지 "
            "함께 실습해 보는 시간입니다. AI가 낯설어도 괜찮습니다. 오늘 배운 내용은 강의 후에도 "
            "따라할 수 있는 실습 가이드 페이지 링크로 드릴 예정입니다."
        ),
    },
    {
        "title": "오늘의 목표 & 50분 로드맵",
        "bullets": [
            "목표 ① 광주아이온 접속과 Gemini·NotebookLM 기본 사용법 익히기",
            "목표 ② 수업·업무에 바로 쓸 수 있는 프롬프트 실습하기",
            "목표 ③ 강의 후 스스로 활용할 수 있는 가이드 확보하기",
            "0~5분 아이온 → 5~20분 NotebookLM → 20~32분 업무 활용",
            "32~45분 Gemini → 45~50분 마무리 & Q&A",
        ],
        "notes": (
            "오늘 50분 동안 네 가지 도구를 다룹니다. 먼저 광주아이온에 접속하는 방법부터 시작하고, "
            "NotebookLM으로 학교 문서 기반 업무를, Gemini로 글쓰기·자료 제작을, 마지막에는 "
            "'이럴 때 뭘 쓰지?' 고민될 때 보는 상황별 가이드를 안내드리겠습니다."
        ),
    },
    {
        "title": "처음이신가요? 3분 빠른 시작",
        "bullets": [
            "STEP 1  광주아이온(aion.gen.go.kr) 접속 → teacher@genedu.kr 로그인",
            "STEP 2  가이드 페이지의 [복사] 버튼으로 프롬프트 복사 → AI에 붙여넣기",
            "STEP 3  AI 결과는 '초안' — 선생님이 꼭 확인하고 수정 후 사용",
            "💡 글자가 작으면 가이드 상단 [가+] 버튼  |  용어는 [AI 기초 도움말] 참고",
            "📌 강의 후에도 이 링크만 있으면 언제든 따라하실 수 있습니다",
        ],
        "notes": (
            "실습 전에 세 가지만 기억해 주세요. 첫째, 광주아이온에 로그인합니다. "
            "둘째, 오늘 드리는 가이드 페이지에서 [복사] 버튼을 누르면 예시 문장이 복사됩니다. "
            "셋째, AI가 만든 결과는 반드시 선생님께서 확인하고 수정한 뒤 사용하세요. "
            "지금부터 화면을 함께 보시면서 따라해 주시면 됩니다."
        ),
    },
    {
        "title": "광주아이온(AI-ON) 마스터하기",
        "time": "[0~5분]",
        "bullets": [
            "통합 ID 하나로 Gemini, NotebookLM, 클래스룸, 드라이브 자동 연결 (SSO)",
            "메인 화면 위젯 클릭 → Gemini / NotebookLM 바로 이동",
            "[나의 화면 구성하기]로 자주 쓰는 위젯 배치 조절",
            "학습 분석 대시보드: 학생 활동·퀴즈 리포트·학습 패턴 확인",
        ],
        "notes": (
            "광주아이온은 선생님 아이디 하나로 모든 에듀테크가 연결되는 통합 플랫폼입니다. "
            "지금 함께 aion.gen.go.kr에 접속해 보겠습니다. 로그인 후 메인 화면에서 "
            "Gemini와 NotebookLM 위젯을 찾아 클릭해 보세요. 우측 [나의 화면 구성하기]로 "
            "자주 쓰는 위젯을 앞에 배치할 수 있습니다."
        ),
    },
    {
        "title": "NotebookLM — 나만의 학교 비서",
        "time": "[5~20분]",
        "bullets": [
            "1-1. 학교 규정·학사일정·공문 업로드 → 학교 전문 챗봇",
            "1-2. 학생 보고서 업로드 → 세특(생기부) 초안 작성",
            "1-3. 성취기준·작년 평가계획 → 새 평가계획 초안",
            "1-4. 교과서 PDF → 평가 문항·루브릭(채점기준표) 제작",
            "실습: + 새 노트 → + 소스 추가 → 하단에서 질문하기",
        ],
        "notes": (
            "NotebookLM은 선생님이 올린 문서만을 기반으로 답변합니다. "
            "학교 규정 PDF, 학사일정, 학생 활동 보고서를 소스로 올리면 "
            "'현장체험학습 마감일이 언제야?', '이 학생 세특 초안 써줘'처럼 질문할 수 있습니다. "
            "지금 가이드의 프롬프트 [복사] 버튼을 눌러 하나씩 실습해 보겠습니다."
        ),
    },
    {
        "title": "부서별 · 담임 업무 맞춤 활용",
        "time": "[20~32분]",
        "bullets": [
            "교무기획부: 학사일정 정리, 회의록 요약, 연간 계획 시사점 도출",
            "교육연구부: 수행평가 루브릭, 학교평가 보고서 개요 작성",
            "담임 — 학부모 소통: 가정통신문·상담일지 요약 초안",
            "담임 — 학급 활동: 협동 프로젝트·중1 적응 프로그램 아이디어",
            "💡 가이드 페이지에서 내 업무에 맞는 프롬프트를 [복사]해 바로 시도",
        ],
        "notes": (
            "부서와 담임 업무별로 활용 예시를 준비했습니다. "
            "교무기획부 선생님은 학사일정 표 정리, 담임 선생님은 학부모 안내문 초안에 활용하시면 좋습니다. "
            "가이드 페이지에서 본인 업무에 가까운 프롬프트를 골라 [복사]한 뒤 Gemini나 NotebookLM에 붙여 넣어 보세요."
        ),
    },
    {
        "title": "Gemini 심화 — 만능 조수",
        "time": "[32~45분]",
        "bullets": [
            "2-1. @기능: @Google 지도, @Drive, @YouTube 실시간 연동",
            "2-2. Gems: 자주 쓰는 AI 역할 저장 (프롬프트·양식 생성기)",
            "2-3. Google Forms: 'Create form with Gemini'로 설문 자동 생성",
            "2-4. 슬라이드 7단계: 내용 구성 → 이미지 → 슬라이드 → 발표 스크립트",
            "⚠️ Forms 사용 시: 언어 English 설정 + Workspace Labs 가입 (최초 1회)",
        ],
        "notes": (
            "Gemini는 새로운 글과 자료를 만드는 데 강합니다. "
            "@Google 지도로 수학여행 동선을, Forms Gemini로 설문을 자동 생성할 수 있습니다. "
            "슬라이드는 Gemini로 내용을 구성한 뒤, 구글 슬라이드의 제미나이 패널에서 이미지와 슬라이드를 만드는 "
            "7단계 프로세스를 따르시면 됩니다. Forms는 최초 1회 영어 설정이 필요합니다."
        ),
    },
    {
        "title": "워크스페이스+ 심화 팁",
        "time": "[45~48분]",
        "bullets": [
            "스프레드시트: '국어 80점 이상 학생 특징 분석해줘' — 함수 없이 자연어 분석",
            "클래스룸: 학생 과제 PDF 업로드 → 성취기준 기반 맞춤 피드백 초안",
            "[BONUS] 2022 개정 교육과정 반영 수업 설계 프롬프트",
            "역량 중심 수업에서 '학생이 스스로 질문 생성' 활동 포함 요청",
        ],
        "notes": (
            "워크스페이스+ 기능을 조금 더 살펴보겠습니다. "
            "스프레드시트에서 복잡한 함수 없이 자연어로 성적 데이터를 분석할 수 있고, "
            "클래스룸에서 학생 과제에 대한 피드백 초안을 받을 수 있습니다. "
            "방학에 수업을 설계하실 때 2022 개정 교육과정 프롬프트도 활용해 보세요."
        ),
    },
    {
        "title": "상황별 활용 가이드 — 강의 후 참고",
        "bullets": [
            "📄 참고 문서가 있으면 → NotebookLM  |  ✨ 새로 만들 일이면 → Gemini",
            "규정·일정·세특·평가 → NotebookLM  |  가정통신문·슬라이드·설문 → Gemini",
            "3월 학기 초: 학부모 안내  |  4~6월: 평가 준비  |  7월: 세특 기록",
            "가이드 페이지 [상황별 활용] 섹션 + 상단 검색창으로 프롬프트 바로 찾기",
            "📌 페이지 링크 북마크 → 강의 후에도 체크리스트와 함께 자기주도 실습",
        ],
        "notes": (
            "강의가 끝난 뒤 가장 많이 받는 질문이 '이럴 때 뭘 써야 하나요?'입니다. "
            "간단히 말하면, 학교 문서를 기반으로 답이 필요하면 NotebookLM, "
            "새로운 글이나 자료를 만들 때는 Gemini를 쓰시면 됩니다. "
            "가이드 페이지 맨 아래 [상황별 활용]에 표로 정리해 두었으니 북마크해 두세요."
        ),
    },
    {
        "title": "마무리 — AI는 선생님의 파트너",
        "bullets": [
            "🔒 개인정보: 학생 실명·연락처 등 민감 정보는 AI에 입력 금지",
            "🔍 사실 확인: AI 생성 정보는 반드시 공신력 있는 자료로 재확인",
            "✅ 최종 판단: 모든 교육적 판단의 책임은 선생님에게 있습니다",
            "AI는 선생님을 대체하지 않고, 아이들과의 교감에 더 집중하도록 돕습니다",
            "실습 가이드 링크 공유  →  Q&A",
        ],
        "type": "closing",
        "notes": (
            "마지막으로 꼭 기억해 주실 세 가지입니다. 개인정보는 절대 입력하지 마시고, "
            "AI가 알려준 내용은 반드시 확인하신 뒤 사용하세요. "
            "AI는 선생님을 대체하는 것이 아니라 업무를 돕는 파트너입니다. "
            "오늘 드린 실습 가이드 링크를 저장해 두시면 언제든 다시 따라하실 수 있습니다. "
            "질문 있으신 선생님 편하게 말씀해 주세요. 감사합니다."
        ),
    },
]


def set_slide_bg(slide, prs, color: RGBColor):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_accent_bar(slide, prs, top=Inches(0), height=Inches(0.12), color=BLUE):
    shape = slide.shapes.add_shape(1, Inches(0), top, prs.slide_width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def add_textbox(slide, left, top, width, height, text, size=18, bold=False, color=SLATE, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    return tf


def add_bullets(tf, items, size=16, color=SLATE, spacing=Pt(8)):
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.level = 0
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = spacing
        p.bullet = True


def build_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    for data in SLIDES:
        layout = prs.slide_layouts[6]  # blank
        slide = prs.slides.add_slide(layout)
        slide_type = data.get("type", "content")

        if slide_type == "title":
            set_slide_bg(slide, prs, BLUE_DARK)
            add_accent_bar(slide, prs, Inches(6.8), Inches(0.15), PINK)
            add_textbox(slide, Inches(0.8), Inches(1.8), Inches(11.5), Inches(1.2),
                         data["title"], size=40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
            add_textbox(slide, Inches(0.8), Inches(3.2), Inches(11.5), Inches(0.8),
                         data["subtitle"], size=22, color=RGBColor(0xBF, 0xDB, 0xFE), align=PP_ALIGN.CENTER)
            tf = add_textbox(slide, Inches(1.5), Inches(4.5), Inches(10), Inches(1.5),
                             "", size=18, color=RGBColor(0xE2, 0xE8, 0xF0), align=PP_ALIGN.CENTER)
            add_bullets(tf, data["bullets"], size=18, color=RGBColor(0xE2, 0xE8, 0xF0), spacing=Pt(12))

        elif slide_type == "closing":
            set_slide_bg(slide, prs, RGBColor(0x0F, 0x17, 0x2A))
            add_accent_bar(slide, prs, Inches(0), Inches(0.12), PINK)
            add_textbox(slide, Inches(0.8), Inches(0.6), Inches(11.5), Inches(1),
                         data["title"], size=32, bold=True, color=RGBColor(0x93, 0xC5, 0xFD))
            tf = add_textbox(slide, Inches(0.9), Inches(1.8), Inches(11.2), Inches(4.8), "", size=17,
                             color=RGBColor(0xCB, 0xD5, 0xE1))
            add_bullets(tf, data["bullets"], size=17, color=RGBColor(0xCB, 0xD5, 0xE1), spacing=Pt(14))

        else:
            set_slide_bg(slide, prs, WHITE)
            add_accent_bar(slide, prs)
            time_label = data.get("time", "")
            if time_label:
                badge = slide.shapes.add_shape(1, Inches(0.7), Inches(0.45), Inches(1.6), Inches(0.45))
                badge.fill.solid()
                badge.fill.fore_color.rgb = RGBColor(0xDB, 0xEA, 0xFE)
                badge.line.fill.background()
                add_textbox(slide, Inches(0.7), Inches(0.42), Inches(1.6), Inches(0.5),
                            time_label, size=13, bold=True, color=BLUE_DARK, align=PP_ALIGN.CENTER)

            add_textbox(slide, Inches(0.7), Inches(0.95), Inches(11.5), Inches(0.9),
                        data["title"], size=30, bold=True, color=BLUE_DARK)
            line = slide.shapes.add_shape(1, Inches(0.7), Inches(1.85), Inches(2.5), Inches(0.06))
            line.fill.solid()
            line.fill.fore_color.rgb = PINK
            line.line.fill.background()

            tf = add_textbox(slide, Inches(0.9), Inches(2.1), Inches(11.2), Inches(4.8), "", size=17, color=SLATE)
            add_bullets(tf, data["bullets"], size=17, color=SLATE, spacing=Pt(10))

        # 발표자 노트 (수업 원고)
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = data.get("notes", "")

        # 슬라이드 번호
        idx = len(prs.slides)
        add_textbox(slide, Inches(12.3), Inches(7.05), Inches(0.8), Inches(0.35),
                    str(idx), size=11, color=SLATE_LIGHT, align=PP_ALIGN.RIGHT)

    prs.save(PPTX_PATH)
    print(f"PPTX saved: {PPTX_PATH}")


def build_pdf():
    ensure_font()
    pdfmetrics.registerFont(TTFont("NotoKR", str(FONT_PATH)))
    page_w, page_h = landscape((297 * mm, 210 * mm))  # A4 landscape
    c = canvas.Canvas(str(PDF_PATH), pagesize=(page_w, page_h))

    for i, data in enumerate(SLIDES, 1):
        slide_type = data.get("type", "content")

        if slide_type == "title":
            c.setFillColor(colors.HexColor("#1E40AF"))
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#F472B6"))
            c.rect(0, 0, page_w, 8, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont("NotoKR", 28)
            c.drawCentredString(page_w / 2, page_h - 80, data["title"])
            c.setFont("NotoKR", 14)
            c.setFillColor(colors.HexColor("#BFDBFE"))
            c.drawCentredString(page_w / 2, page_h - 115, data.get("subtitle", ""))
            c.setFillColor(colors.HexColor("#E2E8F0"))
            c.setFont("NotoKR", 12)
            y = page_h - 170
            for b in data["bullets"]:
                c.drawCentredString(page_w / 2, y, b)
                y -= 22

        elif slide_type == "closing":
            c.setFillColor(colors.HexColor("#0F172A"))
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#F472B6"))
            c.rect(0, page_h - 8, page_w, 8, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#93C5FD"))
            c.setFont("NotoKR", 22)
            c.drawString(40, page_h - 55, data["title"])
            c.setFillColor(colors.HexColor("#CBD5E1"))
            c.setFont("NotoKR", 12)
            y = page_h - 100
            for b in data["bullets"]:
                c.drawString(55, y, f"•  {b}")
                y -= 24

        else:
            c.setFillColor(colors.white)
            c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#3B82F6"))
            c.rect(0, page_h - 10, page_w, 10, fill=1, stroke=0)

            time_label = data.get("time", "")
            if time_label:
                c.setFillColor(colors.HexColor("#DBEAFE"))
                c.roundRect(35, page_h - 48, 70, 20, 4, fill=1, stroke=0)
                c.setFillColor(colors.HexColor("#1E40AF"))
                c.setFont("NotoKR", 9)
                c.drawCentredString(70, page_h - 42, time_label)

            c.setFillColor(colors.HexColor("#1E40AF"))
            c.setFont("NotoKR", 20)
            c.drawString(40, page_h - 75, data["title"])
            c.setFillColor(colors.HexColor("#F472B6"))
            c.rect(40, page_h - 88, 80, 3, fill=1, stroke=0)

            c.setFillColor(colors.HexColor("#334155"))
            c.setFont("NotoKR", 11)
            y = page_h - 115
            for b in data["bullets"]:
                # 긴 줄 자동 줄바꿈
                max_w = page_w - 90
                words, line, lines = b.replace("• ", ""), "", []
                for ch in words:
                    test = line + ch
                    if c.stringWidth(test, "NotoKR", 11) < max_w:
                        line = test
                    else:
                        lines.append(line)
                        line = ch
                if line:
                    lines.append(line)
                for ln in lines:
                    c.drawString(55, y, f"•  {ln}")
                    y -= 18
                y -= 4

        # 발표자 노트 (하단 작게)
        notes = data.get("notes", "")
        if notes:
            c.setFillColor(colors.HexColor("#94A3B8"))
            c.setFont("NotoKR", 7)
            note_preview = notes[:120] + ("..." if len(notes) > 120 else "")
            c.drawString(40, 18, f"[발표자 노트] {note_preview}")

        c.setFillColor(colors.HexColor("#94A3B8"))
        c.setFont("NotoKR", 9)
        c.drawRightString(page_w - 30, 18, f"{i} / {len(SLIDES)}")
        c.showPage()

    c.save()
    print(f"PDF saved: {PDF_PATH}")


if __name__ == "__main__":
    build_pptx()
    build_pdf()
    print("Done.")
