"""합리적인 선택 도우기
실행: streamlit run app.py
배포: GitHub에 app.py와 requirements.txt를 올린 후 Streamlit Community Cloud 연결.
배포 주소를 QR로 공유하면 설치 없이 휴대폰 브라우저에서 사용할 수 있습니다.
"""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from io import BytesIO
import html
import random
import time
import base64
from urllib.parse import urlparse

import qrcode
import streamlit as st


LOGO_BASE64 = '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UUUUAGKSlooASilooAKKKT6UALSdqWkoAKKKO1ABRRRQAUUtFACUnelo7UAH0opaKAEopaKACiiigAoooNABRS0lACUdqWkoAWkNL2ooASjvRR3oAWiiigAoo7UUAFHWiigAooooAUZoNJRQAUlKaO9ACUUtFACUtJRQAUUUvegAHFHb3oooAKDR2ooASloooAKKO1FABRRRQAUUUUAFFJS0AFFFFABRRRQAUn40tHegBKWiigApKWigBKXtRSZoAWik6UtABikpaO9ACUtJQKAFooooAKKKKACiiigAo70UtACUUUUAJRS0lABSUtGKAFooooAKKKKACiiigAoopKAFopKWgAzSUtJQAtFJRQAtJRRQAUtJS0AHaiiigApPxoooAWik7UtABRRRQAUcUUUAFBoooAKKKSgBaKKKACkpaSgBRR1NFFABRQaSgBaKKKACkpaSgA70ooooAKKKKAENFLRQAd6KTvRQAtFJS0AFFJS0AGaKSloAKKKKACg0UUAFJ3FLSUAFLR3ooAKKOKKACiiigAooooASjvS96KACkpaKAEo70tJQAtJS0UAJS0lFABRzS0lAC0lLSUAFFJS0AFFHaigApaKKACjvRRQAdetGKKKACiiigAooooAKKKKAEooooAKO9FFABzRRRQAZooooAWikooAWiikoAKKWigAooooASiijtQAtFJS0AFJRS0AFJ3o/GigBaT6UUZ5oAXrRRRQAUUUnWgApaSloAKKKKACijtR26UAFH1opKADtS0UUAFJS0lABmlpKO9AC0UlLmgBKOtFHagAoopaAEpaPrRQAUUUUAFFFFACUUUv40AFFJS0ABooooAKKKKACkpaSgAooooAKKKO9ABRRRQAdqWkooAKO9FLQAUd6KKACiijvQAdKSiloAQUtJS0AFJS0lABRS0UAFHeiigBKKO9GaAClFFFABRRRQACiiigAo+tHajvQAUUUUAFFFFABRRRQAlFFFAC0lLRQAlFLRQAneloooAKSlpKAFooooAKKKKACiiigAoopKAFooooAKKKKACkopaAEzRRRQAUUfjRQAUUUUAFFFFAB3paSl7UAFJS0UAFFFFABRRRQAUUUUAFFFFACUUtJ3oAKKKWgBKKO1FAC0UUUAFFFFABRRRQAUUUUAFFFFABRRRQAUZopO9ABmlpKWgAooooAKKSloAO/SikpaADFFFFABRRRQAUUYxRQAUUUUAFH40lL2oASiiloAKKKKACiikoAWiiigBKKWkxQAUtJ2ooAOgopaKACig0d6ACiiigAoozRQAUUUfWgAo4oooAKKKikuIozhm59BzSbSAloqv8AbIPVvypyXMLtgNg+/FLmXcdmS0Gij2piClpOtLTAKKO9FABRRRQAUUUUAFFFJ2oAWkpaSgBaKKO9ABSUtJQAUtJRQAtFFFABSUtFACUYopaADtRRSUALRSd6WgAooooAKSlpM80ALSUtGKAEo70UUALRRRQAUlLSUAApaKKAAUUCl7UAJRRR2oAKO9FHfgUAFAoooAKKKKACiiigAooFFAB7UUUUAQ3MpigyOp4FZpOASTV+8QtAGH8JzU3hn+w/+E00pvE8kyaKt1G98YULuYQwLqoHUkAj8a56u5rDY6Pxn8O38I+BtG14ast7Pc7Y9SsxDsOmzvClxFEzZO7dFIDnAwVYY4rL8eeFP+EJ8e3fhr7d9u+zxQSef5fl7vNhSXG3JxjfjrzjNdhq3xcm8a+HfGuj+MINPgi1ZRf6c1hpcELx3sUmYhI8aKzqYnlj3MTjINc58U/Eml+Lfipf6/ozyvZTw2qIZU2NmO2jjbI/3kasVfqaOxztnKXjKNyV6fSrHeqlkpAZ+x4FW+K64fDqYS3AUdqTvS1ZIUUZozQAtFJRmgBaKTtxRmgA74opO9FAC0d6SigBaKTNFADqSkooAXPPWiko7UgHUU2lGcUwFpKO1JQAveiikoAdSUUdaACj8aTvR3oAXNFHWigAopKWgBaSgUZzQAUfhRSUAO7UUnGaKAFpKM0lADqSkzSigBaTNFAoAXiikozQAtFJR2oAO9FH1pKAHUU3NLmgAopKKAFoozQaAClpBRQAdRg81VkslJzG232PNW6Q0nFPcabWxS+wv/z0X8qctkA2ZHyPQVb9qTNT7OI+dgqhUCqMAdBR3oozzVkn/9k='

