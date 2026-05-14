from src import getIcon
import json
from src.appAction.report import bugs_report
import os
import sys

def get_icon(file,temp):
    return getIcon.get_icon(file,os.path.basename(file),temp)

def main(data):
    try:
        data = json.loads(data)
        path = data["path"]
        temp = data["temp"]
    except:
        path = data
        temp = True
    try:
        out_data = {}
        exes = []
        if os.path.exists(path):
            if os.path.isfile(path):
                exes.append(path)
            else:
                for item in os.listdir(path):
                    full_path = os.path.join(path, item)
                    if os.path.isfile(full_path):
                        if item.endswith(".exe") or item.endswith(".EXE"):
                            exes.append(full_path)
                        if item.endswith(".lnk"):
                            full_path = getIcon.get_shortcut_target(full_path)
                            if full_path!=None and os.path.exists(full_path):
                                if os.path.isfile(full_path) and (full_path.endswith(".exe") or full_path.endswith(".EXE")):
                                    exes.append(full_path)

        for exe in exes:
            out_data[exe] = get_icon(exe,temp)
        print(json.dumps(out_data))
    except Exception as e:
        bugs_report("python-iconGetter_parse", f"图标获取器失败: {e}",True)
        print({"error":"图标获取器失败"})
        os._exit(1)


if __name__ == "__main__":
    if len(sys.argv)>1:
        main(sys.argv[1])
    else:
        print({
            "error":"no args"
        })