#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_prompt_text.py —— 导演台六部门 · 提示词结构校验
用途：校验六部门联合会诊产出的最终视频提示词是否达标。
校验项（对齐 Leos 规范 + 导演台既有铁律）：
  1. 非 JSON：不得输出 JSON / 伪 JSON
  2. 有效字符数（去除空白/换行/制表/代码围栏后）≤ 5000
  3. 通过 @image 引用完成资产绑定
  4. 严格镜头数声明 + 实际镜头编号连续（镜头1..镜头N）
  5. 每镜字段完整：机位 / 摄影机运动 / 摄影机位置 / 背景 / 动作 / 微表演细节
用法：python3 scripts/validate_prompt_text.py <prompt-file>
依赖：Python 3.9+，纯标准库
"""
import re
import sys

MAX_VALID_CHARS = 5000


def strip_non_valid(s: str) -> str:
    """去除代码围栏、空白、换行、制表符后的有效字符。"""
    s = re.sub(r"```(?:text|markdown|plaintext)?", "", s)
    s = re.sub(r"\s+", "", s)
    return s


def check_json(text: str) -> list:
    errs = []
    stripped = text.strip()
    if stripped.startswith("{") and ("\"role" in stripped or "```json" in text):
        errs.append("检测到 JSON/伪 JSON 输出，必须改为纯文本镜头模板。")
    return errs


def check_asset_binding(text: str) -> list:
    errs, warns = [], []
    images = re.findall(r"@image(\d+)", text)
    if not images:
        warns.append("未检测到 @image 资产绑定。短片/无参考资产时可忽略；有参考图时应写 @image 绑定。")
    else:
        if len(images) != len(set(images)):
            errs.append("存在重复的 @image 编号，应每种资产唯一。")
    return errs, warns


def check_shot_count(text: str) -> list:
    errs, warns = [], []
    m = re.search(r"只有\s*(\d+)\s*个镜头|N\s*=\s*(\d+)", text)
    declared = None
    if m:
        declared = int(m.group(1) or m.group(2))
        warns.append(f"声明严格 {declared} 个镜头（若与实际不符会强制校验）。")
    shots = []
    for mm in re.finditer(r"【镜头\s*(\d+)\s*】", text):
        shots.append(int(mm.group(1)))
    if not shots:
        errs.append("未检测到【镜头1】…【镜头N】标注，无法完成逐镜校验。")
        return errs, warns
    shots = sorted(shots)
    if shots != list(range(1, len(shots) + 1)):
        errs.append(f"镜头编号不连续：实际为 {shots}，应严格为 1..{len(shots)}。")
    if declared and len(shots) != declared:
        errs.append(f"声明 {declared} 个镜头，实际检测到 {len(shots)} 个，不一致。")
    return errs, warns


REQUIRED_FIELDS = ["机位", "摄影机运动", "摄影机位置", "背景", "动作", "微表演细节"]


def check_shot_fields(text: str) -> list:
    errs = []
    shot_blocks = re.split(r"【镜头\s*\d+\s*】", text)
    # 第一段是开头（资产/空间/声明），跳过
    for idx, block in enumerate(shot_blocks[1:], start=1):
        missing = [f for f in REQUIRED_FIELDS if f not in block]
        if missing:
            errs.append(f"镜头{idx} 缺少字段：{', '.join(missing)}。")
    return errs


def main():
    if len(sys.argv) < 2:
        print("用法：python3 scripts/validate_prompt_text.py <prompt-file>")
        sys.exit(2)
    path = sys.argv[1]
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        print(f"无法读取文件：{e}")
        sys.exit(2)

    errs = []
    warns = []
    valid = strip_non_valid(text)
    vlen = len(valid)

    errs += check_json(text)
    e, w = check_asset_binding(text)
    errs += e
    warns += w
    e, w = check_shot_count(text)
    errs += e
    warns += w
    errs += check_shot_fields(text)

    if vlen > MAX_VALID_CHARS:
        errs.append(f"有效字符 {vlen} 超过上限 {MAX_VALID_CHARS}。")

    print(f"有效字符数：{vlen} / {MAX_VALID_CHARS}")
    for w in warns:
        print(f"[提示] {w}")
    if errs:
        print(f"校验未通过（{len(errs)} 项）：")
        for e in errs:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("校验通过：非JSON、字数达标、镜头连续、字段完整。")
        sys.exit(0)


if __name__ == "__main__":
    main()