def compare_choices(choices: list[dict], won_per_point: int) -> list[dict]:
    """편익=S×환산액, 암묵적 비용=max(다른 대안의 편익-C).
    서로 배타적인 대안 중 하나를 고르는 상황, 공통 환산액을 가정합니다.
    명시적 비용 및 환산액은 음수가 아닌 원 단위 정수입니다.
    """
    if len(choices) < 2:
        raise ValueError("선택지는 최소 2개가 필요합니다.")
    if not isinstance(won_per_point, int) or won_per_point < 1:
        raise ValueError("만족도 1점의 금액은 1원 이상의 정수여야 합니다.")
    rows = []
    for index, choice in enumerate(choices):
        cost = choice["cost"]
        satisfaction = Decimal(str(choice["satisfaction"]))
        if not isinstance(cost, int) or cost < 0 or not 1 <= satisfaction <= 10:
            raise ValueError("비용은 0원 이상의 정수, 만족도는 1~10이어야 합니다.")
        benefit = int((satisfaction * won_per_point).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        net = benefit - cost
        rows.append({"index": index, "name": str(choice["name"]).strip() or f"선택 {index + 1}",
                     "cost": cost, "satisfaction": float(satisfaction),
                     "net_benefit": net, "benefit": benefit})
    for row in rows:
        implicit = max(other["net_benefit"] for other in rows if other["index"] != row["index"])
        row["implicit_cost"] = implicit
        row["opportunity_cost"] = row["cost"] + implicit
        row["economic_profit"] = row["benefit"] - row["opportunity_cost"]
    return rows


def money(value: int) -> str:
    """휴대폰에서도 줄바꿈을 줄이는 정확한 원 단위 표시."""
    return f"{value:,}원"


def main() -> None:
    st.set_page_config(page_title="합리적 선택 도우미!", page_icon=BytesIO(base64.b64decode(LOGO_BASE64)), layout="centered", initial_sidebar_state="collapsed")
    st.markdown("""
<style>
.stApp {background:#F7F9FC; color:#18243B;}
.block-container {max-width:600px; padding:0.65rem 0.7rem 0.65rem !important;}
header[data-testid="stHeader"] {height:0; background:transparent;}
[data-testid="stToolbar"], #MainMenu, footer {display:none;}
/* 각 출력 영역에 실제 높이와 간격을 확보해 다음 입력/카드와 겹치지 않게 합니다. */
/* Streamlit 기본 블록 간격을 유지합니다. 전역 gap 축소는 하지 않습니다. */
[data-testid="stMarkdownContainer"] {display:flow-root; height:auto; overflow:visible;}
[data-testid="stMarkdownContainer"] .hero,
[data-testid="stMarkdownContainer"] .sub,
[data-testid="stMarkdownContainer"] .colhead,
[data-testid="stMarkdownContainer"] .winner,
[data-testid="stMarkdownContainer"] .result,
[data-testid="stMarkdownContainer"] .note {box-sizing:border-box; position:relative; height:auto;}
[data-testid="stMarkdownContainer"] .colhead {padding:2px 0 4px; line-height:1.5; min-height:23px;}
[data-testid="stMarkdownContainer"] .winner,
[data-testid="stMarkdownContainer"] .result {margin:0;}
[data-testid="stMarkdownContainer"] .note {margin:0; padding:3px 0;}
[data-testid="stMarkdownContainer"] .metric {line-height:1.5;}
[data-testid="stMarkdownContainer"] .metric strong {line-height:1.5;}
[data-testid="stMarkdownContainer"] .sub {line-height:1.5;}
[data-testid="stMarkdownContainer"] .hero + .sub {padding-top:3px;}
[data-testid="stHorizontalBlock"] {flex-wrap:nowrap !important; gap:0.35rem !important;}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {min-width:0 !important; width:unset !important; flex-shrink:1 !important;}
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input {font-size:14px; padding-left:7px; padding-right:3px; min-height:36px;}
[data-testid="stNumberInput"] button {display:none;}
[data-testid="stPopover"] button {min-height:36px; padding:0.2rem 0.6rem;}
[data-testid="stTextInput"], [data-testid="stNumberInput"] {min-width:0;}
.hero {font-size:22px; font-weight:850; letter-spacing:-0.8px; line-height:1.25; padding-top:3px;}
.sub {font-size:11px; color:#607087; line-height:1.35;}
.colhead {font-size:11px; color:#607087; white-space:nowrap;}
.winner {background:#E7F5EF; color:#145C42; border:1px solid #BFE4D4; border-radius:12px; padding:8px 10px; font-size:14px; line-height:1.35; margin-top:4px;}
.result {background:white; border:1px solid #E1E7EF; border-radius:10px; padding:6px 9px; margin-top:4px;}
.result-top {display:flex; justify-content:space-between; gap:6px; font-size:12px; line-height:1.3;}
.choice-name {overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:55%; font-weight:700;}
.metrics {display:grid; grid-template-columns:1fr 1fr 1fr; gap:3px; margin-top:4px;}
.metric {font-size:10px; color:#617088; white-space:nowrap;}
.metric strong {display:block; font-size:12px; color:#18243B; font-weight:650; letter-spacing:-0.3px;}
.note {font-size:10px; color:#68758A; line-height:1.35; margin-top:5px;}
@media(max-width:370px) {.metric strong{font-size:10px;} .hero{font-size:20px;}}
</style>
""", unsafe_allow_html=True)

    # 제목과 안내문을 별도 기본 위젯으로 렌더링해 실제 높이를 확보합니다.
    # 첫 접속에만 로고와 슬로건을 1.5초 표시합니다.
    if not st.session_state.get("intro_shown", False):
        intro = st.empty()
        intro.markdown(
            '<div style="min-height:75vh;display:flex;flex-direction:column;'
            'align-items:center;justify-content:center;text-align:center;gap:18px;">'
            f'<img src="data:image/jpeg;base64,{LOGO_BASE64}" alt="SW 로고" '
            'style="width:min(68vw,280px);height:auto;border-radius:24px;">'
            '<div style="font-size:clamp(17px,4.8vw,24px);font-weight:700;'
            'line-height:1.6;overflow-wrap:anywhere;">'
            'smart way-합리적 선택, 당신 손 안에</div></div>',
            unsafe_allow_html=True,
        )
        time.sleep(1.5)
        intro.empty()
        st.session_state["intro_shown"] = True
    st.caption("비용과 만족을 입력하면, 비교는 바로 아래에.")
    with st.expander("⚙ 설정 · 선택지 수 / 1점당 금액 / QR", expanded=False):
        st.markdown("**비교 설정**")
        count = st.selectbox("선택지 수", [2, 3, 4], index=0, key="choice_count")
        rate = int(st.number_input("만족도가 1점 높아지면 최대 얼마까지 더 낼 수 있나요? (원)", min_value=1, max_value=1_000_000_000, value=5000, step=1000, key="point_rate"))
        st.caption("모든 선택지에 같은 환산액을 적용합니다. 원 단위 정수로 계산합니다.")
        st.markdown("**QR로 공유**")
        app_url = st.text_input("배포된 앱 주소", placeholder="https://your-app.streamlit.app", key="share_url").strip()
        if app_url:
            parsed = urlparse(app_url)
            if parsed.scheme in ("https", "http") and parsed.hostname and not parsed.username and not parsed.password:
                qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=4)
                qr.add_data(app_url)
                qr.make(fit=True)
                buf = BytesIO()
                qr.make_image(fill_color="#18243B", back_color="white").save(buf, format="PNG")
                image = buf.getvalue()
                st.image(image, width=180)
                st.download_button("QR 이미지 다운로드", image, file_name="choice-app-qr.png", mime="image/png")
                st.caption("QR은 앱 접속용입니다. 입력한 선택지는 QR에 포함되지 않습니다.")
            else:
                st.warning("http:// 또는 https://로 시작하는 올바른 배포 주소를 입력하세요.")
        else:
            st.caption("GitHub에 두 파일을 올리고 Streamlit Community Cloud에서 app.py를 배포한 뒤, 공개 주소를 입력하세요.")

    a, b, c = st.columns([1.15, 1.35, 1])
    a.markdown('<div class="colhead">선택지</div>', unsafe_allow_html=True)
    b.markdown('<div class="colhead">명시적 비용 · 원</div>', unsafe_allow_html=True)
    c.markdown('<div class="colhead">만족 · 1~10</div>', unsafe_allow_html=True)
    choices = []
    for i in range(count):
        a, b, c = st.columns([1.15, 1.35, 1])
        with a:
            name = st.text_input(f"선택지 {i + 1} 이름", value=f"선택 {chr(65 + i)}", key=f"name_{i}", max_chars=20, label_visibility="collapsed")
        with b:
            cost = int(st.number_input(f"선택지 {i + 1} 비용 (원)", min_value=0, max_value=1_000_000_000, value=10000 + 5000 * i, step=1000, key=f"cost_{i}", label_visibility="collapsed"))
        with c:
            satisfaction = int(st.number_input(f"선택지 {i + 1} 만족도", min_value=1, max_value=10, value=min(7 + i, 10), step=1, key=f"satisfaction_{i}", label_visibility="collapsed"))
        choices.append({"name": name, "cost": cost, "satisfaction": satisfaction})

    rows = compare_choices(choices, rate)
    best = max(row["economic_profit"] for row in rows)
    winners = [row for row in rows if row["economic_profit"] == best]
    names = ", ".join(html.escape(row["name"]) for row in winners)
    title_text = "공동 추천" if len(winners) > 1 else "추천"
    st.markdown(f'<div class="winner"><b>{title_text} · {names}</b><div class="sub">만족도 1점 = {money(rate)} · 순편익(편익 − 비용) 기준</div></div>', unsafe_allow_html=True)
    if len(winners) > 1:
        st.caption("입력 기준상 똑같이 합리적이에요. 고민이 계속되면 동점 선택지 중 하나를 뽑아보세요.")
        signature = tuple((r["name"], r["cost"], r["satisfaction"], rate) for r in rows)
        if st.session_state.get("draw_signature") != signature:
            st.session_state.pop("draw_index", None)
            st.session_state["draw_signature"] = signature
        if st.button("🎲 고민 끝내기 · 하나 뽑기", use_container_width=True):
            st.session_state["draw_index"] = random.choice(winners)["index"]
        if "draw_index" in st.session_state:
            picked = rows[st.session_state["draw_index"]]
            st.success(f"오늘은 {picked['name']}! 경제성이 같아서 무작위로 골랐어요.")
    else:
        winner = winners[0]
        runner = max((r for r in rows if r["index"] != winner["index"]), key=lambda r: r["net_benefit"])
        gap = winner["net_benefit"] - runner["net_benefit"]
        st.caption(f"{runner['name']}보다 순편익이 {money(gap)} 높아요. 비용과 추가 만족의 가치를 함께 비교했어요.")
    for row in rows:
        name = html.escape(row["name"])
        profit = row["economic_profit"]
        prefix = "+" if profit > 0 else ""
        mark = " ✓" if row["economic_profit"] == best else ""
        st.markdown(f'''<div class="result">
<div class="result-top"><span class="choice-name">{name}{mark}</span><span>이윤 {prefix}{money(profit)}</span></div>
<div class="metrics"><div class="metric">편익<strong>{money(row['benefit'])}</strong></div><div class="metric">암묵적 비용<strong>{money(row['implicit_cost'])}</strong></div><div class="metric">기회비용<strong>{money(row['opportunity_cost'])}</strong></div></div></div>''', unsafe_allow_html=True)

    st.caption("순편익 = 만족도 × 1점당 추가 지불 의향 − 명시적 비용. 금액 설정에 따라 추천이 달라집니다.")
    with st.popover("ⓘ 계산 기준", use_container_width=True):
        st.markdown("""**하나만 선택하는 상호 배타적인 대안**을 비교합니다.

- 환산 만족 = 만족도 × 1점의 금액
- **편익 = 환산 만족**
- 순편익 = 편익 − 명시적 비용
- **암묵적 비용 = 포기하는 다른 선택지 중 가장 큰 순편익**
- **기회비용 = 명시적 비용 + 암묵적 비용**
- 경제적 이윤 = 편익 − 기회비용

암묵적 비용은 나머지 대안의 합이 아니라 **최선 대안 하나**의 순편익입니다. 동점은 공동 추천하며, 원하면 동점 대안 중 하나를 무작위로 뽑습니다. 시간·위험·예산 제약은 별도로 고려하지 않습니다.

이 앱은 입력한 선택지 중 하나를 반드시 고르는 상황을 비교하며, ‘아무것도 선택하지 않기’는 포함하지 않습니다. 따라서 모든 순편익이 음수이면 암묵적 비용도 음수일 수 있습니다. 만족도 환산은 개인의 주관적인 비교 기준이며 실제 현금 수익을 의미하지 않습니다.

**모바일 안내:** 기본 2개, 최대 4개를 압축 배치했습니다. 아주 작은 화면·가로 모드·확대 글꼴·키보드 표시 중에는 스크롤이 생길 수 있습니다. 설정은 화면 안에서 펼쳐 바꿀 수 있고, 설명은 팝업으로 열립니다. 설정을 접으면 더 컴팩트하게 비교할 수 있습니다.

**배포:** GitHub 저장소 루트에 `app.py`, `requirements.txt` → Streamlit Community Cloud에서 해당 저장소와 `app.py` 선택 → 배포 주소를 설정에 입력 → QR 다운로드. GitHub 자체는 Python 앱 실행 서버가 아니므로 Streamlit 배포가 필요합니다.

입력값은 서버의 현재 Streamlit 세션에서 처리되며, 앱에서 별도 파일이나 데이터베이스로 저장하지 않습니다. 새 접속 시 기본값으로 시작합니다.
""")


if __name__ == "__main__":
    main()
