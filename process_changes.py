import sys

def process_changed_files(changed_files_path, changes_with_diffs_path):
    # 변경된 파일 목록 읽기
    with open(changed_files_path, 'r') as f:
        changed_files = f.read().splitlines()

    # 변경된 파일 내용 읽기
    with open(changes_with_diffs_path, 'r') as f:
        changes_with_diffs = f.read()

    print(f"Changed Files: {changed_files}")

    # 파일별로 변경된 코드 추출
    for file in changed_files:
        print(f'\n"변경된 파일명"\n"{file}"')
        print('"변경 내용..."')
        
        # 변경된 내용 중에서 모든 라인을 출력
        lines = changes_with_diffs.splitlines()
        for line in lines:
            # diff 헤더, 인덱스 등 불필요한 부분을 제외하고 모든 라인 출력
            if line.startswith('diff --git') or line.startswith('index') or line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
                continue  # 불필요한 diff 메타데이터는 건너뜀

            if line.startswith('+'):
                print(f"+ {line[1:]}")  # 추가된 내용
            elif line.startswith('-'):
                print(f"- {line[1:]}")  # 삭제된 내용
            else:
                print(f"  {line}")  # 변경되지 않은 내용

if __name__ == "__main__":
    # 파일 경로를 인자로 받음
    changed_files_path = sys.argv[1]
    changes_with_diffs_path = sys.argv[2]

    process_changed_files(changed_files_path, changes_with_diffs_path)
