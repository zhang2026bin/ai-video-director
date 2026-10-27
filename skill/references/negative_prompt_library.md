# 负面排除词库

来源整理：个人知识库 06-负面排除库.md + AI导演台实践
整合时间：2026-07-07

---

## 使用原则

1. **每个场景选3-5个最关键的**，写太多AI会混乱
2. **针对性写**：写实风重点写"不要塑料感"，古风重点写"不要现代元素"
3. **放在最后**：负面排除词统一放在提示词最后面
4. **具体问题具体加**：生成后发现什么问题，下次加对应排除词

---

## 一、通用必加（每个分镜都加）

```
no deformation, no distorted features, no extra fingers, no missing fingers
no plastic texture, no sticker feel, no cartoon style
no blur, no artifacts, no noise
no inconsistent lighting, no missing shadows
```

---

## 二、按风格分类

### 写实风
```
no perfect symmetry, no over-symmetrical composition
no plastic skin, no porcelain skin, no over-smoothed skin
no fake bokeh, no oversaturated colors
no over-beautified, no airbrushed look
no visible pores missing, no skin without texture
no clothes without wrinkles, no fabric looking like plastic
no overly clean background, no lack of real clutter
no perfect lighting without realistic imperfections
```

### 古风/国风水墨
```
no modern elements, no contemporary clothing
no plastic-looking hanfu, no cheap hair accessories
no anachronistic architecture, no modern buildings
no cartoon style, no sticker feel
no inconsistent lighting direction, no missing shadows
```

### 科幻/赛博朋克
```
no ancient elements, no outdated sci-fi aesthetics
no cheap special effects, no low-budget CG look
no inconsistent technology levels
```

### 非写实风格（儿童绘本/手绘/插画）
```
no realistic photography parameters (no Sony, Canon, Arri brand names)
no ISO values, no film grain, no f/1.4-f/2.8 aperture values
no camera brand names, no lens model numbers
use style descriptors instead of technical camera specs
```

---

## 三、按场景分类

### 人物特写/情绪场景
```
no exaggerated expressions, no distorted facial features
no excessive body movement, no overly dramatic gestures
no busy background stealing attention
no rapid lighting changes disrupting mood
no flashy camera movements interfering with emotion
```

### 战斗/动作场景
```
no extra weapons, no strange equipment
no broken limbs, no overly gory scenes
no deformed weapons, no impossible physics
no floating objects without reason
```

### 逃亡/追逐场景
```
no static poses, no floating idle poses
no standing still, no relaxed posture
no contact with ground (if flying)
no wheels, tires, metal rods, mechanical parts (unless intended)
```

### 神兽/生物场景
```
no cartoon style, no children's illustration style
no merged scales, no deformed claws
no incorrect wing proportions, no unnatural wing movement
no plastic-looking skin/fur texture
no inconsistent lighting, no missing environment light reflection
```

### 场景/环境镜头
```
no perspective errors, no tilted buildings
no incorrect building proportions
no repetitive architectural details (AI copy-paste)
no mixed architectural styles (unless intentional)
no physically impossible structures
```

---

## 四、手部专项（AI高发问题）

```
no extra fingers, no missing fingers
no fused fingers, no deformed fingers
no overly long nails, no strange nail shapes
no disproportionate hands (too large or too small)
no palm without palm lines
```

---

## 五、运镜专项

```
no excessive camera shake
no inconsistent camera speed (sudden speed changes without reason)
no unmotivated direction changes
no abrupt transitions, no overly flashy transitions
no camera always on face (need environment establishment shots)
no all close-ups (viewer loses spatial awareness)
no all wide shots (can't see character expressions)
```

---

## 六、分场景负面排除模板

### 模板A：古风人物视频
```
【负面排除】no modern elements, no plastic hanfu, no distorted features, no extra fingers, no cartoon style, no sticker feel, no inconsistent lighting direction, no missing shadows, no porcelain skin, no over-smoothed skin
```

### 模板B：写实人像视频
```
【负面排除】no perfect symmetry, no plastic texture, no fake bokeh, no oversaturated colors, no over-beautified, no skin without pores, no clothes without wrinkles, no overly clean background, no perfect lighting without realistic imperfections
```

### 模板C：神兽/生物视频
```
【负面排除】no cartoon style, no children's illustration, no merged scales, no deformed claws, no incorrect wing proportions, no unnatural wing movement, no plastic skin/fur texture, no inconsistent lighting, no missing environment light reflection
```

### 模板D：情绪特写视频
```
【负面排除】no exaggerated expressions, no distorted facial features, no excessive body movement, no busy background, no rapid lighting changes, no flashy camera movements, no over-smoothed skin, no plastic texture
```

### 模板E：战斗/动作视频
```
【负面排除】no extra weapons, no strange equipment, no broken limbs, no deformed weapons, no impossible physics, no inconsistent lighting, no extra fingers, no distorted features
```

### 模板F：非写实风格视频（绘本/手绘/插画）
```
【负面排除】no realistic photography parameters, no camera brand names (Sony, Canon, Arri), no ISO values, no film grain, no f/1.4-f/2.8 aperture, no lens model numbers, no photorealistic rendering, no 3D rendering look
```

---

## 七、高级防翻车（从S级提示词提炼）

```
no deformed anatomy, no twisted body
no extra limbs, no six fingers
no lava, no molten rock (unless intended)
no glowing objects (unless intended)
no standing pose (if action required)
no floating idle pose (if movement required)
no side pose (if frontal required)
no static movement (if dynamic required)
```

---

*整理时间：2026-07-07*
*资料来源：个人知识库 AI短视频提示词/06-负面排除库.md*
