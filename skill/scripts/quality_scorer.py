#!/usr/bin/env python3
"""
品质评分系统
- 视频质量评分（画面/运动/一致性/场景/瑕疵）
- 导演素养自查清单（叙事/视听/场景/声音/品质）
"""

import json
import sys
from typing import List, Dict


# 视频质量评分维度
VIDEO_QUALITY_DIMENSIONS = {
    "画面清晰度": {
        "description": "分辨率、锐度、噪点控制",
        "weight": 1.0,
        "threshold": 4.0,
        "scoring_guide": {
            5: "4K级清晰，细节丰富，零噪点",
            4: "1080p清晰，少量噪点不影响观感",
            3: "基本清晰，偶有模糊帧",
            2: "部分画面模糊，影响观感",
            1: "大量模糊帧，不可接受"
        }
    },
    "运动流畅度": {
        "description": "帧率、动作连贯性、物理合理性",
        "weight": 1.0,
        "threshold": 3.5,
        "scoring_guide": {
            5: "丝滑流畅，物理完全合理",
            4: "流畅，极少量物理瑕疵",
            3: "基本流畅，偶有跳帧或不自然动作",
            2: "明显卡顿或变形",
            1: "严重变形，不可使用"
        }
    },
    "角色一致性": {
        "description": "面部/体型/服装跨镜头一致",
        "weight": 1.2,
        "threshold": 4.0,
        "scoring_guide": {
            5: "完全一致，同一人",
            4: "高度一致，微小区别可忽略",
            3: "基本一致，仔细看能看出差别",
            2: "明显不一致，像换了人",
            1: "完全不同，角色崩坏"
        }
    },
    "场景合理性": {
        "description": "空间逻辑、光影一致、道具连贯",
        "weight": 0.8,
        "threshold": 3.5,
        "scoring_guide": {
            5: "完美空间逻辑，零穿帮",
            4: "合理，极少量不自然",
            3: "基本合理，偶有穿帮",
            2: "空间逻辑混乱",
            1: "完全不合理"
        }
    },
    "无瑕疵度": {
        "description": "AI特有瑕疵（多指/变形/文字乱码/浮空物体）",
        "weight": 1.0,
        "threshold": 3.5,
        "scoring_guide": {
            5: "零AI瑕疵",
            4: "1个轻微瑕疵",
            3: "2-3个轻微或1个明显瑕疵",
            2: "多处明显瑕疵",
            1: "严重AI崩坏（多指/面部变形）"
        }
    }
}


# 导演素养自查清单
DIRECTOR_CHECKLIST = {
    "叙事层": {
        "items": [
            {"id": "n1", "check": "三幕结构完整", "must": True},
            {"id": "n2", "check": "转折点强度≥3分", "must": True},
            {"id": "n3", "check": "情绪弧线有起伏，无平段", "must": True},
            {"id": "n4", "check": "每个角色有清晰动机", "must": True},
            {"id": "n5", "check": "伏笔全部回收", "must": True},
            {"id": "n6", "check": "开头15秒抓住观众", "must": True},
        ]
    },
    "视听层": {
        "items": [
            {"id": "v1", "check": "每个景别有叙事理由", "must": True},
            {"id": "v2", "check": "每个运镜有叙事含义", "must": True},
            {"id": "v3", "check": "色彩匹配情绪弧线", "must": True},
            {"id": "v4", "check": "节奏有变化，非匀速", "must": True},
            {"id": "v5", "check": "光影服务于叙事", "must": False},
            {"id": "v6", "check": "有至少1个构图记忆点", "must": False},
        ]
    },
    "场景层": {
        "items": [
            {"id": "s1", "check": "每个空间有叙事功能", "must": True},
            {"id": "s2", "check": "场景三层内容（前景/中景/背景）", "must": True},
            {"id": "s3", "check": "表演有层次（微表情>大动作）", "must": False},
            {"id": "s4", "check": "无多余场景", "must": True},
        ]
    },
    "声音层": {
        "items": [
            {"id": "a1", "check": "声音三层设计（台词/音效/音乐）", "must": True},
            {"id": "a2", "check": "至少1个静默时刻", "must": False},
            {"id": "a3", "check": "音乐匹配情绪弧线", "must": True},
        ]
    },
    "品质层": {
        "items": [
            {"id": "q1", "check": "画面风格跨镜头一致", "must": True},
            {"id": "q2", "check": "情绪连贯无断裂", "must": True},
            {"id": "q3", "check": "逻辑无断裂", "must": True},
            {"id": "q4", "check": "无AI特有瑕疵（多指/变形/乱码）", "must": True},
        ]
    }
}


