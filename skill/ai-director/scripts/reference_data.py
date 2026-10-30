#!/usr/bin/env python3
"""
资料库数据中心 v27
将references/目录下10个资料库的关键数据硬编码为可调用字典/函数。
任何模块可通过 import 直接引用，无需再读md文件。

数据来源：
- expression_library.md → prompt_generator.py EMOTION_EXPRESSION
- action_library.md → prompt_generator.py EMOTION_ACTION
- camera_movement_guide.md → prompt_generator.py EMOTION_CAMERA + shot_validator.py
- sound_effect_library.md → 下方 SOUND_EFFECTS
- scene_templates.md → 下方 SCENE_TEMPLATES
- style_guide.md → 下方 STYLE_GUIDE
- negative_prompt_library.md → 下方 NEGATIVE_PROMPTS
- prompt_frameworks.md → prompt_generator.py 各generate函数
- director_knowledge.md → 下方 DIRECTOR_KNOWLEDGE
- script_optimization_cases.md → 下方 SCRIPT_OPTIMIZATION
"""

from typing import Dict, List, Optional


# ===== 一、音效词库（来源：sound_effect_library.md）=====

SOUND_EFFECTS = {
    "古风/武侠": {
        "环境音": {
            "竹林": "wind through bamboo stalks, bamboo creaking, distant bird cry, leaves rustling",
            "山间": "wind howling through valley, eagle cry distant, rock crumbling, waterfall far away",
            "古镇街巷": "市井喧哗 distant, 马蹄声 intermittent, 叫卖声 far away, 风铃轻响",
            "古宅室内": "wooden floor creaking, candle flickering, wind through window gap, 更漏声 distant",
            "战场": "war drums distant, horse neighing far away, wind across barren field, crows cawing",
            "寺庙": "wooden fish drum, chanting monks distant, wind through eaves, incense crackling",
            "酒馆": "lute playing soft, wine pouring, cup clinking, fire crackling, low laughter",
        },
        "动作音效": {
            "拔剑": "sword sliding from sheath, metallic ring sharp, leather grip tightening",
            "挥剑": "sword swinging through air, sharp whoosh, cloth rustling",
            "格挡": "metal clashing loud, sparks crackling, impact vibration, body grunt",
            "收剑入鞘": "sword entering sheath, metallic click soft, leather strap fastening",
            "轻功落地": "soft footfall on rooftop, tile creaking slightly, cloth settling",
            "飞檐走壁": "rapid footsteps on tiles, tile cracking, cloth flapping in wind",
            "骑马": "horse hooves on dirt road, leather saddle creaking, horse breathing",
            "倒酒": "wine pouring into ceramic cup, liquid splashing softly",
            "摔杯": "ceramic cup shattering on stone floor, liquid splattering",
        },
    },
    "逃亡/追逐": {
        "环境音": {
            "森林逃亡": "dense forest at night, owl hooting, branches swaying, insects chirping",
            "城市夜逃": "empty city streets at night, distant siren, traffic light clicking, wind through alley",
            "荒野奔逃": "open field, wind howling, dry grass rustling, thunder rolling distant",
        },
        "动作音效": {
            "急促脚步-泥地": "frantic footsteps on muddy ground, splashing puddles, heavy breathing",
            "急促脚步-石板": "rapid footsteps on cobblestone echoing, boots scraping, breath ragged",
            "跌倒爬起": "body hitting ground hard, gasp, hands scraping gravel, scrambling up fast",
            "撞门": "heavy wooden door slamming open, hinges groaning, wood splintering",
            "翻墙": "hands grabbing stone wall, boots scraping, fabric tearing, landing thud",
            "树枝挡路": "branches snapping, leaves rustling violently, thorns scratching fabric",
        },
    },
    "悲伤/离别": {
        "环境音": {
            "雨天": "heavy rain on window pane, thunder rumbling very distant, water dripping from eaves",
            "夜晚": "crickets chirping softly, distant clock ticking, wind whispering through curtains",
            "海边": "gentle waves lapping shore, seagull crying distant, wind blowing sand",
            "空房间": "room tone with slight reverb, faucet dripping in distance, refrigerator humming",
        },
        "动作音效": {
            "哭泣": "soft sobbing, shaky breathing, tears hitting fabric, tissue rustling",
            "收拾行李": "zipper closing slowly, fabric folding, suitcase latch clicking",
            "关门离去": "door closing slowly with soft click, footsteps fading down hallway, silence",
            "握手": "skin contact gentle, fingers interlocking, fabric brushing",
            "拥抱": "cloth rustling soft, deep exhale, heartbeat (if close mic)",
        },
    },
    "温馨/治愈": {
        "环境音": {
            "清晨室内": "birds chirping outside window, soft breeze through curtains, kettle beginning to whistle",
            "咖啡馆": "espresso machine steaming, coffee cup clinking on saucer, soft jazz piano, light chatter murmur",
            "壁炉旁": "fireplace crackling warm, logs shifting, cat purring, clock ticking softly",
            "花园": "bees buzzing, flowers swaying in breeze, fountain trickling, distant children laughing",
        },
        "动作音效": {
            "翻书": "pages turning slowly, paper rustling, book spine creaking",
            "倒茶": "hot water pouring into cup, steam hissing softly, spoon stirring clinking",
            "微笑": "soft exhale through nose, fabric shifting as shoulders relax",
            "猫跳上膝": "soft thud, cat kneading fabric, purring starting",
        },
    },
    "史诗/宏大": {
        "环境音": {
            "山脉": "wind howling across peaks, eagle soaring, distant avalanche rumble",
            "海洋风暴": "massive waves crashing, thunder cracking overhead, wind screaming, rain driving hard",
            "古战场": "war horns blowing, thousands of footsteps marching, shields banging, horses charging",
            "神殿": "deep resonance hum, torches crackling, stone echo, chanting choir distant",
        },
        "动作音效": {
            "号角": "deep war horn blast, echoing across valley, reverberation fading",
            "大地震": "deep earth rumble, ground cracking, rocks falling, dust cloud whoosh",
            "巨石落地": "massive stone impact, ground shaking, debris scattering, echo rolling",
            "旗帜飘扬": "fabric flapping violently in wind, wooden pole creaking, rope straining",
        },
    },
    "科幻/奇幻": {
        "环境音": {
            "太空站": "hologram humming, engine rumble low, communication static, air circulation hiss",
            "魔法森林": "mystical chimes, energy crackling softly, glowing particles humming, ancient tree groaning",
            "赛博城市": "neon buzzing, hovercar passing, drone flying overhead, digital billboards flickering",
            "地下城": "water dripping in cave, torch crackling, chain rattling distant, stone echo",
        },
        "动作音效": {
            "激光射击": "energy beam firing, high-pitched zap, impact explosion",
            "传送门": "portal opening with energy swirl, crackling electricity, whoosh of air being pulled",
            "魔法释放": "spell casting chant, energy building hum, burst release, echo decay",
            "机械启动": "servo motors engaging, hydraulics hissing, metal joints rotating, system boot chime",
        },
    },
    "悬疑/恐怖": {
        "环境音": {
            "废弃建筑": "water dripping rhythmically, wind moaning through broken windows, rats scurrying",
            "深夜巷弄": "distant dog barking, flickering neon buzzing, wind carrying paper scraps",
            "地下室": "pipe groaning, boiler humming irregularly, concrete echo, something scratching",
        },
        "动作音效": {
            "门吱呀开": "old door hinge groaning slowly, wood scraping floor, draft of air",
            "脚步回响": "slow footsteps echoing in empty corridor, each step louder, then sudden stop",
            "手机震动": "phone buzzing on hard surface, vibrating across table, sudden in silence",
            "呼吸": "heavy breathing close to microphone, shaky inhale, held breath",
        },
    },
    "日常/生活": {
        "环境音": {
            "早晨家中": "alarm clock beeping, coffee maker brewing, birds outside, distant traffic",
            "办公室": "keyboard typing, phone ringing distant, air conditioning hum, pages turning",
            "厨房": "oil sizzling in pan, knife chopping on cutting board, water running, timer ticking",
            "超市": "shopping cart rolling, checkout beeping, announcements over speaker, murmuring crowd",
        },
        "动作音效": {
            "开门-钥匙": "key turning in lock, door handle pressing, door swinging open",
            "放书包": "backpack dropping on chair with thud, zipper jingling, books shifting inside",
            "脱鞋": "shoes being kicked off, hitting floor, socks on wood floor",
            "喝水": "glass being picked up, water gulping, glass being set down with soft clink",
        },
    },
    "转场音效": {
        "柔和过渡": "gentle whoosh, smooth transition, light airy",
        "科技转场": "sci-fi transition, digital glitch, electronic sweep",
        "翻页转场": "page turning, paper rustling",
        "时间流逝": "clock ticking accelerating, seasons ambiance changing",
        "闪回切入": "high-pitched ring, memory distortion, echo",
        "梦境切换": "underwater muffled, reversed reverb, ethereal chimes",
        "黑场过渡": "all sound fading to silence, single heartbeat, then new scene",
        "冲击转场": "deep bass drop, screen shake sound, then new ambient",
    },
}

