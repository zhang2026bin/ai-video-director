#!/usr/bin/env python3
"""
提示词生成器 v25
- 11维场景/角色生图提示词
- AITANG 5维视频提示词
- 角色板提示词
- 故事板提示词
- 红线运镜法提示词
- 21格分镜提示词
- 六段式微距提示词
- 情绪驱动词汇自动选取（表情/动作/运镜）
"""

import json
import sys
import os
from typing import Dict, List, Optional


# ===== 情绪驱动词汇映射（硬编码自references/资料库）=====

# 情绪→表情映射（来源：expression_library.md，含怒10种/喜10种/哀10种/恐惧5种/基础12种）
EMOTION_EXPRESSION = {
    # === 基础情绪 ===
    "悲伤": ["下眼睑向上收缩用力，眼白内眼角1/3变红", "泪珠从下睑内眼角溢出，2秒滑到下颌线", "眉头向内收缩形成八字眉"],
    "愤怒": ["眉头紧锁眉心上扬，额头出现纵向皱纹", "鼻翼扩张，鼻孔翕动", "下唇被上排牙齿轻咬，唇缘因压迫泛白"],
    "喜悦": ["颧大肌收缩带动嘴角上扬15-20度", "眼轮匝肌收缩，眼角出现鱼尾纹", "脸颊肌肉上提，眼睛眯起"],
    "恐惧": ["瞳孔放大10%，眼白露出面积增加", "眉毛向中间聚拢并上扬", "下唇微微颤抖"],
    "惊讶": ["眉毛高抬，额头出现横向抬头纹", "眼睛睁大，瞳孔快速收缩", "嘴巴张开，下巴放松下垂"],
    "厌恶": ["上唇上提，鼻翼两侧出现皱褶", "眉毛下压，眼睛微眯", "嘴角向下撇，下巴收紧"],
    "温柔": ["眼神柔和，瞳孔轻微放大", "嘴角微扬不超过5度", "眉头舒展，额头平滑"],
    "坚定": ["眼神聚焦，瞳孔稳定不游移", "下颌收紧，咬肌微微隆起", "眉头平直不皱"],
    # === 怒系细化（来源：expression_library.md 怒10种）===
    "咬牙切齿": ["牙关紧咬，太阳穴青筋微凸，眼神凶狠，鼻翼微微扩张", "眉毛向下压成倒八字，眼神锋利，嘴唇抿紧", "额头青筋微凸，嘴唇颤抖，呼吸急促"],
    "暴怒": ["嘴巴张大呈吼叫状，眉毛上扬，眼神瞪大，额头青筋暴起", "牙关紧咬太阳穴青筋暴起，全身肌肉紧绷", "鼻翼扩张到极限，眼神像要喷火"],
    "冷怒": ["眼神冰冷，嘴角微抿，下巴微抬，面无表情但压迫感强", "表情完全放松但眼神冷冽，嘴角平直或微微下压", "单边嘴角上扬，眼睛斜视，下巴微抬"],
    "隐忍": ["下唇被上排牙齿轻咬1毫米深度，唇缘因压迫泛白", "眼眶泛红但眉头紧蹙，嘴唇抿紧，下巴肌肉紧绷", "两侧嘴角同时向下微撇2-3毫米"],
    # === 喜系细化（来源：expression_library.md 喜10种）===
    "微笑": ["嘴角微微上扬，眼睛弯成月牙，脸颊有淡淡笑纹，眼神温柔", "嘴角轻轻翘起，眼睛含情脉脉，脸颊微红", "嘴角温柔上扬，眼角细纹微微出现，眼神柔软"],
    "大笑": ["嘴巴张开露齿，眼睛眯成缝，眼角有笑纹，头微微后仰", "颧大肌全力收缩，嘴角上扬超过30度，整个面部参与", "嘴巴大张露齿，眼角鱼尾纹深度加深，头向后仰"],
    "苦笑": ["嘴角勉强上扬但眼睛没有笑意，眉头微蹙，眼神带着无奈", "一侧嘴角微扬另一侧下垂，眼神空洞", "嘴角上扬幅度不对称，眉头紧锁"],
    # === 哀系细化（来源：expression_library.md 哀10种）===
    "隐忍不哭": ["眼眶泛红但眉头紧蹙，嘴唇抿紧，下巴肌肉紧绷，鼻翼微缩", "眼泪在眼眶打转但不落下，嘴唇因用力抿紧泛白", "眉头向内收缩形成八字眉，额头平滑无抬头纹"],
    "崩溃": ["双眼紧闭，嘴巴大张呈哭喊状，泪水大量涌出，表情扭曲", "面部肌肉全部收紧，青筋暴起，泪水混合鼻涕", "嘴巴大张到极限，眼睛紧闭或瞪大"],
    "失神": ["眼神空洞失焦，瞳孔放大，表情僵硬，嘴角平直", "眼睛睁大但不眨，瞳孔不聚焦于任何物体", "面部所有肌肉松弛，表情完全空白"],
    "委屈": ["下唇前伸，嘴唇嘟起，眉头微蹙，眼神躲闪，一脸委屈", "眼眶泛红，下唇颤抖，鼻尖泛红", "嘴巴瘪起，下巴肌肉紧绷，眼泪在眼眶打转"],
    # === 恐惧细化（来源：expression_library.md 恐惧5种）===
    "惊恐": ["眉毛上扬、眼睛瞪大露出上方窄条巩膜、嘴巴微张、鼻翼收缩、面色苍白", "瞳孔放大10%，眼白露出面积增加，额头冒汗", "嘴巴张开下巴放松下垂，双手下意识护住面部"],
    "绝望": ["眉毛上挑成八字、眼眶泛红、嘴巴张开呈哀求状、下巴肌肉紧绷", "双眼紧闭眉头紧皱嘴角下拉，满脸绝望", "牙关紧咬但嘴唇颤抖，眼神惊恐不断回望"],
    # === 其他常用 ===
    "思考": ["眼神失焦看向斜上方，手指轻敲太阳穴", "眉头微蹙，嘴唇微抿，眼球缓慢转动", "头部微歪，眼神聚焦在某一点但不眨"],
    "犹豫": ["目光游移不敢对视，手指无意识搓动", "嘴唇抿紧又张开，视线在两个方向反复移动", "一手摸下巴手指轻捻，身体左右轻微摇晃"],
    "平静": ["面部肌肉完全放松，呼吸均匀，眼神温和", "眉头舒展，嘴角自然平直，瞳孔稳定", "表情淡然，不悲不喜，视线平直"],
}

