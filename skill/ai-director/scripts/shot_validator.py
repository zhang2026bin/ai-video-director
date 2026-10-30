#!/usr/bin/env python3
"""
镜头语法校验器 v24
- 景别序列合理性检测
- 运镜合理性检测
- 节奏变化检测
- 滥用检测
- 台词时长校验（字数÷语速+标点停顿）
- 情绪-语速匹配校验
"""

import json
import sys
import re
from typing import List, Dict, Tuple


# ===== 景别层级（从远到近）=====
SHOT_SCALE_ORDER = {
    "大远景": 1, "远景": 2, "全景": 3, "中景": 4,
    "近景": 5, "特写": 6, "超特写": 7
}

# 景别叙事功能（来源：camera_movement_guide.md）
SHOT_SCALE_FUNCTION = {
    "大远景": {"功能": "终局/收束/人物消失/天地苍茫", "用法": "结尾拉远，叙事中段少用"},
    "远景": {"功能": "宏大/孤独/展现地理规模/人物渺小/史诗感", "用法": "需要人物细节时别用"},
    "全景": {"功能": "环境/关系/交代场景/展示人物与环境关系/群像", "用法": "需要看清表情细节时别用"},
    "中景": {"功能": "日常对话/动作/最通用景别兼顾表情和环境", "用法": "需要极致亲密或极致疏离时别用"},
    "近景": {"功能": "对话/意图/人物说话/表情变化/两人互动", "用法": "需要展示环境关系时别用"},
    "特写": {"功能": "情绪/细节/需要看清面部表情变化/手部动作", "用法": "连续多镜特写会让观众迷失空间"},
    "超特写": {"功能": "极致情绪放大/关键情绪转折点(眼泪/瞳孔/握拳)", "用法": "滥用会失去冲击力"},
}

# 合理景别跳转规则
SHOT_JUMP_RULES = {
    "同景别重复": "相邻镜头景别相同，缺乏视觉变化，除非有意制造压迫感",
    "跳过一级": "合理跳转，如远景→近景（震惊效果）",
    "跳过两级及以上": "跳跃过大，观众可能迷失空间感，需要中间镜头过渡",
    "极端跳转(远景↔特写)": "极强冲击力，只在关键情绪转折点使用",
}

# 语速标准（字/秒，经搜索验证）
SPEECH_SPEED_STANDARDS = {
    "极慢": 2.0,  # 深沉感悟/金句/哲理/内心独白/旁白
    "慢速": 2.5,  # 悲伤/沉重/温柔/安慰/回忆
    "中速": 3.5,  # 日常对话/轻松/愉快/解释
    "快速": 4.0,  # 愤怒/激动/着急/兴奋
}

# 情绪-语速对照表
EMOTION_SPEED_MAPPING = {
    "愤怒": "快速",
    "激动": "快速",
    "着急": "快速",
    "兴奋": "快速",
    "恐惧": "快速",  # 急促+短停
    "紧张": "快速",
    "慌乱": "快速",
    "日常": "中速",
    "轻松": "中速",
    "愉快": "中速",
    "解释": "中速",
    "悲伤": "慢速",
    "沉重": "慢速",
    "温柔": "慢速",
    "安慰": "慢速",
    "回忆": "慢速",
    "感悟": "极慢",
    "金句": "极慢",
    "哲理": "极慢",
    "独白": "极慢",
    "旁白": "极慢",
    "犹豫": "慢速",
    "试探": "慢速",
    "不确定": "慢速",
}

# 标点停顿时长（秒）——来源：SKILL.md标点即指令体系 + 个人知识库/标点符号语气控制体系.md
PUNCTUATION_PAUSE = {
    "——": 0.75,   # 破折号拖长0.5-1秒，取中值，语气转折/悬念
    "……": 0.5,    # 省略号渐弱/犹豫/未尽之意
    "！！": 0.5,   # 双感叹号：强度再升级，声音拔高+咬字更重，比单！多0.2秒
    "！": 0.3,    # 感叹号情绪爆发，加重咬字
    "·": 0.5,     # 间隔号一字一顿/咬牙切齿
    "，": 0.4,    # 逗号短停0.3-0.5秒
    "。": 0.9,    # 句号语气落地/收束，停顿0.8-1秒
    "？": 0.5,    # 问号尾音上扬/不确定
    "；": 0.65,   # 分号中停顿0.5-0.8秒，语气未完全收束但需换气
    " ": 0.2,     # 空格微停0.2秒，用于无标点处的自然呼吸节奏
}

