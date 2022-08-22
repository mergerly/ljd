import os
import sys
import time
from ljd.tools import set_luajit_version, process_file, process_folder

sys.setrecursionlimit(1000000)

# default version is 21, for LuaJIT-2.0.1
# set version to 20 for LuaJIT-2.0.0
set_luajit_version(21)

#process_file('mir2.scenes.main.console.widget.infoBar', 'mir2.scenes.main.console.widget.infoBar.lua')
# process_file('mir2.app', 'mir2.app.lua')

def process_folder2(in_dir, out_dir, lua_ext=None):
    from concurrent.futures.process import ProcessPoolExecutor
    from pathlib import Path

    start = time.time()

    in_dir = Path(in_dir)
    out_dir = Path(out_dir)

    executor = ProcessPoolExecutor()
    fs = []
    for root, _, names in os.walk(in_dir):
        root = Path(root)
        reldir = root.relative_to(in_dir)
        out_root = out_dir / reldir
        out_root.mkdir(parents=True, exist_ok=True)

        for name in names:
            relpath = reldir / name
            path_in = root / name
            if lua_ext is not None:
                out_name = Path(name).with_suffix(lua_ext)
            else:
                # out_name = name + '.lua'
                out_name = name
            path_out = out_root / out_name
            print(f"process_file: {str(path_in)} -> {str(path_out)}")
            f = executor.submit(process_file, str(path_in), str(path_out))
            f.path = str(relpath)
            fs.append(f)
    failed = []
    success = []
    for f in fs:
        try:
            f.result()
            print("SUCCESS %s" % f.path)
            success.append(f.path)
        except Exception as e:
            failed.append([f.path, e])

    dt = time.time() - start
    for path, e in failed:
        print("FAILED %s %r", path, e)
    print(
        "Decompile folder %s -> %s: success %s, fail %s in %.3fs" %(
        in_dir,
        out_dir,
        len(success),
        len(failed),
        dt)
    )
    return success

def process_folder3(in_dir, out_dir, lua_ext=None):
    from pathlib import Path
    in_dir = Path(in_dir)
    out_dir = Path(out_dir)

    for root, _, names in os.walk(in_dir):
        root = Path(root)
        reldir = root.relative_to(in_dir)
        out_root = out_dir / reldir
        out_root.mkdir(parents=True, exist_ok=True)

        for name in names:
            relpath = reldir / name
            path_in = root / name
            if lua_ext is not None:
                out_name = Path(name).with_suffix(lua_ext)
            else:
                out_name = Path(name).with_suffix('.lua')
            path_out = out_root / out_name
            print(f"process_file: {str(path_in)} -> {str(path_out)}")
            process_file(str(path_in), str(path_out))

def main():
    # process_folder(r'D:\mir3\client\resdecode\mir2', r'D:\mir3\client\resdecode\mir2u')
    # process_folder2(r'D:\mir3\client\resdecode\mir2', r'D:\mir3\client\resdecode\mir2u')
    process_file(r'F:\传奇3手游\工具\走、跑素材及安卓元宝金币灵符显示完美不掉\战神引擎走、跑素材及安卓元宝金币灵符显示\mir2.scenes.main.console.widget.infoBar', r'F:\传奇3手游\工具\走、跑素材及安卓元宝金币灵符显示完美不掉\战神引擎走、跑素材及安卓元宝金币灵符显示\mir2.scenes.main.console.widget.infoBar.lua')

if __name__ == "__main__":
    main()