# 音效万能公式
SOUND_FORMULA = "主体动作 + 接触材质 + 环境空间 + 远近层次 + 时间变化 + 禁止项"

# 音效避坑规则
SOUND_RULES = [
    "拒绝堆砌：普通镜头保留1-2个核心音效即可",
    "音画同步：脚步声/开门声必须和画面动作对齐",
    "音量层级固定：配音 > BGM > 音效 > 环境音",
    "时空统一：古风禁现代音效，室内不加室外嘈杂",
    "善用留白：高潮反转镜头可完全静音",
    "材质第一：木门/金属门/石门必须区分",
    "力度分级：轻放/中力/猛摔，力度决定情绪强度",
]

# 三层音频体系
AUDIO_LAYERS = {
    "环境音": "底层铺垫，全程循环，音量最低",
    "动作音效": "点对点同步，与画面动作精确对齐",
    "BGM/情绪音": "氛围烘托，根据情绪弧线设计",
}


def get_sound_effects(scene_type: str, action: str = "") -> Dict:
    """根据场景类型获取音效推荐"""
    effects = SOUND_EFFECTS.get(scene_type, {})
    if not effects:
        # 模糊匹配
        for key in SOUND_EFFECTS:
            if key in scene_type or scene_type in key:
                effects = SOUND_EFFECTS[key]
                break
    
    result = {
        "scene_type": scene_type,
        "found": bool(effects),
        "environment_sounds": effects.get("环境音", {}),
        "action_sounds": effects.get("动作音效", {}),
    }
    
    if action:
        # 查找特定动作音效
        action_sounds = effects.get("动作音效", {})
        matched = {k: v for k, v in action_sounds.items() if action in k}
        result["matched_action"] = matched if matched else f"未找到'{action}'，建议用万能公式自定义"
    
    return result