# 情绪→动作映射（来源：action_library.md 含10种情绪肢体语言+8种战斗+6种逃跑+8种手部）
EMOTION_ACTION = {
    # === 基础情绪 ===
    "悲伤": ["肩膀耷拉，头低垂，双臂无力垂在身侧，步伐沉重", "偶尔抬手擦眼角，嘴角下拉，全身动作幅度缩小到最小", "身体蜷缩，重心降低，双手捂住面部"],
    "愤怒": ["牙关紧咬，太阳穴青筋微凸，拳头攥紧指节发白，肩膀绷紧，身体微微前倾呈进攻姿态", "猛地站起或拍桌，肩膀前倾身体前压", "反向预备：肩膀先向后转→腰部带动→拳头沿直线冲出"],
    "喜悦": ["双手举起或拍手，身体轻快地左右摇摆", "跳跃或原地转圈，脚步轻盈", "肩膀自然下沉，手臂松松垂在身侧，呼吸缓慢深长"],
    "恐惧": ["身体蜷缩，双臂环抱胸前，肩膀耸起护住脖子，眼睛瞪大瞳孔收缩，不断左右扫视", "双手护住胸口或面部，脚步后退，重心不稳", "身体后缩，肩膀收紧，呼吸急促浅短"],
    "思考": ["一手托腮，手指轻敲太阳穴，头部微歪", "抬头看向远方，眼神失焦", "来回踱步，步伐缓慢"],
    "犹豫": ["一只手伸出一半又缩回，重心在两只脚之间来回切换，视线在两个方向反复移动", "一手摸下巴，手指轻捻，嘴唇抿紧又张开", "身体左右轻微摇晃，目光游移不敢对视"],
    "坚定": ["下巴微抬，肩膀后展，双脚站稳与肩同宽，双手握拳垂在身侧，眼神直视前方不移开", "呼吸平稳深长，全身肌肉稳定不晃", "身体微微前倾但不失重心，脚步沉稳"],
    "温柔": ["手指以极轻力度触碰对方手背，肩膀放松微向对方倾斜", "头部微歪15度，视线柔和不直视", "呼吸平缓，动作幅度缩小到最小，每个动作带缓冲"],
    # === 细化情绪 ===
    "绝望": ["双手抱头，身体蜷缩，肩膀剧烈起伏（哭泣）", "身体僵直不动，双手无力垂下，眼神空洞失焦，全身肌肉失去张力", "膝盖弯曲身体下沉，最终跪倒在地"],
    "警惕": ["身体微微侧转减小暴露面积，一只手搭在武器上，脚步放轻脚跟先着地", "头部缓慢扫视四周，瞳孔收缩，呼吸变浅变轻", "重心压低，随时准备爆发"],
    "忠诚/守护": ["身体微微侧向被守护者，一只手搭在对方肩上或挡在身前", "目光扫视四周保持警戒，下巴微收，肩膀宽阔呈保护姿态", "脚步跟随被守护者移动，始终保持半步距离"],
    "如释重负": ["紧绷的身体突然松弛，肩膀下沉，头微后仰，双眼闭合", "深呼一口气，嘴唇微张，手指从紧握状态逐根展开", "全身肌肉从紧绷→松弛的可见变化过程1.5秒"],
    "崩溃": ["双手抱头身体蜷缩，肩膀剧烈起伏", "面部肌肉全部收紧青筋暴起，嘴巴大张呈哭喊状", "膝盖发软身体下沉，双手撑地或抓握身边物体"],
    "疲惫": ["肩膀耷拉背微驼，重心偏向一条腿，一只手揉着后颈或太阳穴", "步履缓慢略带拖沓，步幅短，肩膀下垂，手臂摆动幅度小", "坐姿时身体前倾蜷缩，手肘撑在膝上，手指插进头发里"],
}

