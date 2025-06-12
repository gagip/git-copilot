import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

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

def generate_git_logs(repo_path: Path, start_year: int = 2021, start_month: int = 8):
    os.chdir(repo_path)
    ensure_git_repo(repo_path)

    output_dir = repo_path / "git_logs_by_month"
    output_dir.mkdir(exist_ok=True)

    start_date = datetime(start_year, start_month, 1)
    end_date = datetime.now()

    for dt in month_range(start_date, end_date):
        since = dt.strftime("%Y-%m-%d")
        until = (dt.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(seconds=1)
        until_str = until.strftime("%Y-%m-%d")

        filename = f"git_log_{dt.strftime('%Y-%m')}.txt"
        filepath = output_dir / filename

        print(f"📦 {dt.strftime('%Y-%m')} 로그 생성 중...")

        git_log_cmd = [
            "git", "log",
            f"--since={since}",
            f"--until={until_str}",
            '--pretty=format:===%ncommit:%H%nAuthor:%an%nEmail:%ae%nDate:%ad%nMessage:%s%n',
            '--patch',
            '--date=iso'
        ]

        # 한글 깨짐 방지: subprocess에서 출력을 직접 받아 파일에 utf-8로 저장
        result = subprocess.run(git_log_cmd, capture_output=True, encoding="utf-8", check=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result.stdout)

    print(f"✅ 완료! {output_dir} 에 월별 로그가 저장되었습니다.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python git_log_split_by_month.py <git_repo_path>")
        sys.exit(1)

    repo_path = Path(sys.argv[1]).resolve()
    generate_git_logs(repo_path)