# 时长公式（来源：SKILL.md 4.1时长公式）——用于估算每个镜头合理时长
SHOT_DURATION_FORMULA = {
    "旁白": {"公式": "旁白字数 ÷ 3字/秒", "示例": "15字旁白 = 5秒"},
    "单个动作": {"公式": "0.5-1.5秒", "示例": "闭眼=0.5-1秒，转头=1-1.5秒，抬手=0.5秒"},
    "动作+情绪变化": {"公式": "2-4秒", "示例": "需要看清表情从A变到B"},
    "空间建立": {"公式": "景别跨越数 × 1-2秒", "示例": "大远景→中景约3秒，全景→近景约2秒"},
    "静态展示": {"公式": "2-3秒", "示例": "建筑空镜/物品特写，超过3秒必砍"},
    "纯过渡": {"公式": "1-2秒", "示例": "叠化/色彩渐变/场景切换"},
    "转折点/情绪爆发": {"公式": "3-7秒", "示例": "仅全片最关键处使用"},
}

# 分镜4种类型自动匹配规则（来源：SKILL.md 4.0分镜类型选择）
STORYBOARD_TYPES = {
    "调度分镜图": {
        "适用": "绘本/图文/空间叙事/角色在固定场景移动",
        "核心关注": "角色在空间里的移动路径+机位跟随",
        "复杂度": 2,
        "匹配关键词": ["移动", "走到", "经过", "场景转换", "空间"],
    },
    "故事分镜图": {
        "适用": "剧情/情感/人物关系/有情感转折",
        "核心关注": "情绪节奏+叙事节拍+表演指示",
        "复杂度": 3,
        "匹配关键词": ["争吵", "和好", "感动", "离别", "对话", "情感"],
    },
    "动作分镜图": {
        "适用": "打斗/运动/舞蹈/追逐/特技动作",
        "核心关注": "动作设计+攻击轨迹+受力方向",
        "复杂度": 4,
        "匹配关键词": ["打斗", "追逐", "舞蹈", "奔跑", "攻击", "闪避", "战斗"],
    },
    "全维度执行图": {
        "适用": "复杂项目/多角色协同/需要精确控制每个维度",
        "核心关注": "机位+角色+互动+效果+音效全标注",
        "复杂度": 5,
        "匹配关键词": ["多角色", "协同", "复杂", "全维度"],
    },
}

def auto_match_storyboard_type(description: str) -> str:
    """根据内容描述自动推荐分镜类型"""
    if not description:
        return "故事分镜图"  # 默认
    
    scores = {}
    for stype, config in STORYBOARD_TYPES.items():
        score = 0
        for kw in config["匹配关键词"]:
            if kw in description:
                score += 1
        scores[stype] = score
    
    # 取最高分，无匹配则默认故事分镜图
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "故事分镜图"
    return best

# 合理的景别跳转（相邻或跨一级）
REASONABLE_JUMPS = {
    "同景别重复": "相邻镜头景别相同，缺乏视觉变化，除非有意制造压迫感",
    "跳过一级": "合理跳转，如远景→近景（震惊效果）",
    "跳过两级及以上": "跳跃过大，观众可能迷失空间感，需要中间镜头过渡",
    "极端跳转(远景↔特写)": "极强冲击力，只在关键情绪转折点使用"
}

# 运镜叙事含义
CAMERA_MOVE_MEANINGS = {
    "推近": "聚焦/发现/压迫感",
    "拉远": "揭示/孤立/解脱",
    "横摇": "观察/揭示",
    "跟拍": "参与/紧迫",
    "环绕": "英雄感/困顿感",
    "升降": "权力感/渺小感",
    "手持": "纪实感/紧张感",
    "固定": "冷静/等待/凝固",
    "甩镜": "转场/震惊/时间跳跃"
}


