"""
D-Day Counter - Streamlit 웹 앱
KPI 카드, 차트, 이벤트 관리 UI를 제공합니다.
"""

from __future__ import annotations

import datetime

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app.dday_core import sort_events_by_proximity
from app.models import DdayEventCreate, EventCategory
from app.storage import add_event, delete_event, load_events

# ───────── 페이지 설정 ─────────
st.set_page_config(
    page_title="📅 D-Day Counter",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ───────── 커스텀 CSS ─────────
st.markdown(
    """
    <style>
    /* 전체 배경 */
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }

    /* KPI 카드 */
    .kpi-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-4px); }
    .kpi-value { font-size: 2.4rem; font-weight: 800; color: #00d4ff; }
    .kpi-label { font-size: 0.95rem; color: rgba(255,255,255,0.7); margin-top: 4px; }

    /* 이벤트 카드 */
    .event-card {
        background: rgba(255,255,255,0.06);
        border-left: 4px solid #00d4ff;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }
    .event-card.past { border-left-color: #888; opacity: 0.65; }
    .event-card.today { border-left-color: #ff6ec7; }

    /* 사이드바 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e, #16213e);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ───────── 유틸 ─────────


def kpi_card(label: str, value, color: str = "#00d4ff") -> str:
    return f"""
    <div class="kpi-card">
        <div class="kpi-value" style="color:{color}">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """


# ───────── 사이드바: 이벤트 추가 ─────────
with st.sidebar:
    st.header("➕ 새 이벤트 등록")
    with st.form("add_event_form", clear_on_submit=True):
        title = st.text_input("제목", max_chars=100, placeholder="예: 기말 시험")
        target_date = st.date_input("목표 날짜", value=datetime.date.today() + datetime.timedelta(days=7))
        category = st.selectbox("카테고리", [c.value for c in EventCategory])
        memo = st.text_area("메모 (선택)", max_chars=200)
        submitted = st.form_submit_button("등록")
        if submitted and title:
            cat_enum = EventCategory(category)
            add_event(DdayEventCreate(title=title, target_date=target_date, category=cat_enum, memo=memo or None))
            st.success(f"✅ '{title}' 이벤트가 등록되었습니다!")
            st.rerun()

    st.divider()
    st.caption("📅 D-Day Counter v1.0")

# ───────── 메인 ─────────
st.title("📅 D-Day Counter Dashboard")
st.caption(f"오늘: {datetime.date.today().isoformat()}")

events = load_events()
responses = sort_events_by_proximity(events) if events else []

# KPI 카드 영역
total = len(responses)
upcoming = sum(1 for r in responses if r.d_day >= 0)
past = total - upcoming
today_count = sum(1 for r in responses if r.d_day == 0)
nearest = responses[0] if responses else None

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(kpi_card("전체 이벤트", total, "#00d4ff"), unsafe_allow_html=True)
with col2:
    st.markdown(kpi_card("다가오는 일정", upcoming, "#00e676"), unsafe_allow_html=True)
with col3:
    st.markdown(kpi_card("지난 일정", past, "#ff9800"), unsafe_allow_html=True)
with col4:
    nearest_label = nearest.d_day_label if nearest else "-"
    st.markdown(kpi_card("가장 가까운 D-Day", nearest_label, "#ff6ec7"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if not events:
    st.info("📭 등록된 이벤트가 없습니다. 사이드바에서 새 이벤트를 추가해 주세요!")
else:
    # ───────── 차트 ─────────
    tab_list, tab_chart = st.tabs(["📋 이벤트 목록", "📊 시각화"])

    with tab_list:
        for resp in responses:
            card_class = "event-card"
            if resp.d_day == 0:
                card_class += " today"
            elif resp.d_day < 0:
                card_class += " past"

            col_info, col_action = st.columns([5, 1])
            with col_info:
                st.markdown(
                    f"""<div class="{card_class}">
                        <strong>{resp.title}</strong>
                        &nbsp; <span style="color:#aaa">[{resp.category.value}]</span><br>
                        📆 {resp.target_date.isoformat()} &nbsp;|&nbsp;
                        <span style="font-weight:700; color:{'#ff6ec7' if resp.d_day <= 3 and resp.d_day >= 0 else '#00d4ff'}">{resp.d_day_label}</span>
                        {f'<br>📝 {resp.memo}' if resp.memo else ''}
                    </div>""",
                    unsafe_allow_html=True,
                )
            with col_action:
                if st.button("🗑️", key=f"del_{resp.id}", help="삭제"):
                    delete_event(resp.id)
                    st.rerun()

    with tab_chart:
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            # 카테고리별 분포 도넛 차트
            cat_counts = {}
            for r in responses:
                cat_counts[r.category.value] = cat_counts.get(r.category.value, 0) + 1
            if cat_counts:
                fig_donut = go.Figure(
                    data=[
                        go.Pie(
                            labels=list(cat_counts.keys()),
                            values=list(cat_counts.values()),
                            hole=0.5,
                            marker=dict(colors=px.colors.qualitative.Set2),
                        )
                    ]
                )
                fig_donut.update_layout(
                    title="카테고리별 분포",
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white"),
                    height=350,
                )
                st.plotly_chart(fig_donut, width="stretch")

        with chart_col2:
            # D-Day 바 차트 (미래 이벤트만)
            future = [r for r in responses if r.d_day >= 0]
            if future:
                fig_bar = go.Figure(
                    data=[
                        go.Bar(
                            x=[r.title for r in future],
                            y=[r.d_day for r in future],
                            marker_color=[
                                "#ff6ec7" if r.d_day <= 3 else "#00d4ff" for r in future
                            ],
                            text=[r.d_day_label for r in future],
                            textposition="auto",
                        )
                    ]
                )
                fig_bar.update_layout(
                    title="다가오는 일정 (남은 일수)",
                    xaxis_title="이벤트",
                    yaxis_title="남은 일수",
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white"),
                    height=350,
                )
                st.plotly_chart(fig_bar, width="stretch")
            else:
                st.info("다가오는 일정이 없습니다.")

        # 타임라인 (전체)
        if responses:
            fig_timeline = go.Figure()
            for r in responses:
                color = "#ff6ec7" if r.d_day <= 3 and r.d_day >= 0 else ("#888" if r.d_day < 0 else "#00d4ff")
                fig_timeline.add_trace(
                    go.Scatter(
                        x=[r.target_date],
                        y=[r.title],
                        mode="markers+text",
                        marker=dict(size=14, color=color),
                        text=[r.d_day_label],
                        textposition="middle right",
                        name=r.title,
                        showlegend=False,
                    )
                )
            # 오늘 선
            fig_timeline.add_shape(
                type="line",
                x0=datetime.date.today().isoformat(),
                x1=datetime.date.today().isoformat(),
                y0=0, y1=1,
                yref="paper",
                line=dict(dash="dash", color="#ff6ec7"),
            )
            fig_timeline.add_annotation(
                x=datetime.date.today().isoformat(),
                y=1, yref="paper",
                text="오늘",
                showarrow=False,
                font=dict(color="#ff6ec7"),
            )
            fig_timeline.update_layout(
                title="📅 이벤트 타임라인",
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                height=300,
                xaxis_title="날짜",
            )
            st.plotly_chart(fig_timeline, width="stretch")
