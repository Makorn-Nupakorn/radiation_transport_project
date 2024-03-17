brew install uv

uv venv rt_env.venv

source rt_env.venv/bin/activate

uv pip install ipykernel rich pyyaml yml memory-profiler

python3 main.py