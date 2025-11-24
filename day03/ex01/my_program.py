from local_lib.path import pathlib


def main() -> int:

    script_dir = pathlib.Path(__file__).parent
    repo_root = (script_dir ).resolve()

    work_dir = repo_root / 'test_folder'
    work_dir.mkdir(parents=True, exist_ok=True)

    file_path = work_dir / 'test_file.txt'
    content = 'Hello World!!!!\n'

    with file_path.open('w') as f:
        f.write(content)

    with file_path.open('r') as f:
        data = f.read()

    print(f'Write and read from: {file_path}')
    print(data)

    return 1
if __name__ == '__main__':
    main()