#!/usr/bin/env python
from pathlib import Path
import argparse
import csv

menufilepath = Path('saizeriya_menu.txt')


def printallmenu():
    with open(menufilepath, encoding='utf-8', mode='r') as f:
        print(f.read())

# 部分的な置換を避ける為に、
# 置換の前にメニューリストを、メニュー名が長い順にソートする
# 例
# ---
# AA20,バッファローモッツァレラ
# AA70,バッファローモッツァレラWサイズ
# ---
# OK : バッファローモッツァレラWサイズ > AA70
# NG : バッファローモッツァレラWサイズ > AA20Wサイズ

def convert(in_txt: str, iscompile: bool):
    with open(menufilepath, encoding='utf-8', mode='r') as f:
        menulist = csv.reader(f, delimiter=',')
        menulistsorted = sorted(
            list(menulist).copy(),
            key=lambda x: len(
                x[1]),
            reverse=True)
        # print(menulistsorted)

        out_txt = in_txt

        # 半角全角表記ゆれ対策
        # 半角に統一する
        out_txt = out_txt.replace("（", "(").replace("）", ")")
        out_txt = out_txt.replace("＆", "&")
        if iscompile:
            for i in range(len(menulistsorted)):
                out_txt = out_txt.replace(menulistsorted[i][1], menulistsorted[i][0])
        else:  # decompile
            for i in range(len(menulistsorted)):
                out_txt = out_txt.replace(menulistsorted[i][0], menulistsorted[i][1])
        print(out_txt)


def compile(in_txt: str):
    convert(in_txt=in_txt, iscompile=True)


def decompile(in_txt: str):
    convert(in_txt=in_txt, iscompile=False)


def main():
    psr = argparse.ArgumentParser()
    # psr.add_argument('-a', '--all', help="print all menu")
    psr.add_argument('-c', '--compile', default="", help="convert menu to menu code")
    psr.add_argument('-d', '--decompile', default="", help="convert menu code to menu")
    args = psr.parse_args()

    # if args.all:
    #     printallmenu()
    if len(args.compile) > 0:
        compile(args.compile)
    if len(args.decompile) > 0:
        decompile(args.decompile)
    # test
    # compile("カルボナーラ大盛")
    # decompile("PA55")
    # compile("バッファローモッツァレラのピザWチーズ、エビクリームグラタン、カルボナーラ大盛(｀・ω・´)")


if __name__ == '__main__':
    main()
