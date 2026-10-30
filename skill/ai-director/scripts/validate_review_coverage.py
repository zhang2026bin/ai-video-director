#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_review_coverage.py —— 导演台六部门 · 逐镜审稿覆盖校验
用途：校验六角色逐镜审稿表是否达到 6×N 笛卡尔全覆盖。
规则：参与审稿的六个角色（总导演/表演指导/镜内执行导演/摄影指导/提示词导演/场记）
      必须依次覆盖镜头 1..N，应有 6×N 条角色—镜头记录；不得缺行/重复/越界。
用法：python3 scripts/validate_review_coverage.py <review.md> --shots N
依赖：Python 3.9+，纯标准库
"""
import argparse
import re
import sys

# 归一化后的六岗位标准名（与 normalize_role 的返回值一致）
ROLES = ["总导演", "表演指导", "镜内执行导演", "摄影指导", "提示词导演", "场记"]


def normalize_role(name: str) -> str:
    """把表格中的角色名归一到六大岗。
    注意：必须先匹配最具体的岗位名，最后才是"导演"（总导演），
    否则"镜内执行导演/表演指导/摄影指导/提示词导演"都会被"导演"提前吞并。"""
    if "执行" in name:
        return "镜内执行导演"
    if "表演" in name:
        return "表演指导"
    if "摄影" in name:
        return "摄影指导"
    if "提示词" in name:
        return "提示词导演"
    if "场记" in name or "连续" in name:
        return "场记"
    if "导演" in name:
        return "总导演"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("review_file")
    ap.add_argument("--shots", type=int, required=True)
    args = ap.parse_args()

    try:
        text = open(args.review_file, encoding="utf-8").read()
    except OSError as e:
        print(f"无法读取文件：{e}")
        sys.exit(2)

    n = args.shots
    records = []  # (role, shot)
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        role_norm = normalize_role(cells[0])
        if role_norm is None:
            continue
        try:
            shot = int(re.sub(r"\D", "", cells[1]))
        except ValueError:
            continue
        if shot >= 1 and shot <= n:
            records.append((role_norm, shot))

    expected = 6 * n
    errs = []

    # 缺行
    covered = set(records)
    missing = [(r, s) for r in ROLES for s in range(1, n + 1)
               if (r, s) not in covered]
    if missing:
        errs.append(f"缺行 {len(missing)} 条（应为 6×{n}={expected} 条），缺失如：{missing[:5]}…")

    # 重复
    if len(records) != len(set(covered)):
        dup = [x for x in covered if records.count(x) > 1]
        errs.append(f"存在重复行：{dup}")

    # 越界
    over = [r for r in records if r[1] > n]
    if over:
        errs.append(f"存在超出镜头范围的记录：{over[:5]}")

    print(f"检测到审稿记录：{len(records)} 条；期望 6×{n}={expected} 条")
    if errs:
        print("审稿覆盖校验未通过：")
        for e in errs:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("校验通过：六角色×N镜全覆盖，无缺行/重复/越界。")
        sys.exit(0)


if __name__ == "__main__":
    main()