# 情绪→运镜映射（来源：camera_movement_guide.md 含情绪→镜头组合公式）
EMOTION_CAMERA = {
    "悲伤": ["缓慢拉远", "固定镜头", "特写固定→缓慢拉远→孤独广角"],
    "愤怒": ["快速推入", "手持晃动", "快速变焦+跳切+低角度仰拍"],
    "喜悦": ["环绕旋转", "跟拍", "平视中景"],
    "恐惧": ["手持晃动", "快速推入+倾斜构图", "高角度俯视"],
    "紧张": ["快速推入", "手持晃动", "侧面平推"],
    "沉思": ["缓慢推入", "固定镜头", "特写"],
    "回忆": ["缓慢拉远", "固定镜头", "柔焦"],
    "坚定": ["固定镜头", "缓慢推入", "正面中景"],
    "孤独/绝望": ["高角度俯视", "后退疏远", "群像拉远，人物偏小"],
    "浪漫/温馨": ["缓慢推入+柔焦", "微距缓推", "慢速3-5秒/镜"],
    "英雄/胜利": ["环绕旋转", "终极技拉升", "慢动作"],
}

# 语速标准（字/秒）
SPEECH_SPEED = {
    "极慢": 2.0,  # 金句/哲理/独白
    "慢速": 2.5,  # 悲伤/温柔/回忆
    "中速": 3.5,  # 日常对话
    "快速": 4.0,  # 愤怒/激动/紧张
}

# ===== 风格锁定后缀（来源：SKILL.md 风格锁定后缀速查）=====
STYLE_SUFFIX = {
    "3D毛绒": "3D cartoon Pixar-style rendering, soft velvety matte finish, rounded edges, NOT photograph, NOT real footage, NOT 3D render",
    "电影级数字插画": "cinematic digital illustration style, semi-realistic rendering, artistic painterly quality, NOT photograph, NOT real footage",
    "国风水墨": "ink wash painting style, brush strokes, cold blue moonlight, rice paper texture, NOT photograph, NOT real footage, NOT 3D render",
    "写实人像": "cinematic photorealistic, natural skin texture, subtle film grain, NOT anime, NOT cartoon, NOT CG plastic",
    "粘土/定格": "clay texture, fingerprints visible, matte finish, paint layers, brush strokes, slightly bumpy surface, stop-motion lighting, small studio setup",
}

# ===== 质感锚点速查（来源：SKILL.md 质感锚点速查）=====
# 每次只选1-2个锚点强化，避免模型注意力分散
TEXTURE_ANCHORS = {
    "写实人像": {
        "皮肤/表面": "通透肤质+自然毛孔+微血色感+无磨皮痕迹",
        "毛发/发丝": "根根分明+自然蓬松+发际线清晰",
        "五官细节": "眼窝自然阴影+鼻梁高光柔和+唇部湿润感",
        "光影搭配": "侧逆光+窗边自然光+阴影柔和过渡",
    },
    "3D毛绒": {
        "皮肤/表面": "fluffy wool texture+felt material+soft fibers visible",
        "毛发/发丝": "wool fiber direction+slightly uneven surface",
        "五官细节": "button eyes+wool ball joints",
        "光影搭配": "soft diffused light+warm ambient glow+fuzzy edges",
    },
    "水墨/敦煌": {
        "皮肤/表面": "壁画肌理+矿物颜料色+宣纸纹理",
        "毛发/发丝": "飞白笔意+浓淡墨色",
        "五官细节": "线条晕染+留白呼吸",
        "光影搭配": "石青石绿朱砂矿物色+千年斑驳",
    },
    "粘土/定格": {
        "皮肤/表面": "clay texture+fingerprints visible+matte finish",
        "毛发/发丝": "paint layers+brush strokes",
        "五官细节": "slightly bumpy surface",
        "光影搭配": "stop-motion lighting+small studio setup",
    },
}