# ===== 二、负面排除词库（来源：negative_prompt_library.md）=====

NEGATIVE_PROMPTS = {
    "通用必加": "no deformation, no distorted features, no extra fingers, no missing fingers, no plastic texture, no sticker feel, no cartoon style, no blur, no artifacts, no noise, no inconsistent lighting, no missing shadows",
    
    "按风格": {
        "写实风": "no perfect symmetry, no plastic skin, no porcelain skin, no over-smoothed skin, no fake bokeh, no oversaturated colors, no over-beautified, no airbrushed look, no visible pores missing, no skin without texture, no clothes without wrinkles, no fabric looking like plastic, no overly clean background, no perfect lighting without realistic imperfections",
        "古风/国风水墨": "no modern elements, no contemporary clothing, no plastic-looking hanfu, no cheap hair accessories, no anachronistic architecture, no modern buildings, no cartoon style, no sticker feel, no inconsistent lighting direction, no missing shadows",
        "科幻/赛博朋克": "no ancient elements, no outdated sci-fi aesthetics, no cheap special effects, no low-budget CG look, no inconsistent technology levels",
        "非写实风格(绘本/手绘/插画)": "no realistic photography parameters, no Sony, no Canon, no Arri brand names, no ISO values, no film grain, no f/1.4-f/2.8 aperture, no camera brand names, no lens model numbers, use style descriptors instead of technical camera specs",
    },
    
    "按场景": {
        "人物特写/情绪": "no exaggerated expressions, no distorted facial features, no excessive body movement, no overly dramatic gestures, no busy background stealing attention, no rapid lighting changes disrupting mood, no flashy camera movements interfering with emotion",
        "战斗/动作": "no extra weapons, no strange equipment, no broken limbs, no overly gory scenes, no deformed weapons, no impossible physics, no floating objects without reason",
        "逃亡/追逐": "no static poses, no floating idle poses, no standing still, no relaxed posture, no contact with ground (if flying)",
        "神兽/生物": "no cartoon style, no children's illustration style, no merged scales, no deformed claws, no incorrect wing proportions, no unnatural wing movement, no plastic-looking skin/fur texture, no inconsistent lighting",
        "场景/环境": "no perspective errors, no tilted buildings, no incorrect building proportions, no repetitive architectural details, no mixed architectural styles, no physically impossible structures",
    },
    
    "手部专项": "no extra fingers, no missing fingers, no fused fingers, no deformed fingers, no overly long nails, no strange nail shapes, no disproportionate hands, no palm without palm lines",
    
    "运镜专项": "no excessive camera shake, no inconsistent camera speed, no unmotivated direction changes, no abrupt transitions, no overly flashy transitions, no camera always on face, no all close-ups, no all wide shots",
    
    "分场景模板": {
        "A-古风人物": "no modern elements, no plastic hanfu, no distorted features, no extra fingers, no cartoon style, no sticker feel, no inconsistent lighting direction, no missing shadows, no porcelain skin, no over-smoothed skin",
        "B-写实人像": "no perfect symmetry, no plastic texture, no fake bokeh, no oversaturated colors, no over-beautified, no skin without pores, no clothes without wrinkles, no overly clean background, no perfect lighting without realistic imperfections",
        "C-神兽/生物": "no cartoon style, no children's illustration, no merged scales, no deformed claws, no incorrect wing proportions, no unnatural wing movement, no plastic skin/fur texture, no inconsistent lighting, no missing environment light reflection",
        "D-情绪特写": "no exaggerated expressions, no distorted facial features, no excessive body movement, no busy background, no rapid lighting changes, no flashy camera movements, no over-smoothed skin, no plastic texture",
        "E-战斗/动作": "no extra weapons, no strange equipment, no broken limbs, no deformed weapons, no impossible physics, no inconsistent lighting, no extra fingers, no distorted features",
        "F-非写实风格": "no realistic photography parameters, no camera brand names (Sony, Canon, Arri), no ISO values, no film grain, no f/1.4-f/2.8 aperture, no lens model numbers, no photorealistic rendering, no 3D rendering look",
    },
    
    "高级防翻车": "no deformed anatomy, no twisted body, no extra limbs, no six fingers, no lava, no molten rock, no glowing objects, no standing pose (if action required), no floating idle pose (if movement required)",
}


