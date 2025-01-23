import sys

def process_changed_files(changed_files_path, changes_with_diffs_path):
    # 변경된 파일 목록 읽기
    with open(changed_files_path, 'r') as f:
        changed_files = f.read().splitlines()

    # 변경된 파일 내용 읽기
    with open(changes_with_diffs_path, 'r') as f:
        changes_with_diffs = f.read()

    print(f"Changed Files: {changed_files}")

    # 변경된 파일별로 내용을 출력
    for file in changed_files:
        print(f'\n"변경된 파일명"\n"{file}"')
        print('"변경 내용..."')

        # 해당 파일에 대한 변경된 코드만 추출
        lines = changes_with_diffs.splitlines()
        file_changes_started = False  # 해당 파일에 대한 변경 사항 시작 여부 확인

        for line in lines:
            # 파일에 해당하는 diff 블록만 처리
            if f'a/{file}' in line or f'b/{file}' in line:  # 해당 파일에 대한 diff 시작을 찾음
                file_changes_started = True
            
            if file_changes_started:
                # diff 헤더, 인덱스 등 불필요한 부분을 제외하고 변경 사항만 출력
                if line.startswith('diff --git') or line.startswith('index') or line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
                    continue  # 불필요한 diff 메타데이터는 건너뜀

                # "\ No newline at end of file" 제거
                if '\\ No newline at end of file' in line:
                    continue

                # 변경 사항 출력
                if line.startswith('+'):
                    print(f"+ {line[1:]}")  # 추가된 내용
                elif line.startswith('-'):
                    print(f"- {line[1:]}")  # 삭제된 내용
                else:
                    print(f"  {line}")  # 변경되지 않은 내용

                # 해당 파일의 변경 사항 끝나면 다음 파일로 넘어가기
                if line.startswith('diff --git'):
                    file_changes_started = False

if __name__ == "__main__":
    # 파일 경로를 인자로 받음
    changed_files_path = sys.argv[1]
    changes_with_diffs_path = sys.argv[2]

    process_changed_files(changed_files_path, changes_with_diffs_path)
