"""
分镜图生成器 - AI导演台v30
根据分镜脚本自动生成4种类型的分镜图提示词
"""

from typing import Dict, List, Optional


def generate_storyboard_prompt(
    storyboard_type: str,
    shot_data: Dict,
    style: str = "电影级超写实",
    character_desc: str = "",
    scene_desc: str = ""
) -> str:
    """
    生成分镜图提示词
    
    Args:
        storyboard_type: 分镜图类型
            - "调度图" - 场景空间布局（俯视图，展示角色位置和运动轨迹）
            - "故事板" - 镜头关系（多个镜头并排，展示叙事逻辑）
            - "动作板" - 动作细节（关键动作的连续帧）
            - "全维度板" - 所有元素（场景+角色+动作+光影+情绪）
        shot_data: 镜头数据，包含：
            - shot_id: 镜头编号（如"S03"）
            - duration: 时长（秒）
            - emotion: 情绪关键词
            - location: 场景位置
            - action: 主要动作
            - camera_movement: 运镜方式
            - shot_size: 景别
        style: 视觉风格（默认电影级超写实）
        character_desc: 角色描述
        scene_desc: 场景描述
    
    Returns:
        分镜图提示词字符串
    """
    
    if storyboard_type == "调度图":
        return _generate_blocking_board(shot_data, style, character_desc, scene_desc)
    elif storyboard_type == "故事板":
        return _generate_story_board(shot_data, style)
    elif storyboard_type == "动作板":
        return _generate_action_board(shot_data, style, character_desc)
    elif storyboard_type == "全维度板":
        return _generate_full_dimension_board(shot_data, style, character_desc, scene_desc)
    else:
        raise ValueError(f"不支持的分镜图类型: {storyboard_type}")


def _generate_blocking_board(shot_data: Dict, style: str, character_desc: str, scene_desc: str) -> str:
    """生成调度图 - 俯视图展示角色位置和运动轨迹"""
    
    return f"""【调度图】{shot_data.get('shot_id', 'SXX')} | {shot_data.get('duration', 0)}s | {shot_data.get('location', '')}

**画面构图**：
- 视角：俯视图（鸟瞰角度）
- 场景：{scene_desc}
- 角色位置：{character_desc}
- 运动轨迹：{shot_data.get('action', '')}

**关键元素**：
- 角色A起始位置：画面左侧
- 角色A运动方向：→ 向右移动
- 镜头运动：{shot_data.get('camera_movement', '')}
- 情绪氛围：{shot_data.get('emotion', '')}

**提示词**：
{style}，场景概念设计图，俯视图，鸟瞰角度，展示角色在空间中的位置和运动轨迹，清晰的构图布局，建筑蓝图风格，标注角色位置和运动方向，{shot_data.get('emotion', '')}氛围，8K

**负面排除**：
no [细节过多, 透视错误, 角色比例失调, 混乱的布局]
"""


def _generate_story_board(shot_data: Dict, style: str) -> str:
    """生成故事板 - 多个镜头并排展示叙事逻辑"""
    
    # 故事板通常包含3-5个关键帧
    key_frames = [
        ("开始", "0s", shot_data.get('emotion', '')),
        ("发展", "5s", shot_data.get('emotion', '')),
        ("高潮", f"{shot_data.get('duration', 10)}s", shot_data.get('emotion', ''))
    ]
    
    frames_text = ""
    for i, (phase, time, emotion) in enumerate(key_frames, 1):
        frames_text += f"**第{i}帧 [{phase} {time}]**：{emotion}状态\n"
    
    return f"""【故事板】{shot_data.get('shot_id', 'SXX')} | {shot_data.get('duration', 0)}s

**叙事结构**：
{frames_text}
**镜头关系**：
- 景别变化：{shot_data.get('shot_size', '中景')} → 特写
- 运镜方式：{shot_data.get('camera_movement', '')}
- 情绪曲线：从{shot_data.get('emotion', '')}开始，逐步加强

**提示词**：
{style}，故事板，分镜草图，3个连续画面并排展示，每个画面展示不同时间点的关键帧，叙事性强，漫画风格分镜，清晰的镜头编号和时间标注，8K

**负面排除**：
no [画面混乱, 镜头关系不清, 缺乏叙事逻辑, 风格不统一]
"""


