import sys

def process_changed_files(changed_files_path, changes_with_diffs_path):
    # 변경된 파일 목록 읽기
    with open(changed_files_path, 'r') as f:
        changed_files = f.read().splitlines()
    
    print(f"Changed Files: {changed_files}")

    # 변경된 파일 내용 읽기
    with open(changes_with_diffs_path, 'r') as f:
        changes_with_diffs = f.read()

    print("\nChanges with Diffs:\n")
    print(changes_with_diffs)

    # 여기서 파일명과 내용을 활용한 로직 추가
    for file in changed_files:
        print(f"Processing file: {file}")
        # 파일별로 처리 로직 작성 가능

if __name__ == "__main__":
    # 파일 경로를 인자로 받음
    changed_files_path = sys.argv[1]
    changes_with_diffs_path = sys.argv[2]

    process_changed_files(changed_files_path, changes_with_diffs_path)