def validate_shot_sequence(shots: List[Dict]) -> Dict:
    """
    校验景别序列合理性。
    输入: shots列表，每个含 shot_number, shot_scale, camera_move, description, duration
    """
    if not shots:
        return {"valid": False, "error": "镜头列表为空"}
    
    issues = []
    warnings = []
    
    # 提取景别序列
    scales = []
    for s in shots:
        scale = s.get("shot_scale", "")
        scales.append(scale)
    
    # 1. 检查相邻镜头景别变化
    same_scale_count = 0
    for i in range(1, len(scales)):
        prev_level = SHOT_SCALE_ORDER.get(scales[i-1], 0)
        curr_level = SHOT_SCALE_ORDER.get(scales[i], 0)
        
        if scales[i] == scales[i-1]:
            same_scale_count += 1
            if same_scale_count >= 2:
                issues.append(
                    f"镜头{shots[i].get('shot_number', i+1)}: 连续{same_scale_count+1}个"
                    f"{scales[i]}，视觉单调"
                )
        else:
            same_scale_count = 0
        
        # 检查跳转幅度
        jump = abs(curr_level - prev_level)
        if jump >= 4:
            warnings.append(
                f"镜头{shots[i].get('shot_number', i+1)}: {scales[i-1]}→{scales[i]}跳转过大"
                f"（跨度{jump}级），确认是否有叙事需要"
            )
    
    # 2. 检查全片景别分布
    scale_distribution = {}
    for s in scales:
        scale_distribution[s] = scale_distribution.get(s, 0) + 1
    
    total_shots = len(scales)
    for scale, count in scale_distribution.items():
        ratio = count / total_shots
        if ratio > 0.5:
            issues.append(
                f"景别'{scale}'占比{ratio:.0%}，过度依赖单一景别"
            )
    
    # 3. 检查是否缺少远景（空间感缺失）
    has_establishing = any(
        s in scale_distribution for s in ["大远景", "远景", "全景"]
    )
    if not has_establishing:
        issues.append("全片无远景/全景，空间感缺失，观众无法定位")
    
    # 4. 检查是否缺少特写（情感细节缺失）
    has_close = any(
        s in scale_distribution for s in ["近景", "特写", "超特写"]
    )
    if not has_close:
        warnings.append("全片无近景/特写，情感传达可能不够直接")
    
    return {
        "valid": len(issues) == 0,
        "scale_distribution": scale_distribution,
        "has_establishing_shot": has_establishing,
        "has_close_up": has_close,
        "issues": issues,
        "warnings": warnings
    }


def validate_camera_moves(shots: List[Dict]) -> Dict:
    """校验运镜合理性"""
    issues = []
    warnings = []
    
    moves = [s.get("camera_move", "固定") for s in shots]
    
    # 1. 检查运镜滥用
    move_distribution = {}
    for m in moves:
        move_distribution[m] = move_distribution.get(m, 0) + 1
    
    total = len(moves)
    for move, count in move_distribution.items():
        ratio = count / total
        if ratio > 0.6 and move != "固定":
            issues.append(
                f"运镜'{move}'占比{ratio:.0%}，过度使用会失去冲击力"
            )
    
    # 2. 检查固定镜头比例（全片需要节奏锚点）
    static_ratio = move_distribution.get("固定", 0) / total
    if static_ratio < 0.15:
        warnings.append(
            f"固定镜头仅占{static_ratio:.0%}，全片运动过多可能让观众疲劳"
        )
    
    # 3. 检查运镜是否有叙事理由
    for s in shots:
        move = s.get("camera_move")
        meaning = s.get("camera_move_reason")  # 用户是否标注了理由
        if move and move != "固定" and not meaning:
            warnings.append(
                f"镜头{s.get('shot_number', '?')}: 运镜'{move}'未标注叙事理由"
                f"（{CAMERA_MOVE_MEANINGS.get(move, '未知运镜')}）"
            )
    
    return {
        "valid": len(issues) == 0,
        "move_distribution": move_distribution,
        "static_ratio": static_ratio,
        "issues": issues,
        "warnings": warnings
    }