def get_negative_prompt(style: str = "", scene: str = "", template: str = "") -> str:
    """根据风格/场景/模板获取负面排除词"""
    if template:
        return NEGATIVE_PROMPTS["分场景模板"].get(template, NEGATIVE_PROMPTS["通用必加"])
    
    parts = [NEGATIVE_PROMPTS["通用必加"]]
    
    if style and style in NEGATIVE_PROMPTS["按风格"]:
        parts.append(NEGATIVE_PROMPTS["按风格"][style])
    
    if scene and scene in NEGATIVE_PROMPTS["按场景"]:
        parts.append(NEGATIVE_PROMPTS["按场景"][scene])
    
    return ", ".join(parts)


# ===== 三、场景模板（来源：scene_templates.md）=====

SCENE_TEMPLATES = {
    "人物+大场景": {
        "结构": "【风格】+【画质】→【人物】谁穿什么什么姿态什么表情 →【环境】在哪里什么建筑 →【构图】什么镜头角度什么引导线 →【对比】渺小人物vs宏大场景 →【光影】什么光源什么色调",
        "适用": "角色进入新空间、建立场景关系",
    },
    "神兽/生物": {
        "结构": "【风格】+【画质】→【主体】什么神兽 →【细节】鳞片/毛发颜色眼睛特征角/翅膀 →【动作】什么动作什么姿态 →【环境】在什么环境 →【真实感】鳞片高光毛发层次光影统一",
        "适用": "奇幻生物、动物特写",
    },
    "文化IP视频": {
        "结构": "【基本信息】多少秒 →【风格定位】极繁主义史诗级 →【运镜方式】→【核心场景】什么奇观 →【文化元素】非遗/传统技艺 →【核心主体】→【细节质感】材质/光影/纹理",
        "适用": "非遗、传统文化、IP推广",
    },
    "情绪特写视频": {
        "结构": "【整体设定】风格+色调+画质 →【分镜1】开场特写局部细节 →【分镜2】面部微表情变化按时间写 →【分镜3】关键动作特写细节 →【分镜4】收尾拉远定格 →【负面排除】",
        "适用": "情绪表达、微表情、内心戏",
    },
    "AIGC导演级五要素": {
        "结构": "1.摄影机与光学设定(视角/焦段/距离/光学效果/运动) → 2.运动动力学(速度/轨迹/残影/变速/参照物) → 3.环境与物理交互(场景搭建/材质/碰撞/流体/重力) → 4.灯光与材质(配色/光源/材质反射) → 5.氛围与情绪(整体基调/细节情绪/收尾定格)",
        "适用": "特效大片/生物/玄幻等高精度复杂场景",
    },
}