# ===== 真实感5大避坑规则（来源：SKILL.md）=====
REALISM_RULES = [
    {"规则": "不完美=真实", "说明": "皮肤太光滑=假，必须加毛孔/雀斑/肤色不均/血丝"},
    {"规则": "禁止幻想语言", "说明": "不用magical/ethereal/dreamlike，改用captured/shot on/natural daylight"},
    {"规则": "色彩克制", "说明": "不用vivid/bright/vibrant，改用soft/muted/olive-toned"},
    {"规则": "背景不能忽略", "说明": "背景不真实=全图穿帮，给背景同等光照+景深+细节"},
    {"规则": "负向词必须具体", "说明": "不写no bad quality，写no CG plastic, no blurry, no distorted hands, no unrealistic lighting"},
]

# ===== 3锁定保一致性参数（来源：SKILL.md）=====
CONSISTENCY_LOCKS = {
    "锁构图": "主体占画面60%+景深虚化，每张图保持相同构图比例",
    "锁风格Token": "固定风格词组合全程不变（如3D cartoon Pixar-style rendering, soft velvety matte finish复制到每镜）",
    "锁视觉层级": "前景20%+中景60%+远景20%，每张图保持相同空间分配",
}

# ===== 色彩叙事规则（来源：SKILL.md + director_knowledge.md）=====
COLOR_NARRATIVE = {
    "暖色": "温暖/希望/安全",
    "冷色": "孤独/压抑/疏离",
    "红色": "危险/激情/冲突",
    "蓝色": "冷静/忧郁/科技",
    "绿色": "生命/成长/自然",
    "黄色": "希望/活力/警告",
    "紫色": "神秘/高贵/不安",
    "黑色": "死亡/未知/压迫",
    "白色": "纯洁/空虚/终结",
    "金色": "神圣/财富/回忆",
}

# ===== 情绪→专属光影（来源：SKILL.md 铁律4 五感法）=====
EMOTION_LIGHTING = {
    "温柔": "暖调侧柔光",
    "隐忍": "冷调侧光",
    "爆发": "硬光侧影明暗对比",
    "悲伤": "低色温侧光+阴影面积大",
    "恐惧": "底光+冷色温+高对比",
    "喜悦": "正面柔光+暖色温+高调",
    "愤怒": "底光或侧硬光+红色调",
    "回忆": "柔焦+暖黄调+低对比+光晕",
    "坚定": "正面光+中等色温+阴影清晰",
    "孤独": "侧逆光+冷色温+大面积阴影",
}

# 情绪→语速映射
EMOTION_SPEED = {
    "愤怒": "快速",
    "激动": "快速",
    "紧张": "快速",
    "恐惧": "快速",
    "日常": "中速",
    "轻松": "中速",
    "愉快": "中速",
    "悲伤": "慢速",
    "温柔": "慢速",
    "回忆": "慢速",
    "感悟": "极慢",
    "坚定": "极慢",
}


def generate_11dim_prompt(params: Dict) -> Dict:
    """
    生成11维场景/角色提示词。
    输入:
    {
        "type": "scene" | "character",
        "dimensions": {
            "1_scene": "...",
            "2_worldview": "...",
            "3_subject_detail": "...",
            "4_space_structure": "...",
            "5_time_weather": "...",
            "6_lighting": "...",
            "7_color_tone": "...",
            "8_lens": "...",
            "9_atmosphere": "...",
            "10_quality_style": "...",
            "11_negative": "..."
        }
    }
    """
    dim = params.get("dimensions", {})
    prompt_type = params.get("type", "scene")
    
    # 校验11维完整性
    dimension_keys = [
        "1_scene", "2_worldview", "3_subject_detail", "4_space_structure",
        "5_time_weather", "6_lighting", "7_color_tone", "8_lens",
        "9_atmosphere", "10_quality_style", "11_negative"
    ]
    
    missing = [k for k in dimension_keys if not dim.get(k)]
    if missing:
        return {
            "valid": False,
            "error": f"缺少维度: {', '.join(missing)}",
            "missing_dimensions": missing
        }
    
    # 场景类型：绘图指令无人物
    if prompt_type == "scene":
        scene_constraint = "empty scenery only, no people, no human figures, no body parts, no clothing, no hands, no faces"
        subject_desc = dim["3_subject_detail"]  # 场景主体是空间/物体，不是人
    else:
        scene_constraint = ""
        subject_desc = dim["3_subject_detail"]
    
    # 组合提示词
    parts = [
        f"A {dim['2_worldview']} style scene: {dim['1_scene']}.",
        f"Subject: {subject_desc}.",
        f"Composition: {dim['4_space_structure']}.",
        f"Time and weather: {dim['5_time_weather']}.",
        f"Lighting: {dim['6_lighting']}.",
        f"Color palette: {dim['7_color_tone']}.",
        f"Camera: {dim['8_lens']}.",
        f"Mood: {dim['9_atmosphere']}.",
        f"Quality: {dim['10_quality_style']}.",
    ]
    
    if scene_constraint:
        parts.append(f"IMPORTANT: {scene_constraint}.")
    
    parts.append(f"Negative prompt: {dim['11_negative']}.")
    
    prompt_text = " ".join(parts)
    
    # 镜头参数摘要
    lens_summary = dim.get("8_lens", "未指定")
    
    return {
        "valid": True,
        "type": prompt_type,
        "prompt": prompt_text,
        "lens_summary": lens_summary,
        "dimensions_filled": len([k for k in dimension_keys if dim.get(k)]),
        "total_dimensions": 11
    }