def validate_rhythm(shots: List[Dict]) -> Dict:
    """检测节奏变化"""
    issues = []
    warnings = []
    
    durations = [s.get("duration", 3) for s in shots]
    
    if not durations:
        return {"valid": False, "error": "无时长数据"}
    
    # 1. 检测节奏单调（连续N个镜头时长相近）
    tolerance = 1.0  # 秒
    monotone_streak = 1
    for i in range(1, len(durations)):
        if abs(durations[i] - durations[i-1]) <= tolerance:
            monotone_streak += 1
            if monotone_streak >= 5:
                issues.append(
                    f"镜头{i-monotone_streak+2}到{i+1}: 连续{monotone_streak}个镜头"
                    f"时长接近（约{durations[i]:.1f}秒），节奏单调"
                )
        else:
            monotone_streak = 1
    
    # 2. 检测节奏转折点
    rhythm_changes = []
    for i in range(1, len(durations)):
        diff = durations[i] - durations[i-1]
        if abs(diff) > 2.0:
            rhythm_changes.append({
                "at_shot": i + 1,
                "change": f"{diff:+.1f}秒",
                "type": "加速" if diff < 0 else "减速"
            })
    
    if not rhythm_changes and len(durations) > 5:
        warnings.append("全片无节奏转折，可能缺少节奏变化")
    
    # 3. 平均节奏判断
    avg_duration = sum(durations) / len(durations)
    if avg_duration > 5:
        rhythm_type = "慢节奏"
    elif avg_duration > 2:
        rhythm_type = "中等节奏"
    else:
        rhythm_type = "快节奏"
    
    # 4. 检查全片节奏是否过于单一
    if not rhythm_changes:
        warnings.append(f"全片{rhythm_type}，缺少节奏对比")
    
    return {
        "valid": len(issues) == 0,
        "avg_duration": round(avg_duration, 1),
        "rhythm_type": rhythm_type,
        "rhythm_changes": rhythm_changes,
        "total_duration": sum(durations),
        "issues": issues,
        "warnings": warnings
    }


def calculate_dialogue_duration(dialogue: str, speed_tier: str = "中速") -> Tuple[float, float]:
    """
    计算台词时长。
    公式：中文字数÷语速+标点停顿
    
    Args:
        dialogue: 台词文本
        speed_tier: 语速档位（极慢/慢速/中速/快速）
    
    Returns:
        (纯字数时长, 总时长含标点停顿)
    """
    # 统计中文字数（排除标点和空格）
    chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', dialogue))
    
    # 获取语速
    speed = SPEECH_SPEED_STANDARDS.get(speed_tier, 3.5)
    
    # 纯字数时长
    base_duration = chinese_chars / speed if speed > 0 else 0
    
    # 计算标点停顿
    pause_duration = 0
    for punct, pause in PUNCTUATION_PAUSE.items():
        pause_duration += dialogue.count(punct) * pause
    
    total_duration = base_duration + pause_duration
    
    return round(base_duration, 2), round(total_duration, 2)


