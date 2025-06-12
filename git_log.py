import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
from typing import Optional


def ensure_git_repo(path: Path):
    if not (path / ".git").exists():
        print(f"❌ '{path}' 는 Git 저장소가 아닙니다.")
        sys.exit(1)


def month_range(start: datetime, end: datetime):
    """start ~ end 까지 월 단위 반복 생성"""
    current = start
    while current <= end:
        yield current
        # 다음 달 1일로 이동
        next_month = current.replace(day=28) + timedelta(days=4)
        current = next_month.replace(day=1)


def parse_submodules(repo_path: Path):
    gitmodules_path = repo_path / ".gitmodules"
    if not gitmodules_path.exists():
        return []
    submodules = []
    with open(gitmodules_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("path = "):
                submodules.append(line.split("=", 1)[1].strip())
    return submodules


def generate_git_logs(
    repo_path: Path,
    start_year: int = 2021,
    start_month: int = 8,
    output_dir: Optional[Path] = None,
    repo_label: Optional[str] = None,
    main_repo_path: Optional[Path] = None,
    main_project_name: Optional[str] = None,
):
    if main_repo_path is None:
        main_repo_path = repo_path
    if main_project_name is None:
        main_project_name = main_repo_path.name
    if output_dir is None:
        output_dir = main_repo_path / f"{main_project_name}_git_logs_by_month"
    output_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(repo_path)
    ensure_git_repo(repo_path)

    start_date = datetime(start_year, start_month, 1)
    end_date = datetime.now()

    label = repo_label if repo_label else repo_path.name
    # 파일명에 디렉토리 구분자가 들어가지 않도록 치환
    safe_label = label.replace("/", "_").replace("\\", "_")

    for dt in month_range(start_date, end_date):
        since = dt.strftime("%Y-%m-%d")
        until = (dt.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(
            seconds=1
        )
        until_str = until.strftime("%Y-%m-%d")

        filename = f"{safe_label}_git_log_{dt.strftime('%Y-%m')}.txt"
        filepath = output_dir / filename

        print(f"📦 {dt.strftime('%Y-%m')} 로그 생성 중... ({safe_label})")

        git_log_cmd = [
            "git",
            "log",
            f"--since={since}",
            f"--until={until_str}",
            "--pretty=format:===%ncommit:%H%nAuthor:%an%nEmail:%ae%nDate:%ad%nMessage:%s%n",
            "--patch",
            "--date=iso",
        ]

        # 한글 및 인코딩 깨짐 방지: 바이너리로 받아 그대로 파일에 저장
        result = subprocess.run(git_log_cmd, stdout=subprocess.PIPE, check=True)
        with open(filepath, "wb") as f:
            f.write(result.stdout)

    print(f"✅ 완료! {output_dir} 에 월별 로그가 저장되었습니다.")

    # 서브모듈 처리
    for submodule in parse_submodules(repo_path):
        sub_path = repo_path / submodule
        if sub_path.exists():
            generate_git_logs(
                sub_path,
                start_year,
                start_month,
                output_dir=output_dir,
                repo_label=submodule,
                main_repo_path=main_repo_path,
                main_project_name=main_project_name,
            )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python git_log_split_by_month.py <git_repo_path>")
        sys.exit(1)

    repo_path = Path(sys.argv[1]).resolve()
    generate_git_logs(repo_path)
