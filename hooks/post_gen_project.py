import subprocess

def pip_compile():
    print('Running pip compile...')
    with open("requirements.txt", "w") as fs:
        subprocess.run(['uv', 'pip', 'compile', 'requirements.in'], check=True, stdout=fs)

def create_venv():
    print('Creating virtual environment...')
    subprocess.run(['python', '-m', 'venv', 'venv'], check=True)

def init_git():
    print('Initializing Git repository...')
    subprocess.run(['git', 'init'], check=True)

def main():
    create_venv()
    pip_compile()
    init_git()

if __name__ == '__main__':
    main()
