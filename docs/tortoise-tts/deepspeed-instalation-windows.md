# 1. Install libaio
```
pip install libaio
```

# 2. Clone DeepSpeed
```
git clone https://github.com/microsoft/DeepSpeed
```

# 3. Build for Windows.
If you are using Visual Studio Community 2019:
```
cd DeepSpeed
```
Make cl compiler visible
```
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" x64
```
After this, use the command below to test if cl is visible
```
cl
```
Build DeepSpeed
```
build_win.bat
```

# 4. Install Python package

```
pip install dist/deepspeed-0.14.5+879c6cd0-cp39-cp39-win_amd64.whl
```