def generate_aitang_video_prompt(params: Dict) -> Dict:
    """
    生成AITANG 5维视频提示词。
    输入:
    {
        "reference_images": {
            "character": "图片X",
            "scene": "图片Y",
            "storyboard": "图片Z"
        },
        "shot_count": N,
        "duration_seconds": N,
        "beat_logic": "分镜与动作逻辑描述",
        "rhythm": "节奏描述",
        "character_physics": "角色物理细节描述",
        "scene_lens": "场景与镜头风格描述",
        "final_beat": "最终节拍处理描述"
    }
    """
    ref = params.get("reference_images", {})
    shot_count = params.get("shot_count", 1)
    duration = params.get("duration_seconds", 5)
    
    # 校验5维完整性
    required_fields = [
        ("beat_logic", "分镜与动作逻辑"),
        ("rhythm", "时长与节奏"),
        ("character_physics", "角色设定与物理细节"),
        ("scene_lens", "场景与镜头风格"),
        ("final_beat", "最终节拍处理")
    ]
    
    missing = []
    for field, label in required_fields:
        if not params.get(field):
            missing.append(label)
    
    if missing:
        return {
            "valid": False,
            "error": f"缺少维度: {', '.join(missing)}",
            "missing_dimensions": missing
        }
    
    # 组合参考素材声明
    ref_parts = []
    if ref.get("character"):
        ref_parts.append(f"角色@{ref['character']}")
    if ref.get("scene"):
        ref_parts.append(f"场景@{ref['scene']}")
    if ref.get("storyboard"):
        ref_parts.append(f"故事板@{ref['storyboard']}")
    
    ref_line = f"参考素材：{', '.join(ref_parts)}" if ref_parts else ""
    
    # 组合5维提示词
    prompt = f"""{ref_line}

1.分镜与动作逻辑
蓝图声明：使用故事板作为完整视觉和动作来源，从左到右、从上到下依次遵循所有{shot_count}个镜头；不得重新诠释动作、姿势、镜头角度或能量递进。
{params['beat_logic']}

2.时长与节奏
节奏声明：将完整的{shot_count}镜头序列压缩到{duration}秒，每个节拍必须清晰呈现为动作快照，不能是冗长拖沓的动作；使用紧凑节奏+快速剪辑+流畅转场，最终节拍前不松懈不停顿。
{params['rhythm']}

3.角色设定与物理细节
动态物理：呼吸/肌肉紧绷/汗水/摩擦变形，不是静态描述。
{params['character_physics']}

4.场景与镜头风格
环境4层：空间+光源+材质+质感。镜头：具体角度+运动方式+光影效果。
{params['scene_lens']}

5.最终节拍处理
定格收尾，与故事板最后一格一致。
{params['final_beat']}"""
    
    return {
        "valid": True,
        "prompt": prompt,
        "dimensions_filled": 5,
        "total_dimensions": 5,
        "shot_count": shot_count,
        "duration_seconds": duration
    }


def generate_character_board_prompt(params: Dict) -> Dict:
    """生成AITANG角色板提示词"""
    char_name = params.get("name", "未命名角色")
    reference_image = params.get("reference_image", "@参考图像")
    role = params.get("role", "")
    core_emotion = params.get("core_emotion", "")
    visual_sign = params.get("visual_sign", "")
    
    prompt = f"""创建一张艺术性的16:9角色身份板。

核心要求：
- [主体]: {reference_image}
- 背景：纯白色/柔和米白色，无环境/道具/标志/水印

设计方向：
不要标准角色参考表，要电影般的身份板——高端动画工作室角色研究与艺术书布局的结合。
布局不对称、优雅、视觉难忘，大片留白、多样化图像比例、有意的不平衡。

布局规则：
- 不要重叠任何角色图像
- 每个视角有清晰分离和呼吸空间
- 无裁剪面部/隐藏肢体/堆叠人物/合并姿势

主要构图：
放置一个大型英雄全身视角，略微偏离中心作为视觉锚点。围绕它排列较小的辅助研究：
中性全身/背面/侧面/坐姿/倾斜/蹲姿/俯视/仰视/富有表现力的肖像。
每个视角是独立干净的角色研究。

身份锁定6要素：
相同面部 + 相同面部比例 + 相同发型 + 相同服装 + 相同身体比例 + 相同姿势语言

艺术性部分：
- 小轮廓研究区：2-3个简化黑色角色轮廓
- 小表情研究区：细微情感变化
- 小细节研究区：面部/头发/服装关键视觉特征

文本设计：
时尚角色ID块，简约大胆艺术导向：{char_name} / {role} / {core_emotion} / {visual_sign}"""
    
    return {"valid": True, "prompt": prompt, "character": char_name}