def score_video_quality(scores: Dict[str, float]) -> Dict:
    """
    评分视频质量。
    输入: 各维度分数(1-5)
    输出: 加权总分 + 是否通过 + 各维度详情
    """
    results = {}
    total_weight = 0
    weighted_sum = 0
    failed_dimensions = []
    
    for dim_name, config in VIDEO_QUALITY_DIMENSIONS.items():
        score = scores.get(dim_name, 0)
        weight = config["weight"]
        threshold = config["threshold"]
        passed = score >= threshold
        
        results[dim_name] = {
            "score": score,
            "weight": weight,
            "weighted_score": score * weight,
            "threshold": threshold,
            "passed": passed,
            "guide": config["scoring_guide"].get(score, "")
        }
        
        weighted_sum += score * weight
        total_weight += weight
        
        if not passed:
            failed_dimensions.append(f"{dim_name}: {score}分（需≥{threshold}）")
    
    overall_score = weighted_sum / total_weight if total_weight > 0 else 0
    overall_pass = len(failed_dimensions) == 0 and overall_score >= 3.5
    
    return {
        "dimensions": results,
        "overall_score": round(overall_score, 2),
        "overall_pass": overall_pass,
        "failed_dimensions": failed_dimensions,
        "action": "通过" if overall_pass else "未通过，需重设提示词或重生成"
    }


def run_director_checklist(check_results: Dict[str, Dict[str, bool]]) -> Dict:
    """
    导演素养自查清单。
    输入: {category_id: {item_id: True/False}}
    输出: 通过率 + 失败项 + 必须/建议分类
    """
    total_items = 0
    passed_items = 0
    must_fail = []
    suggest_fail = []
    category_results = {}
    
    for category_name, category_data in DIRECTOR_CHECKLIST.items():
        cat_checks = check_results.get(category_name, {})
        cat_pass = 0
        cat_total = 0
        
        for item in category_data["items"]:
            item_id = item["id"]
            checked = cat_checks.get(item_id, False)
            total_items += 1
            cat_total += 1
            
            if checked:
                passed_items += 1
                cat_pass += 1
            else:
                entry = {
                    "category": category_name,
                    "id": item_id,
                    "check": item["check"],
                    "must": item["must"]
                }
                if item["must"]:
                    must_fail.append(entry)
                else:
                    suggest_fail.append(entry)
        
        category_results[category_name] = {
            "passed": cat_pass,
            "total": cat_total,
            "ratio": f"{cat_pass}/{cat_total}"
        }
    
    return {
        "overall_ratio": f"{passed_items}/{total_items}",
        "overall_percentage": round(passed_items / total_items * 100, 1) if total_items > 0 else 0,
        "must_fail_count": len(must_fail),
        "suggest_fail_count": len(suggest_fail),
        "must_fail_items": must_fail,
        "suggest_fail_items": suggest_fail,
        "category_results": category_results,
        "overall_pass": len(must_fail) == 0,
        "action": "通过" if len(must_fail) == 0 else f"未通过，{len(must_fail)}项必须项未达标"
    }


def full_quality_check(quality_data: Dict) -> Dict:
    """
    执行完整品质检查。
    输入格式:
    {
        "mode": "video" | "checklist" | "both",
        "video_scores": {
            "画面清晰度": 4,
            "运动流畅度": 3.5,
            "角色一致性": 4,
            "场景合理性": 3.5,
            "无瑕疵度": 4
        },
        "checklist_results": {
            "叙事层": {"n1": true, "n2": true, ...},
            "视听层": {"v1": true, ...},
            ...
        }
    }
    """
    mode = quality_data.get("mode", "both")
    result = {}
    
    if mode in ["video", "both"]:
        video_scores = quality_data.get("video_scores", {})
        if video_scores:
            result["video_quality"] = score_video_quality(video_scores)
    
    if mode in ["checklist", "both"]:
        checklist_results = quality_data.get("checklist_results", {})
        if checklist_results:
            result["checklist"] = run_director_checklist(checklist_results)
    
    # 综合判断
    video_pass = result.get("video_quality", {}).get("overall_pass", True)
    checklist_pass = result.get("checklist", {}).get("overall_pass", True)
    result["overall_pass"] = video_pass and checklist_pass
    
    return result


if __name__ == "__main__":
    input_data = json.load(sys.stdin)
    result = full_quality_check(input_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
