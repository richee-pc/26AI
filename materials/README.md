# AI 실습 연수 수업 원고 자료

중학교 선생님 대상 **50분 생성형 AI 실습 연수**용 슬라이드입니다.

## 파일

| 파일 | 설명 |
|------|------|
| `AI_lecture_script.pptx` | PowerPoint 원본 (10매, 발표자 노트 포함) |
| `AI_lecture_script.pdf` | PDF 출력물 (배포·인쇄용) |
| `generate_lecture_slides.py` | PPT·PDF 재생성 스크립트 |

## 슬라이드 구성 (10매)

1. 표지 — AI와 함께 스마트하게 일하기
2. 오늘의 목표 & 50분 로드맵
3. 처음이신가요? 3분 빠른 시작
4. 광주아이온(AI-ON) 마스터하기
5. NotebookLM 활용
6. 부서별·담임 업무 활용
7. Gemini 심화
8. 워크스페이스+ 심화 팁
9. 상황별 활용 가이드 (강의 후)
10. 마무리 & 주의사항

각 슬라이드 **발표자 노트**에 수업 원고(멘트)가 들어 있습니다. PowerPoint에서 [보기 → 발표자 노트]로 확인하세요.

## 재생성 방법

```bash
pip install python-pptx reportlab
cd materials
python3 generate_lecture_slides.py
```

PDF 한글 폰트는 최초 실행 시 `fonts/NotoSansKR.ttf`가 필요합니다.