def generate_storyboard_prompt(params: Dict) -> Dict:
    """生成故事板提示词"""
    board_type = params.get("type", "12grid")
    character_ref = params.get("character_ref", "@角色图")
    
    if board_type == "12grid":
        prompt = f"""参考{character_ref}，创建分镜动作故事板，16:9画幅，12个电影风格面板，黑白粗糙铅笔线条。

颜色标注系统：
🔴红色=机位运动/镜头调度 🔵蓝色=角色动作轨迹 🟢绿色=互动关系
🟠橙色=效果/冲击力 🟣紫色=音效/标注 ⚫黑色=补充标注

动作设计要求：
- 明确双方侧重招式
- 拳拳到肉的打击感与动态张力
- 好莱坞动作电影风格摄影技巧
- 极简环境元素
- 以定格姿势收尾"""
        
    elif board_type == "21grid":
        prompt = f"""参考角色{character_ref}，创建电影感的21格项目网格单图，3列×7行，专业体育摄影序列风格。
每个面板左上角标1-21序号，底部大写无衬线字体加粗白色标题。

节奏设计：
1-3 FIRST BREATH（极慢→蓄势）
4-6 FIRST MOVE（快速爆发）
7-9 FOOTWORK（中速地面动作）
10-12 THE SPIN（加速旋转定格）
13-17 SLOW MOTION（极快高潮）
18-21 THE LANDING（减速→定格收尾）"""
    else:
        return {"valid": False, "error": f"不支持的故事板类型: {board_type}"}
    
    return {"valid": True, "prompt": prompt, "type": board_type}


def generate_redline_prompt(params: Dict) -> Dict:
    """生成红线运镜法提示词"""
    scene_ref = params.get("scene_ref", "@场景图")
    path_ref = params.get("path_ref", "@红线路径图")
    movement_desc = params.get("movement_desc", "从入口切入→环绕主体→穿越走廊→冲刺出口")
    
    prompt = f"""参考素材：场景参考{scene_ref}，摄像机运动路径参考{path_ref}中的红色路径

核心指令：
完全按照红箭头的红色路径生成视频画面。创建第一人称一镜到底的FPV无人机镜头，电影感，速度节奏：快→慢→快。

红线仅作为摄像机运动路径参考，不要出现在最终视频画面中。

运镜描述：{movement_desc}

禁忌：不要有红线/箭头/文字/水印，一镜到底不要剪辑，不要失真建筑比例"""
    
    return {"valid": True, "prompt": prompt}


def generate_macro_prompt(params: Dict) -> Dict:
    """生成六段式微距提示词"""
    prompt = f"""1.镜头基础：{params.get('lens', '100mm macro / f2.8 / 浅景深 / 窄FOV')}
2.场景信息：{params.get('scene', '微观环境 / 细腻材质 / 侧逆光 / 暖色温')}
3.运动信息：{params.get('movement', '缓慢推近 / 主体微动')}
4.物理时间互动：{params.get('physics', '弹性变形 + 慢速 + 环境微颤反馈')}
5.细节：{params.get('detail', '微观纹理 / 光影粒子 / 材质反射')}
6.收尾：{params.get('ending', '定格 / 焦点锁定 / 情绪落点')}"""
    
    return {"valid": True, "prompt": prompt}


def get_emotion_words(emotion: str, style: str = "") -> Dict:
    """
    根据情绪自动选取表情、动作、运镜、语速、光影。
    来源：expression_library.md / action_library.md / camera_movement_guide.md / SKILL.md
    返回所有候选项（每种情绪3个表情/3个动作/3个运镜），由导演按需选取。
    """
    if not emotion:
        return {
            "valid": False,
            "error": "未提供情绪参数"
        }
    
    # 从映射表中获取全部候选
    expressions = EMOTION_EXPRESSION.get(emotion, ["中性表情"])
    actions = EMOTION_ACTION.get(emotion, ["自然站立"])
    cameras = EMOTION_CAMERA.get(emotion, ["固定镜头"])
    speed = EMOTION_SPEED.get(emotion, "中速")
    lighting = EMOTION_LIGHTING.get(emotion, "自然光")
    
    result = {
        "valid": True,
        "emotion": emotion,
        "expressions": expressions,  # 3个候选表情
        "actions": actions,  # 3个候选动作
        "cameras": cameras,  # 3个候选运镜
        "speed_tier": speed,
        "speed_value": SPEECH_SPEED[speed],
        "lighting": lighting,
    }
    
    # 如果指定了风格，附加风格相关配置
    if style:
        result["style_suffix"] = STYLE_SUFFIX.get(style, "")
        result["texture_anchors"] = TEXTURE_ANCHORS.get(style, {})
    
    return result