def _generate_action_board(shot_data: Dict, style: str, character_desc: str) -> str:
    """生成动作板 - 关键动作的连续帧"""
    
    return f"""【动作板】{shot_data.get('shot_id', 'SXX')} | {shot_data.get('duration', 0)}s

**动作分解**：
- 角色：{character_desc}
- 主要动作：{shot_data.get('action', '')}
- 动作阶段：
  - 第1帧（准备）：身体蓄力，重心下沉
  - 第2帧（发力）：动作爆发，肌肉紧绷
  - 第3帧（完成）：动作结束，惯性延续
  - 第4帧（恢复）：回到平衡状态

**关键姿态**：
- 姿态1：{character_desc} 准备动作
- 姿态2：{character_desc} 发力瞬间
- 姿态3：{character_desc} 动作完成

**提示词**：
{style}，动作板，连续动作分解图，4个连续帧展示同一角色的完整动作过程，每个帧展示不同阶段的姿态，动态线条，运动模糊效果，清晰的姿态变化，8K

**负面排除**：
no [姿态僵硬, 动作不连贯, 角色变形, 比例失调]
"""


def _generate_full_dimension_board(shot_data: Dict, style: str, character_desc: str, scene_desc: str) -> str:
    """生成全维度板 - 场景+角色+动作+光影+情绪"""
    
    return f"""【全维度板】{shot_data.get('shot_id', 'SXX')} | {shot_data.get('duration', 0)}s | {shot_data.get('location', '')}

**场景空间**：
- 环境：{scene_desc}
- 空间层次：前景/中景/远景
- 关键道具：环境中的细节元素

**角色状态**：
- 角色：{character_desc}
- 表情：{shot_data.get('emotion', '')}
- 动作：{shot_data.get('action', '')}
- 身体语言：情绪外化的肢体表现

**光影氛围**：
- 主光源：自然光/人工光
- 光影效果：高对比/柔光/逆光
- 色温：冷色调/暖色调

**镜头语言**：
- 景别：{shot_data.get('shot_size', '中景')}
- 运镜：{shot_data.get('camera_movement', '')}
- 构图：三分法/对称/对角线

**情绪基调**：
- 核心情绪：{shot_data.get('emotion', '')}
- 氛围关键词：3个描述词

**提示词**：
{style}，全维度概念设计图，展示完整的场景氛围，包含角色{character_desc}在{scene_desc}中的完整状态，{shot_data.get('emotion', '')}情绪，{shot_data.get('camera_movement', '')}运镜，{shot_data.get('shot_size', '')}景别，丰富的细节和层次感，电影级构图，8K

**负面排除**：
no [细节缺失, 氛围不对, 角色与环境割裂, 光影混乱]
"""


def batch_generate_storyboards(
    shots: List[Dict],
    storyboard_type: str,
    style: str = "电影级超写实",
    characters: Dict[str, str] = None,
    scenes: Dict[str, str] = None
) -> str:
    """
    批量生成分镜图提示词
    
    Args:
        shots: 镜头列表，每个镜头是一个字典
        storyboard_type: 分镜图类型
        style: 视觉风格
        characters: 角色描述字典（角色名 → 描述）
        scenes: 场景描述字典（场景名 → 描述）
    
    Returns:
        所有分镜图提示词
    """
    characters = characters or {}
    scenes = scenes or {}
    
    results = []
    for shot in shots:
        character_desc = characters.get(shot.get('character', ''), '角色')
        scene_desc = scenes.get(shot.get('location', ''), '场景')
        
        prompt = generate_storyboard_prompt(
            storyboard_type=storyboard_type,
            shot_data=shot,
            style=style,
            character_desc=character_desc,
            scene_desc=scene_desc
        )
        results.append(prompt)
    
    return "\n\n" + "="*50 + "\n\n".join(results)


# 使用示例
if __name__ == "__main__":
    # 示例镜头数据
    sample_shot = {
        "shot_id": "S03",
        "duration": 10,
        "emotion": "惊奇",
        "location": "麦田中央",
        "action": "男孩触碰到外星生命",
        "camera_movement": "缓慢推进",
        "shot_size": "中景",
        "character": "男孩"
    }
    
    sample_characters = {
        "男孩": "10岁瘦小男孩，穿红色旧外套，眼神警惕但好奇"
    }
    
    sample_scenes = {
        "麦田中央": "金色麦田，微风轻拂，远处地平线"
    }
    
    # 生成4种分镜图
    print("="*50)
    print("调度图")
    print("="*50)
    print(generate_storyboard_prompt("调度图", sample_shot, "电影级超写实", 
                                     sample_characters["男孩"], sample_scenes["麦田中央"]))
    
    print("\n" + "="*50)
    print("故事板")
    print("="*50)
    print(generate_storyboard_prompt("故事板", sample_shot, "电影级超写实"))
    
    print("\n" + "="*50)
    print("动作板")
    print("="*50)
    print(generate_storyboard_prompt("动作板", sample_shot, "电影级超写实", 
                                     sample_characters["男孩"]))
    
    print("\n" + "="*50)
    print("全维度板")
    print("="*50)
    print(generate_storyboard_prompt("全维度板", sample_shot, "电影级超写实",
                                     sample_characters["男孩"], sample_scenes["麦田中央"]))