def get_scene_template(template_type: str) -> Dict:
    """获取场景模板"""
    return SCENE_TEMPLATES.get(template_type, {
        "valid": False,
        "available": list(SCENE_TEMPLATES.keys())
    })


# ===== 四、风格速查完整库（来源：style_guide.md 60+种）=====

STYLE_GUIDE = {
    "东方美学": {
        "水墨写意": {"关键词": "中国水墨画、留白、泼墨", "视觉": "墨迹晕染、意境悠远、大量留白", "适用": "古风叙事、文人题材"},
        "工笔重彩": {"关键词": "工笔画、细线勾勒、矿物颜料", "视觉": "线条精准、色彩浓重、细节丰富", "适用": "传统人物、花鸟"},
        "敦煌壁画": {"关键词": "敦煌壁画、飞天、唐卡", "视觉": "金底背景、飘带飞扬、斑驳古朴", "适用": "神话/佛教题材"},
        "浮世绘": {"关键词": "浮世绘、木版画、葛饰北斋", "视觉": "平面感、浓墨轮廓线、淡色填充", "适用": "日式题材"},
        "山水青绿": {"关键词": "青绿山水、千里江山图", "视觉": "大青绿设色、山峦层叠", "适用": "山水风光"},
        "汉服古风": {"关键词": "汉服、魏晋风骨", "视觉": "宽袍大袖、严谨形制、古典气质", "适用": "古风人物"},
        "新中式": {"关键词": "新中式、国潮", "视觉": "传统元素解构、现代构图、克制配色", "适用": "现代国风品牌"},
        "武侠水墨": {"关键词": "武侠水墨、江湖、山水剑客", "视觉": "水墨晕染、动态剑光、留白写意", "适用": "武侠动作"},
    },
    "西方艺术": {
        "文艺复兴": {"关键词": "古典主义、解剖学透视", "视觉": "写实三角构图、焦点透视", "适用": "历史/宗教题材"},
        "巴洛克": {"关键词": "明暗对比法、光影戏剧", "视觉": "强烈明暗对比、动感构图", "适用": "戏剧/史诗"},
        "洛可可": {"关键词": "粉彩色调、装饰主义", "视觉": "粉色金色、卷草纹、奢华", "适用": "宫廷/浪漫"},
        "印象派": {"关键词": "松散笔触、光影研究", "视觉": "笔触破碎、光斑、色光混合", "适用": "户外/自然"},
        "超现实主义": {"关键词": "达利、融化的时钟", "视觉": "梦境感、荒诞并置", "适用": "奇幻/梦境"},
        "极简主义": {"关键词": "极少元素、负空间", "视觉": "大面积留白、高度对比", "适用": "品牌/产品"},
    },
    "现代数字艺术": {
        "超写实": {"关键词": "毛孔级细节、以假乱真", "视觉": "极致细节、皮肤纹理、光学真实", "适用": "真人模拟"},
        "电影感": {"关键词": "电影级光照、宽银幕", "视觉": "宽画幅、景深、戏剧光效", "适用": "短片/广告"},
        "概念艺术": {"关键词": "奇幻插画、高细节场景", "视觉": "氛围感强、叙事性强", "适用": "游戏/影视概念"},
        "低多边形": {"关键词": "几何切割面、极简光影", "视觉": "三角面拼接、简约配色", "适用": "科技/抽象"},
        "像素艺术": {"关键词": "8位/16位风格", "视觉": "马赛克颗粒、复古游戏感", "适用": "怀旧/游戏"},
        "扁平插画": {"关键词": "矢量艺术、纯色平涂", "视觉": "无渐变、简洁现代", "适用": "UI/品牌"},
        "渐变插画": {"关键词": "梦幻渐变、柔光", "视觉": "柔和色彩过渡", "适用": "治愈/梦幻"},
        "双重曝光": {"关键词": "叠加影像、剪影融合", "视觉": "两张照片合成", "适用": "艺术/情绪"},
        "故障艺术": {"关键词": "数字腐蚀、数据破坏", "视觉": "色差、错位、信号干扰", "适用": "赛博/前卫"},
    },
    "幻想与科幻": {
        "赛博朋克": {"关键词": "霓虹雨夜、全息广告", "视觉": "霓虹灯光、雨夜街道", "适用": "科幻/反乌托邦"},
        "蒸汽朋克": {"关键词": "黄铜机械、飞艇、齿轮", "视觉": "维多利亚科技、蒸汽动力", "适用": "复古科幻"},
        "废土朋克": {"关键词": "后启示录、废墟辐射", "视觉": "末日废墟、锈蚀建筑", "适用": "末日题材"},
        "黑暗幻想": {"关键词": "残酷美学、阴郁世界", "视觉": "阴暗色调、哥特元素", "适用": "暗黑奇幻"},
        "剑与魔法": {"关键词": "奇幻冒险、龙与地下城", "视觉": "城堡、魔法、战士", "适用": "西幻RPG"},
        "星际科幻": {"关键词": "太空歌剧、星际飞船", "视觉": "宇宙飞船、外星文明", "适用": "太空题材"},
        "维多利亚哥特": {"关键词": "阴暗学府、煤灯夜色", "视觉": "古宅煤灯、神秘学", "适用": "哥特悬疑"},
    },
    "插画与绘本": {
        "儿童绘本": {"关键词": "可爱温馨、明亮配色", "视觉": "圆润造型、明亮色彩、治愈感", "适用": "儿童教育"},
        "暗黑绘本": {"关键词": "阴郁童话", "视觉": "暗黑童话风、阴郁氛围", "适用": "成人童话"},
        "日系动漫": {"关键词": "赛璐璐上色、勾线", "视觉": "勾线描边、平涂上色", "适用": "动漫风"},
        "美式漫画": {"关键词": "粗黑线、漫威风格", "视觉": "粗黑轮廓、动态姿势", "适用": "超级英雄"},
        "欧洲漫画": {"关键词": "清晰线条、水彩质感", "视觉": "清晰线稿、水彩上色", "适用": "叙事漫画"},
        "Q版角色": {"关键词": "大头娃娃、二头身", "视觉": "头大身小、可爱简化", "适用": "萌系/搞笑"},
    },
}