def get_style_config(style: str) -> Dict:
    """获取指定风格的完整配置：后缀+质感锚点+真实感规则+一致性锁定"""
    return {
        "valid": style in STYLE_SUFFIX,
        "style": style,
        "suffix": STYLE_SUFFIX.get(style, ""),
        "texture_anchors": TEXTURE_ANCHORS.get(style, {}),
        "realism_rules": REALISM_RULES,
        "consistency_locks": CONSISTENCY_LOCKS,
    }


def validate_realism(prompt: str) -> Dict:
    """
    检查提示词是否违反真实感5大避坑规则。
    返回违规项列表。
    """
    violations = []
    prompt_lower = prompt.lower()
    
    # 规则1：检查是否用了幻想语言
    fantasy_words = ["magical", "ethereal", "dreamlike", "fantastic", "mystical"]
    for fw in fantasy_words:
        if fw in prompt_lower:
            violations.append({
                "规则": "禁止幻想语言",
                "违规词": fw,
                "建议替换": "captured / shot on / natural daylight"
            })
    
    # 规则2：检查是否用了过度鲜艳色彩词
    vivid_words = ["vivid", "bright", "vibrant", "neon", "fluorescent"]
    for vw in vivid_words:
        if vw in prompt_lower:
            violations.append({
                "规则": "色彩克制",
                "违规词": vw,
                "建议替换": "soft / muted / olive-toned"
            })
    
    # 规则3：检查负向词是否太模糊
    vague_negatives = ["no bad quality", "no bad", "high quality", "best quality", "masterpiece"]
    for vn in vague_negatives:
        if vn in prompt_lower:
            violations.append({
                "规则": "负向词必须具体",
                "违规词": vn,
                "建议替换": "no CG plastic, no blurry, no distorted hands, no unrealistic lighting"
            })
    
    return {
        "valid": len(violations) == 0,
        "violations": violations,
        "checked_rules": len(REALISM_RULES)
    }


def validate_shot_format_v32(shot_prompt: str) -> Dict:
    """
    v32硬性格式校验：检查分镜提示词是否符合新结构。
    
    v32格式要求：
    - 必须在开头定义：【镜头语言】、【风格锁定】、【负面排除】、【音效设计】
    - 时间段内只写该时段特有的情绪+动作+台词+音效
    - 时间段内不重复运镜/景别/风格后缀/负面排除
    
    返回校验结果和违规项。
    """
    import re
    violations = []
    warnings = []
    
    if not shot_prompt or not shot_prompt.strip():
        return {
            "valid": False,
            "error": "提示词为空",
            "violations": ["提示词不能为空"]
        }
    
    lines = shot_prompt.strip().split('\n')
    text = shot_prompt.strip()
    
    # 检查是否有v32必需的结构块
    required_blocks = ['【镜头语言】', '【风格锁定】', '【负面排除】', '【音效设计】', '【本镜参数】']
    missing_blocks = []
    for block in required_blocks:
        if block not in text:
            missing_blocks.append(block)
    
    if missing_blocks:
        violations.append(f"v32缺少必需结构块: {', '.join(missing_blocks)}")
    
    # 检查是否有时间段标记
    time_segments = [line for line in lines if line.strip().startswith('[') and 's-' in line and 's]:' in line]
    if not time_segments:
        violations.append("未找到任何时间段标记，格式应为 [Xs-Ys]:")
    
    # v32检查：时间段内不应重复风格锁定后缀
    for segment in time_segments:
        segment = segment.strip()
        time_match = re.search(r'\[(\d+s)-(\d+s)\]:', segment)
        if not time_match:
            continue
        time_range = time_match.group(0)
        
        # 检查时间段内是否有风格后缀（v32不允许）
        style_keywords = ['style', 'not photograph', 'rendering', 'painting', '8K', '4K']
        has_inline_style = any(kw in segment.lower() for kw in style_keywords)
        if has_inline_style:
            violations.append(f"{time_range}: v32禁止在时间段内写风格后缀，应在开头【风格锁定】中定义")
        
        # 检查时间段内是否有负面排除（v32不允许）
        if re.search(r'\bno\s+\[', segment.lower()):
            violations.append(f"{time_range}: v32禁止在时间段内写负面排除，应在开头【负面排除】中定义")
    
    # 检查【负面排除】块是否有内容
    neg_match = re.search(r'【负面排除】\s*\n(.*?)(?=\n【|\n\[|\Z)', text, re.DOTALL)
    if neg_match:
        neg_content = neg_match.group(1).strip()
        if not neg_content or neg_content == '-':
            warnings.append("【负面排除】块为空，建议添加负面排除词")
    
    return {
        "valid": len(violations) == 0,
        "format": "v32",
        "time_segments_count": len(time_segments),
        "violations": violations,
        "warnings": warnings,
        "summary": f"v32格式校验：{len(time_segments)}个时间段，{len(violations)}个违规，{len(warnings)}个警告"
    }


