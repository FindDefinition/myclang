from pathlib import Path 
import json 
if __name__ == "__main__":
    p1 = Path("/home/yy/deeplearning/myclang/myclang/cext/clang++.json")
    p2 = Path("/home/yy/deeplearning/myclang/myclang/cext/libclang.json")
    with p1.open("r") as f:
        p1d = json.load(f)
    with p2.open("r") as f:
        p2d = json.load(f)
    libs1 = p1d["Linux"]["libraries"]
    libs2 = p2d["Linux"]["libraries"]
    res = []
    for l in libs2:
        if l not in libs1:
            res.append(l)
            print(l)