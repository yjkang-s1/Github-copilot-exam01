"""
D-Day Counter - Rich 터미널 대시보드
터미널에서 D-Day 이벤트를 아름다운 테이블/패널로 표시합니다.
"""

from __future__ import annotations

from datetime import date

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from app.dday_core import sort_events_by_proximity
from app.storage import load_events

console = Console()


def _get_dday_color(d_day: int) -> str:
    """D-Day 값에 따라 색상을 반환합니다."""
    if d_day == 0:
        return "bold magenta"
    elif 1 <= d_day <= 3:
        return "bold red"
    elif 4 <= d_day <= 7:
        return "bold yellow"
    elif d_day > 7:
        return "green"
    else:
        return "dim"


def render_dashboard() -> None:
    """터미널 D-Day 대시보드를 렌더링합니다."""
    events = load_events()
    if not events:
        console.print(
            Panel(
                "[yellow]등록된 이벤트가 없습니다. 먼저 이벤트를 추가해 주세요![/yellow]",
                title="📅 D-Day Counter",
                border_style="blue",
            )
        )
        return

    sorted_responses = sort_events_by_proximity(events)

    # 요약 KPI
    total = len(sorted_responses)
    upcoming = sum(1 for r in sorted_responses if r.d_day >= 0)
    today_count = sum(1 for r in sorted_responses if r.d_day == 0)

    kpi_text = (
        f"[bold cyan]전체:[/bold cyan] {total}개  |  "
        f"[bold green]다가오는 일정:[/bold green] {upcoming}개  |  "
        f"[bold magenta]오늘 D-Day:[/bold magenta] {today_count}개"
    )
    console.print(Panel(kpi_text, title="📊 요약", border_style="bright_blue"))

    # 테이블
    table = Table(
        title=f"📅 D-Day Dashboard  ({date.today().isoformat()})",
        show_header=True,
        header_style="bold bright_white on blue",
        border_style="bright_blue",
        show_lines=True,
    )
    table.add_column("#", style="dim", width=4, justify="center")
    table.add_column("제목", min_width=15)
    table.add_column("카테고리", width=10, justify="center")
    table.add_column("목표일", width=12, justify="center")
    table.add_column("D-Day", width=16, justify="center")
    table.add_column("메모", max_width=25)

    for idx, resp in enumerate(sorted_responses, 1):
        color = _get_dday_color(resp.d_day)
        dday_text = Text(resp.d_day_label, style=color)
        table.add_row(
            str(idx),
            resp.title,
            resp.category.value,
            resp.target_date.isoformat(),
            dday_text,
            resp.memo or "-",
        )

    console.print(table)


if __name__ == "__main__":
    render_dashboard()
