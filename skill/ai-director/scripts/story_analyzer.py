#!/usr/bin/env python3
"""
故事结构分析器
- 三幕结构检测
- 转折点强度评分
- 情绪弧线计算与平段检测
- 伏笔回收检查
- 角色动机验证
"""

import json
import sys
from typing import List, Dict, Optional


# 情绪值定义
EMOTION_VALUES = {
    "绝望": -5, "崩溃": -5, "毁灭": -5,
    "恐惧": -4, "悲痛": -4, "愤怒": -4,
    "悲伤": -3, "孤独": -3, "压抑": -3,
    "忧虑": -2, "紧张": -2, "不安": -2,
    "低落": -1, "疲惫": -1, "犹豫": -1,
    "平静": 0, "日常": 0, "等待": 0,
    "好奇": 1, "期待": 1, "微光": 1,
    "温暖": 2, "喜悦": 2, "希望": 2,
    "感动": 3, "幸福": 3, "胜利": 3,
    "狂喜": 4, "巅峰": 4, "觉醒": 4,
    "超脱": 5, "救赎": 5, "永恒": 5,
}


def detect_three_act_structure(scenes: List[Dict]) -> Dict:
    """检测三幕结构是否完整"""
    if not scenes:
        return {"valid": False, "error": "场景列表为空"}
    
    total = len(scenes)
    has_act = any(s.get("act") for s in scenes)
    if not has_act:
        act1_end = max(1, int(total * 0.25))
        act2_end = max(act1_end + 1, int(total * 0.75))
        for i, s in enumerate(scenes):
            if i < act1_end:
                s["act"] = 1
            elif i < act2_end:
                s["act"] = 2
            else:
                s["act"] = 3
    
    acts = {1: [], 2: [], 3: []}
    for s in scenes:
        acts[s.get("act", 1)].append(s)
    
    act_completeness = {}
    for act_num, act_scenes in acts.items():
        act_completeness[act_num] = {
            "scene_count": len(act_scenes),
            "has_content": len(act_scenes) > 0,
            "duration_ratio": len(act_scenes) / total if total > 0 else 0
        }
    
    ideal_ratios = {1: 0.25, 2: 0.50, 3: 0.25}
    ratio_warnings = []
    for act_num, ratio in ideal_ratios.items():
        actual = act_completeness[act_num]["duration_ratio"]
        if abs(actual - ratio) > 0.15:
            ratio_warnings.append(f"第{act_num}幕占比{actual:.0%}，建议约{ratio:.0%}")
    
    act1_has_setup = any(
        s.get("purpose") in ["建置", "引入", "日常", "setup"] for s in acts[1]
    )
    act3_has_resolution = any(
        s.get("purpose") in ["解决", "高潮", "收尾", "resolution"] for s in acts[3]
    )
    
    issues = ratio_warnings[:]
    if not act1_has_setup:
        issues.append("第一幕缺少建置")
    if not act3_has_resolution:
        issues.append("第三幕缺少解决")
    
    return {
        "valid": all(act_completeness[a]["has_content"] for a in [1, 2, 3]),
        "act_completeness": act_completeness,
        "ratio_warnings": ratio_warnings,
        "act1_has_setup": act1_has_setup,
        "act3_has_resolution": act3_has_resolution,
        "total_scenes": total,
        "issues": issues
    }


def score_turning_point(scene_before: Dict, scene_after: Dict) -> int:
    """评估转折点强度(1-5分)"""
    emotion_before = scene_before.get("emotion_value", 0)
    emotion_after = scene_after.get("emotion_value", 0)
    
    delta = abs(emotion_after - emotion_before)
    direction_flip = (emotion_before * emotion_after < 0)
    
    if delta >= 6:
        score = 5
    elif delta >= 4:
        score = 4
    elif delta >= 3:
        score = 3
    elif delta >= 2:
        score = 2
    else:
        score = 1
    
    if direction_flip:
        score = min(5, score + 1)
    
    return score


def analyze_emotion_arc(scenes: List[Dict]) -> Dict:
    """分析情绪弧线，检测平段"""
    emotions = []
    for s in scenes:
        ev = s.get("emotion_value")
        if ev is None:
            emotion_label = s.get("emotion", "平静")
            ev = EMOTION_VALUES.get(emotion_label, 0)
        emotions.append(ev)
    
    if not emotions:
        return {"valid": False, "error": "无情绪数据"}
    
    # 检测平段：连续3个以上同方向
    flat_zones = []
    streak_start = 0
    streak_direction = 0
    
    for i in range(1, len(emotions)):
        diff = emotions[i] - emotions[i-1]
        current_dir = 1 if diff > 0 else (-1 if diff < 0 else 0)
        
        if current_dir == streak_direction and current_dir != 0:
            continue
        else:
            streak_len = i - streak_start
            if streak_len >= 3 and streak_direction != 0:
                flat_zones.append({
                    "start_scene": streak_start + 1,
                    "end_scene": i,
                    "direction": "持续上升" if streak_direction > 0 else "持续下降",
                    "length": streak_len,
                    "suggestion": "建议在此区间插入反差场景打破单调"
                })
            streak_start = i - 1
            streak_direction = current_dir
    
    streak_len = len(emotions) - streak_start
    if streak_len >= 3 and streak_direction != 0:
        flat_zones.append({
            "start_scene": streak_start + 1,
            "end_scene": len(emotions),
            "direction": "持续上升" if streak_direction > 0 else "持续下降",
            "length": streak_len,
            "suggestion": "建议在此区间插入反差场景打破单调"
        })
    
    max_idx = emotions.index(max(emotions)) if emotions else 0
    min_idx = emotions.index(min(emotions)) if emotions else 0
    
    pre_climax_buildup = False
    if max_idx >= 2:
        pre_emotions = emotions[max_idx-2:max_idx]
        if all(e < emotions[max_idx] for e in pre_emotions):
            pre_climax_buildup = True
    
    opening_closing_relation = "闭环" if (emotions[0] * emotions[-1] > 0) else "反差"
    
    issues = []
    if flat_zones:
        issues.append("存在平段（连续3场以上同向情绪）")
    if not pre_climax_buildup and max_idx > 0:
        issues.append("高潮前缺乏足够蓄势")
    
    return {
        "valid": True,
        "emotion_curve": emotions,
        "max_emotion_scene": max_idx + 1,
        "min_emotion_scene": min_idx + 1,
        "flat_zones": flat_zones,
        "has_flat_zones": len(flat_zones) > 0,
        "pre_climax_buildup": pre_climax_buildup,
        "opening_closing_relation": opening_closing_relation,
        "emotion_range": max(emotions) - min(emotions),
        "issues": issues
    }