def validate_dialogue_timing(shots: List[Dict]) -> Dict:
    """
    校验台词时长是否符合镜头时长。
    规则：台词时长≤镜头时长，超8秒必须拆分
    """
    issues = []
    warnings = []
    timing_records = []
    
    for shot in shots:
        shot_num = shot.get("shot_number", "?")
        duration = shot.get("duration", 0)
        dialogue = shot.get("dialogue", "")
        speed_tier = shot.get("speed_tier", "中速")
        emotion = shot.get("emotion", "")
        
        if not dialogue:
            continue
        
        # 计算台词时长
        base_dur, total_dur = calculate_dialogue_duration(dialogue, speed_tier)
        
        # 检查是否超过镜头时长
        if total_dur > duration:
            issues.append(
                f"镜头{shot_num}: 台词时长{total_dur}秒超过镜头时长{duration}秒"
                f"（{len(re.findall(r'[\u4e00-\u9fa5]', dialogue))}字/{speed_tier}），需延长镜头或拆分台词"
            )
        
        # 检查是否超过8秒（必须拆分）
        if total_dur > 8:
            issues.append(
                f"镜头{shot_num}: 台词时长{total_dur}秒超过8秒铁律，必须拆分为多个镜头"
            )
        
        # 检查情绪-语速匹配
        if emotion:
            expected_tier = EMOTION_SPEED_MAPPING.get(emotion, "")
            if expected_tier and expected_tier != speed_tier:
                warnings.append(
                    f"镜头{shot_num}: 情绪'{emotion}'建议语速'{expected_tier}'，"
                    f"实际使用'{speed_tier}'，确认是否有意调整"
                )
        
        timing_records.append({
            "shot_number": shot_num,
            "dialogue": dialogue,
            "char_count": len(re.findall(r'[\u4e00-\u9fa5]', dialogue)),
            "speed_tier": speed_tier,
            "base_duration": base_dur,
            "total_duration": total_dur,
            "shot_duration": duration,
            "fit": "✅" if total_dur <= duration else "❌"
        })
    
    return {
        "valid": len(issues) == 0,
        "timing_records": timing_records,
        "issues": issues,
        "warnings": warnings
    }


def validate_shot_duration_rules(shots: List[Dict]) -> Dict:
    """
    校验每镜时长规则（10秒左右，5-15秒范围）。
    """
    issues = []
    warnings = []
    
    for shot in shots:
        shot_num = shot.get("shot_number", "?")
        duration = shot.get("duration", 0)
        
        if duration < 5:
            issues.append(f"镜头{shot_num}: 时长{duration}秒低于5秒下限，过短")
        elif duration > 15:
            issues.append(f"镜头{shot_num}: 时长{duration}秒超过15秒上限，过长")
        elif duration > 10:
            warnings.append(f"镜头{shot_num}: 时长{duration}秒超过10秒标准，确认是否有叙事需要")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings
    }


def full_shot_validation(shot_data: Dict) -> Dict:
    """
    执行完整镜头校验。
    输入格式:
    {
        "shots": [
            {"shot_number": 1, "shot_scale": "远景", "camera_move": "推近", 
             "description": "...", "duration": 4, "camera_move_reason": "聚焦关键线索",
             "dialogue": "台词内容", "speed_tier": "中速", "emotion": "日常"},
            ...
        ]
    }
    """
    shots = shot_data.get("shots", [])
    
    result = {
        "shot_sequence": validate_shot_sequence(shots),
        "camera_moves": validate_camera_moves(shots),
        "rhythm": validate_rhythm(shots),
        "dialogue_timing": validate_dialogue_timing(shots),
        "shot_duration_rules": validate_shot_duration_rules(shots),
        "all_issues": [],
        "all_warnings": [],
        "overall_pass": True
    }
    
    for section in ["shot_sequence", "camera_moves", "rhythm", "dialogue_timing", "shot_duration_rules"]:
        data = result[section]
        if data.get("issues"):
            tag = {
                "shot_sequence": "[景别]",
                "camera_moves": "[运镜]",
                "rhythm": "[节奏]",
                "dialogue_timing": "[台词时长]",
                "shot_duration_rules": "[镜头时长]"
            }[section]
            result["all_issues"].extend([f"{tag} {i}" for i in data["issues"]])
        if data.get("warnings"):
            tag = {
                "shot_sequence": "[景别]",
                "camera_moves": "[运镜]",
                "rhythm": "[节奏]",
                "dialogue_timing": "[台词时长]",
                "shot_duration_rules": "[镜头时长]"
            }[section]
            result["all_warnings"].extend([f"{tag} {w}" for w in data["warnings"]])
    
    result["overall_pass"] = len(result["all_issues"]) == 0
    
    return result


if __name__ == "__main__":
    input_data = json.load(sys.stdin)
    result = full_shot_validation(input_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