def search_style(keyword: str) -> List[Dict]:
    """根据关键词搜索匹配的风格"""
    results = []
    for category, styles in STYLE_GUIDE.items():
        for name, info in styles.items():
            if (keyword in name or keyword in info["关键词"] or 
                keyword in info["视觉"] or keyword in info["适用"]):
                results.append({
                    "分类": category,
                    "风格": name,
                    **info
                })
    return results


def get_all_styles() -> Dict:
    """获取全部风格列表（按分类）"""
    return {cat: list(styles.keys()) for cat, styles in STYLE_GUIDE.items()}


# ===== 五、导演知识速查（来源：director_knowledge.md）=====

DIRECTOR_KNOWLEDGE = {
    "光影语法": {
        "顶光": {"叙事": "审视/压迫/神性", "场景": "审讯/神启/崩溃"},
        "逆光": {"叙事": "轮廓/神秘/希望", "场景": "角色转身/走出黑暗"},
        "侧光/半面光": {"叙事": "分裂/矛盾/两面", "场景": "角色内心挣扎/秘密"},
        "底光": {"叙事": "恐怖/诡异/非人", "场景": "恐怖片/反派"},
        "柔光/漫射": {"叙事": "温暖/安全/梦境", "场景": "家庭/回忆/童年"},
        "硬光/直射": {"叙事": "真实/残酷/力量", "场景": "纪实/对抗/觉醒"},
        "光源遮挡": {"叙事": "未知/威胁/等待", "场景": "恐怖/悬疑/伏笔"},
    },
    
    "色彩叙事": {
        "暖橙/金色": {"情绪": "温暖/怀旧/希望", "用法": "回忆/家/黎明"},
        "冷蓝/青色": {"情绪": "孤独/压抑/未来", "用法": "深夜/科技/疏离"},
        "红色": {"情绪": "危险/激情/暴力", "用法": "警告/爱情/冲突"},
        "绿色": {"情绪": "自然/病态/不祥", "用法": "森林/毒药/诡异"},
        "黄色": {"情绪": "快乐/病态/警告", "用法": "阳光/腐烂/危险信号"},
        "消色/灰": {"情绪": "绝望/记忆/虚无", "用法": "末日/闪回/失去希望"},
    },
    
    "色彩技巧": {
        "色彩转折": "同一场戏从暖调变冷调=情绪急转（如团聚→争吵）",
        "角色专属色": "每个角色绑一个主色，观众一看色调就知道谁在场",
        "两套世界两套色调": "现实vs梦境/过去vs现在，用色调区分",
    },
    
    "剪辑节奏": {
        "长镜头/慢剪": {"时长": "5秒+", "效果": "沉浸/冥想/焦虑", "场景": "文艺片/恐怖片/等待"},
        "常规节奏": {"时长": "2-4秒", "效果": "流畅叙事", "场景": "大部分叙事段落"},
        "快速剪辑": {"时长": "1-2秒", "效果": "紧张/兴奋/混乱", "场景": "动作戏/蒙太奇/高潮"},
        "极速剪辑": {"时长": "<1秒", "效果": "碎裂/失控/冲击", "场景": "精神崩溃/爆炸/记忆闪回"},
    },
    
    "剪辑铁律": [
        "快→慢的减速比慢→快的加速更有冲击力",
        "安静是最大的音量——快节奏中插一个固定长镜头比再加快切更有力",
        "剪辑点跟音乐节拍走，不跟画面走",
    ],
    
    "音乐情绪映射": {
        "紧张": {"特征": "不协和音+心跳节奏+渐强", "乐器": "弦乐群/合成器"},
        "悲伤": {"特征": "下行旋律+弱音+留白", "乐器": "大提琴/钢琴/单簧管"},
        "温暖": {"特征": "大调+柔和节奏+泛音", "乐器": "木吉他/竖琴/钢琴"},
        "史诗": {"特征": "铜管+打击乐+渐强", "乐器": "交响乐团+合唱"},
        "诡异": {"特征": "微音程+失真+反常节奏", "乐器": "特雷门琴/合成器/水琴"},
        "空灵": {"特征": "长音+混响+极简", "乐器": "人声/电子/环境音"},
    },
    
    "氛围反差公式": [
        "温暖但孤独（家的灯光，窗外无人）",
        "奢华但破败（金漆剥落的宫殿）",
        "童真但诡异（微笑的布偶在暗角）",
        "干净但危险（无菌实验室里的血迹）",
        "精致但腐败（完美蛋糕上的霉斑）",
    ],
    
    "景别序列规则": {
        "远景→中景→近景": "正常推进——聚焦/发现/深入",
        "近景→远景": "震惊/疏离——突然拉开距离/揭示全局",
        "特写→特写": "压迫/紧张——快速剪辑/信息轰炸",
        "远景→远景": "对比/平行——两个空间的并列",
        "中景→特写→中景": "强调后回归——突出细节后回到语境",
    },
}