def check_foreshadowing(foreshadows: List[Dict]) -> Dict:
    """检查伏笔回收"""
    unresolved = []
    resolved = []
    
    for f in foreshadows:
        if f.get("resolved_scene"):
            resolved.append(f)
        else:
            unresolved.append(f)
    
    issues = [
        f"伏笔'{f.get('description', f.get('id', '?'))}'未回收，种植于第{f.get('planted_scene', '?')}场"
        for f in unresolved
    ]
    
    return {
        "total": len(foreshadows),
        "resolved_count": len(resolved),
        "unresolved_count": len(unresolved),
        "unresolved": unresolved,
        "all_resolved": len(unresolved) == 0,
        "issues": issues
    }


def validate_character_motivation(characters: List[Dict]) -> Dict:
    """验证角色动机和弧线"""
    results = []
    issues = []
    
    for char in characters:
        name = char.get("name", "未命名")
        motivation = char.get("motivation")
        arc = char.get("arc")
        
        char_issues = []
        if not motivation:
            char_issues.append("缺少核心动机")
        
        if not arc:
            char_issues.append("缺少角色弧线")
        else:
            if arc.get("start") == arc.get("end"):
                char_issues.append("弧线无变化（开篇=结尾），角色是NPC")
            if not arc.get("middle"):
                char_issues.append("弧线缺少中间变化")
        
        results.append({
            "name": name,
            "has_motivation": bool(motivation),
            "has_arc": bool(arc),
            "arc_has_change": arc.get("start") != arc.get("end") if arc else False,
            "issues": char_issues
        })
        issues.extend([f"角色'{name}': {i}" for i in char_issues])
    
    return {
        "characters": results,
        "total": len(results),
        "characters_with_issues": sum(1 for r in results if r["issues"]),
        "issues": issues
    }


def full_analysis(story_data: Dict) -> Dict:
    """
    执行完整故事结构分析。
    输入格式:
    {
        "scenes": [{"id": 1, "act": 1, "emotion": "平静", "emotion_value": 0, "purpose": "建置"}, ...],
        "turning_points": [{"after_scene": 5, "description": "..."}, ...],
        "foreshadows": [{"id": "f1", "planted_scene": 3, "resolved_scene": 10, "description": "..."}, ...],
        "characters": [{"name": "主角", "motivation": "...", "arc": {"start": "...", "middle": "...", "end": "..."}}, ...]
    }
    """
    result = {
        "structure": None,
        "emotion_arc": None,
        "turning_points": None,
        "foreshadowing": None,
        "characters": None,
        "all_issues": [],
        "overall_pass": True
    }
    
    scenes = story_data.get("scenes", [])
    
    if scenes:
        result["structure"] = detect_three_act_structure(scenes)
        if result["structure"].get("issues"):
            result["all_issues"].extend(["[结构] " + i for i in result["structure"]["issues"]])
    
    if scenes:
        result["emotion_arc"] = analyze_emotion_arc(scenes)
        if result["emotion_arc"].get("issues"):
            result["all_issues"].extend(["[弧线] " + i for i in result["emotion_arc"]["issues"]])
    
    turning_points = story_data.get("turning_points", [])
    tp_scores = []
    for tp in turning_points:
        scene_idx = tp.get("after_scene", 0) - 1
        if 0 <= scene_idx < len(scenes) - 1:
            score = score_turning_point(scenes[scene_idx], scenes[scene_idx + 1])
            tp_scores.append({
                "after_scene": tp["after_scene"],
                "description": tp.get("description", ""),
                "score": score,
                "passing": score >= 3
            })
    result["turning_points"] = tp_scores
    weak_tps = [t for t in tp_scores if not t["passing"]]
    if weak_tps:
        result["all_issues"].extend([
            f"[转折] 第{t['after_scene']}场后转折强度仅{t['score']}分（需≥3）"
            for t in weak_tps
        ])
    
    foreshadows = story_data.get("foreshadows", [])
    if foreshadows:
        result["foreshadowing"] = check_foreshadowing(foreshadows)
        if result["foreshadowing"].get("issues"):
            result["all_issues"].extend(["[伏笔] " + i for i in result["foreshadowing"]["issues"]])
    
    characters = story_data.get("characters", [])
    if characters:
        result["characters"] = validate_character_motivation(characters)
        if result["characters"].get("issues"):
            result["all_issues"].extend(["[角色] " + i for i in result["characters"]["issues"]])
    
    result["overall_pass"] = len(result["all_issues"]) == 0
    
    return result


if __name__ == "__main__":
    input_data = json.load(sys.stdin)
    result = full_analysis(input_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