def validate_emotion_consistency(shots: List[Dict]) -> Dict:
    """
    校验分镜的情绪一致性。
    检查：表情/动作/运镜/光影是否与标注的情绪匹配。
    使用扩充后的完整映射表（22种情绪）。
    """
    issues = []
    warnings = []
    
    for shot in shots:
        shot_num = shot.get("shot_number", "?")
        emotion = shot.get("emotion", "")
        description = shot.get("description", "")
        
        if not emotion:
            continue
        
        # 检查表情是否匹配（从扩充后的映射表选取）
        expected_expressions = EMOTION_EXPRESSION.get(emotion, [])
        if expected_expressions:
            has_match = any(expr in description for expr in expected_expressions)
            if not has_match:
                warnings.append(
                    f"镜头{shot_num}: 情绪'{emotion}'建议使用表情"
                    f"「{expected_expressions[0][:30]}...」等{len(expected_expressions)}个候选，描述中未体现"
                )
        
        # 检查动作是否匹配
        expected_actions = EMOTION_ACTION.get(emotion, [])
        action_desc = shot.get("action", "")
        if expected_actions and action_desc:
            has_action_match = any(act in action_desc for act in expected_actions)
            if not has_action_match:
                warnings.append(
                    f"镜头{shot_num}: 情绪'{emotion}'建议动作"
                    f"「{expected_actions[0][:30]}...」等{len(expected_actions)}个候选，描述中未体现"
                )
        
        # 检查运镜是否匹配
        expected_cameras = EMOTION_CAMERA.get(emotion, [])
        camera_move = shot.get("camera_move", "")
        if expected_cameras and camera_move:
            # 检查是否有部分匹配（因为运镜描述可能包含组合词）
            has_camera_match = any(cam in camera_move for cam in expected_cameras)
            if not has_camera_match:
                warnings.append(
                    f"镜头{shot_num}: 情绪'{emotion}'建议运镜{expected_cameras}，"
                    f"实际使用'{camera_move}'，确认是否有意调整"
                )
        
        # 检查光影是否匹配情绪
        expected_lighting = EMOTION_LIGHTING.get(emotion, "")
        lighting_desc = shot.get("lighting", "")
        if expected_lighting and lighting_desc:
            # 提取关键词匹配
            lighting_keywords = expected_lighting.split("+")
            has_light_match = any(kw in lighting_desc for kw in lighting_keywords)
            if not has_light_match:
                warnings.append(
                    f"镜头{shot_num}: 情绪'{emotion}'建议光影'{expected_lighting}'，"
                    f"实际'{lighting_desc}'，确认是否有意调整"
                )
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "emotion_mappings_count": {
            "expressions": len(EMOTION_EXPRESSION),
            "actions": len(EMOTION_ACTION),
            "cameras": len(EMOTION_CAMERA),
            "lighting": len(EMOTION_LIGHTING),
        }
    }


def generate_prompt(prompt_data: Dict) -> Dict:
    """
    统一入口：根据type调用对应生成器。
    输入:
    {
        "type": "11dim" | "aitang_video" | "character_board" | "storyboard" | "redline" | "macro" | "emotion_words",
        ...对应参数
    }
    """
    prompt_type = prompt_data.get("type", "")
    
    # 特殊处理：情绪词汇查询
    if prompt_type == "emotion_words":
        emotion = prompt_data.get("emotion", "")
        style = prompt_data.get("style", "")
        return get_emotion_words(emotion, style)
    
    # 特殊处理：风格配置查询
    if prompt_type == "style_config":
        style = prompt_data.get("style", "")
        return get_style_config(style)
    
    # 特殊处理：真实感校验
    if prompt_type == "validate_realism":
        prompt = prompt_data.get("prompt", "")
        return validate_realism(prompt)
    
    # 特殊处理：v32分镜格式校验
    if prompt_type == "validate_shot_format_v32":
        shot_prompt = prompt_data.get("shot_prompt", "")
        return validate_shot_format_v32(shot_prompt)
    
    generators = {
        "11dim": generate_11dim_prompt,
        "aitang_video": generate_aitang_video_prompt,
        "character_board": generate_character_board_prompt,
        "storyboard": generate_storyboard_prompt,
        "redline": generate_redline_prompt,
        "macro": generate_macro_prompt,
    }
    
    generator = generators.get(prompt_type)
    if not generator:
        return {
            "valid": False,
            "error": f"未知提示词类型: {prompt_type}",
            "supported_types": list(generators.keys()) + ["emotion_words", "style_config", "validate_realism"]
        }
    
    return generator(prompt_data)


if __name__ == "__main__":
    input_data = json.load(sys.stdin)
    result = generate_prompt(input_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