def get_director_knowledge(category: str, sub_key: str = "") -> Dict:
    """获取导演知识"""
    data = DIRECTOR_KNOWLEDGE.get(category, {})
    if sub_key and isinstance(data, dict):
        return {sub_key: data.get(sub_key, "未找到")}
    return data


# ===== 六、剧本优化案例（来源：script_optimization_cases.md）=====

SCRIPT_OPTIMIZATION = {
    "六大优化维度": [
        {"维度": "视觉化改造", "核心": "把'他说他很伤心'改成动作/表情/环境传达，为每个关键情节点设计视觉锚点"},
        {"维度": "情绪弧线强化", "核心": "绘制情绪曲线(-5到+5)，弧线太平加反转点，太满加留白段"},
        {"维度": "对话精炼", "核心": "删废话，加潜台词，台词要有钩子（金句或情绪爆发点）"},
        {"维度": "场景结构优化", "核心": "删冗余场景，合并同类场景，调整顺序（倒叙/插叙增强悬念）"},
        {"维度": "角色深度挖掘", "核心": "给主角内在矛盾（想要A但害怕B），给配角存在理由，角色弧线要可见"},
        {"维度": "节奏与时长控制", "核心": "根据目标时长调整内容量，标记每场建议时长，高潮给足铺垫快速"},
    ],
    "优化铁律": [
        "Show, don't tell：能用画面说的，绝不用台词",
        "少即是多：信息密度要高，但表现要克制",
        "情绪优先：逻辑可以简化，情绪必须到位",
        "视觉钩子：至少有一个画面让观众记住",
        "留白艺术：不是所有东西都要说透",
        "错位推到极致：情境错位越大，戏剧张力越强",
    ],
    "质量自检": [
        "核心冲突是否一句话说得清？",
        "是否有至少3个视觉锚点？",
        "情绪弧线是否有明显起伏？",
        "每句台词是否都有功能？",
        "是否有至少一个留白段？",
        "优化后是否比原版更有电影感？",
    ],
}


