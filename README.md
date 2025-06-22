# 🧠 Installing `dlib` in a Conda Environment (Python 3.10, Linux)

This guide shows how to install the `dlib` library using a Conda environment with Python 3.10 on Linux.

```bash
# 1️⃣ Create Conda Environment
conda create -n face-env python=3.10 -y
conda activate face-env

# 2️⃣ Install Dependencies
conda install -c conda-forge cmake boost
sudo apt update
sudo apt install build-essential libopenblas-dev liblapack-dev

# 3️⃣ Install dlib
pip install dlib

# (If it fails with a compiler error)
pip install dlib --no-cache-dir

# (Optional: GPU-enabled version)
pip install dlib==19.24.0

# 4️⃣ Verify Installation
python -c "import dlib; print(dlib.__version__)"
```

> ✅ Notes:
> - Works best on Ubuntu-based systems.
> - Compilation may take a few minutes.
> - Use `--no-cache-dir` to avoid stale builds if needed.
> - For face recognition, install `face_recognition` after `dlib`.

# Installing env dependencies

`conda create --name face-env --file requirements.txt`

you still need to go through step *2* till *4* to ensure `dlib` is installed correctly.