# ===== 七、情绪微表情量化速查（来源：SKILL.md 铁律4）=====

EMOTION_MICRO_EXPRESSION = {
    "温柔浅笑": "嘴角上扬15°+眼轮匝肌轻收缩+眼角极细细纹",
    "苦笑": "嘴角单侧上扬单侧下沉+眉头轻蹙+眼底疲惫",
    "隐忍难过": "眼眶泛红+泪水充盈不落+下唇颤抖+喉结滚动",
    "愤怒隐忍": "眉头紧锁眉心深纹+牙关紧咬腮帮微鼓+拳头攥紧指节发白",
    "崩溃大哭": "泪水汹涌+鼻头泛红+张口哭泣+肩膀剧烈起伏",
}

# 真假笑区分
SMILE_AUTHENTICITY = {
    "真笑": "眼轮匝肌收缩+眼角细纹（ involuntarily）",
    "假笑": "嘴角上扬但眼轮匝肌无收缩+眼神空洞",
}


# ===== 八、5条写法铁律（来源：SKILL.md）=====

FIVE_IRON_RULES = {
    "铁律1-教小孩画画": {
        "核心": "假设AI是会画画但不懂故事的小孩，每句话按字面意思画",
        "要求": ["每个细节说清楚不留模糊", "不写缓缓慢慢微微写秒数", "不写高级好看震撼写具体参数", "表情五官逐一写+量化", "动作写发力起点→路径→终点→用时"],
    },
    "铁律2-指令式>描述式": {
        "核心": "用指令语气而非描述语气",
        "对比": {"描述式(差)": "画面中角色微笑着转身", "指令式(好)": "必须遵循面板顺序，不得重新诠释动作"},
    },
    "铁律3-反面约束+正面指令配对": {
        "核心": "关键动作嵌入'不要X，而是Y'",
        "公式": "[正确行为描述]——不要[常见错误]，而是[精确要求]。先[步骤1]，再[步骤2]。",
    },
    "铁律4-叙事思维": {
        "核心": "写提示词=写小说片段",
        "要求": ["场景构图三层：前景+中景+远景", "五感法：视觉+听觉+触觉+嗅觉+情绪", "人物小说笔法：动作有动机，微表情>大动作"],
    },
    "铁律5-量化禁模糊": {
        "核心": "禁止模糊形容词，用数字替代",
        "替换表": {"缓缓/慢慢/微微": "用2秒从A移到B", "轻轻地": "指尖以2N力度触碰", "大大的/小小的": "占画面60%", "逐渐变化": "0-3秒眉头紧皱→3-5秒眉头舒展", "电影感/高级感": "24mm f5.6深景深胶片颗粒IMAX画幅"},
    },
}


# ===== 九、万能公式汇总 =====

FORMULAS = {
    "动作描写": "[预备动作0.3-0.5秒]→[主动作]→[身体联动反馈]→[环境交互]",
    "动作完整": "[视线/重心预备]→[发力起点]→[动作路径]→[终点状态]→[用时]→[生理反应]→[环境反馈]",
    "打斗动作": "[对抗局势]→[角色发力逻辑]→[动作结果]→[身体反馈]→[环境破坏]",
    "音效设计": "主体动作 + 接触材质 + 环境空间 + 远近层次 + 时间变化 + 禁止项",
    "氛围反差": "主情绪 + 反向裂隙（如温暖但孤独）",
    "情绪微表情": "面部肌肉 + 10秒时间轴 + 肢体微动作 + 专属光影 + 严格避坑",
    "场景构图": "前景(质感细节20%) + 中景(主体动作60%) + 远景(氛围定调20%)",
    "台词时长": "中文字数 ÷ 语速(字/秒) + 标点停顿(秒)",
    "镜头时长": "max(旁白时长, 动作时长, 空间建立时长)",
}
