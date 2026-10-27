# 音效词库（按场景分类）

来源整理：个人知识库 + 网络资料（AI短剧音频设计笔记、AudioLDM-S提示词技巧、Seedance 2.0声画帧锁机制、可灵八层框架）
整合时间：2026-07-07

---

## 核心原则

1. **三层音频体系**：环境音（底层铺垫）+ 动作音效（点对点同步）+ BGM/情绪音（氛围烘托）
2. **音量层级**：配音 > BGM > 动作音效 > 环境音（环境音永远最低）
3. **声源预埋**：不写"清脆敲击声"，写"右手食指敲击青瓷茶盏边缘（特写）"——声源+部位+材质+动作
4. **材质匹配**：木门/金属门/石门声音必须区分，材质错误瞬间出戏
5. **力度匹配**：轻放 vs 猛摔差异明显，力度决定情绪
6. **多层叠加**：真实环境是混合音效，如雨夜 = 雨声(主) + 远处车流(次) + 风声(次) + 零星雷声(点缀)
7. **留白也是设计**：高潮/反转/悬念镜头弱化环境音，只保留动作音效或完全静音
8. **时空逻辑**：古风禁出现汽车/手机音效；室内不加室外嘈杂车流

---

## 一、古风/武侠场景

### 环境音（底层铺垫，全程循环）
```
【竹林】wind through bamboo stalks, bamboo creaking, distant bird cry, leaves rustling
【山间】wind howling through valley, eagle cry distant, rock crumbling, waterfall far away
【古镇街巷】市井喧哗 distant, 马蹄声 intermittent, 叫卖声 far away, 风铃轻响
【古宅室内】wooden floor creaking, candle flickering, wind through window gap, 更漏声 distant
【战场】war drums distant, horse neighing far away, wind across barren field, crows cawing
【寺庙】wooden fish drum, chanting monks distant, wind through eaves, incense crackling
【酒馆】lute playing soft, wine pouring, cup clinking, fire crackling, low laughter
```

### 动作音效（与画面同步）
```
【拔剑】sword sliding from sheath, metallic ring sharp, leather grip tightening
【挥剑】sword swinging through air, sharp whoosh, cloth rustling
【格挡】metal clashing loud, sparks crackling, impact vibration, body grunt
【收剑入鞘】sword entering sheath, metallic click soft, leather strap fastening
【轻功落地】soft footfall on rooftop, tile creaking slightly, cloth settling
【飞檐走壁】rapid footsteps on tiles, tile cracking, cloth flapping in wind
【骑马】horse hooves on dirt road, leather saddle creaking, horse breathing
【倒酒】wine pouring into ceramic cup, liquid splashing softly
【摔杯】ceramic cup shattering on stone floor, liquid splattering
```

### 完整示例（10秒古风对峙）
```
【音效】
[0s-3s] wind through bamboo stalks, leaves rustling, two swords slowly drawn from sheaths | 
[3s-6s] rapid sword clashing, metal ringing, footsteps circling on gravel, cloth flapping | 
[6s-8s] heavy sword strike, deep metallic boom, shockwave whoosh, opponent stumbling back | 
[8s-10s] sword tip touching ground, heavy breathing, wind calming, single bamboo creak
```

---

## 二、逃亡/追逐场景

### 环境音
```
【森林逃亡】dense forest at night, owl hooting, branches swaying, insects chirping
【城市夜逃】empty city streets at night, distant siren, traffic light clicking, wind through alley
【荒野奔逃】open field, wind howling, dry grass rustling, thunder rolling distant
```

### 动作音效
```
【急促脚步-泥地】frantic footsteps on muddy ground, splashing puddles, heavy breathing
【急促脚步-石板】rapid footsteps on cobblestone echoing, boots scraping, breath ragged
【跌倒爬起】body hitting ground hard, gasp, hands scraping gravel, scrambling up fast
【撞门】heavy wooden door slamming open, hinges groaning, wood splintering
【翻墙】hands grabbing stone wall, boots scraping, fabric tearing, landing thud
【树枝挡路】branches snapping, leaves rustling violently, thorns scratching fabric
```

### 完整示例（10秒森林逃亡）
```
【音效】
[0s-3s] frantic footsteps on forest floor, branches snapping, heavy ragged breathing, heart pounding | 
[3s-6s] stumbling over root, body falling, hands scraping wet leaves, gasping | 
[6s-8s] scrambling up fast, boots slipping on mud, desperate breathing louder | 
[8s-10s] sudden silence, only wind and one owl hoot, holding breath
```

---

## 三、悲伤/离别场景

### 环境音
```
【雨天】heavy rain on window pane, thunder rumbling very distant, water dripping from eaves
【夜晚】crickets chirping softly, distant clock ticking, wind whispering through curtains
【海边】gentle waves lapping shore, seagull crying distant, wind blowing sand
【空房间】room tone with slight reverb, faucet dripping in distance, refrigerator humming
```

### 动作音效
```
【哭泣】soft sobbing, shaky breathing, tears hitting fabric, tissue rustling
【收拾行李】zipper closing slowly, fabric folding, suitcase latch clicking
【关门离去】door closing slowly with soft click, footsteps fading down hallway, silence
【握手】skin contact gentle, fingers interlocking, fabric brushing
【拥抱】cloth rustling soft, deep exhale, heartbeat (if close mic)
```

### 完整示例（10秒雨天离别）
```
【音效】
[0s-3s] rain on window continuous, soft sobbing, shaky breathing, tissue rustling | 
[3s-6s] footsteps approaching slowly, door handle turning, hinge creaking | 
[6s-8s] brief silence, then door closing with soft click | 
[8s-10s] footsteps fading away into rain, only rain sound remaining, single tear drop
```

---

## 四、温馨/治愈场景

### 环境音
```
【清晨室内】birds chirping outside window, soft breeze through curtains, kettle beginning to whistle
【咖啡馆】espresso machine steaming, coffee cup clinking on saucer, soft jazz piano, light chatter murmur
【壁炉旁】fireplace crackling warm, logs shifting, cat purring, clock ticking softly
【花园】bees buzzing, flowers swaying in breeze, fountain trickling, distant children laughing
```

### 动作音效
```
【翻书】pages turning slowly, paper rustling, book spine creaking
【倒茶】hot water pouring into cup, steam hissing softly, spoon stirring clinking
【微笑】soft exhale through nose, fabric shifting as shoulders relax
【猫跳上膝】soft thud, cat kneading fabric, purring starting
```

### 完整示例（10秒咖啡馆温馨）
```
【音效】
[0s-3s] espresso machine steaming, coffee cup placed on saucer with soft clink, gentle jazz piano | 
[3s-6s] spoon stirring slowly in cup, soft laughter between two people, chair shifting | 
[6s-8s] page turning from a book on table, pen writing on paper | 
[8s-10s] window breeze, curtain rustling, rain beginning to tap on glass
```

---

## 五、史诗/宏大场景

### 环境音
```
【山脉】wind howling across peaks, eagle soaring, distant avalanche rumble
【海洋风暴】massive waves crashing, thunder cracking overhead, wind screaming, rain driving hard
【古战场】war horns blowing, thousands of footsteps marching, shields banging, horses charging
【神殿】deep resonance hum, torches crackling, stone echo, chanting choir distant
```

### 动作音效
```
【号角】deep war horn blast, echoing across valley, reverberation fading
【大地震】deep earth rumble, ground cracking, rocks falling, dust cloud whoosh
【巨石落地】massive stone impact, ground shaking, debris scattering, echo rolling
【旗帜飘扬】fabric flapping violently in wind, wooden pole creaking, rope straining
```

### 完整示例（10秒史诗开场）
```
【音效】
[0s-3s] deep horn blast echoing across mountains, wind howling, distant war drums beginning | 
[3s-6s] drums building louder, thousands of footsteps marching in unison, armor clinking | 
[6s-8s] battle cry roaring from army, swords drawn simultaneously, horses neighing | 
[8s-10s] sudden silence except wind, single raven cawing, camera reveals battlefield
```

---

## 六、科幻/奇幻场景

### 环境音
```
【太空站】hologram humming, engine rumble low, communication static, air circulation hiss
【魔法森林】mystical chimes, energy crackling softly, glowing particles humming, ancient tree groaning
【赛博城市】neon buzzing, hovercar passing, drone flying overhead, digital billboards flickering
【地下城】water dripping in cave, torch crackling, chain rattling distant, stone echo
```

### 动作音效
```
【激光射击】energy beam firing, high-pitched zap, impact explosion
【传送门】portal opening with energy swirl, crackling electricity, whoosh of air being pulled
【魔法释放】spell casting chant, energy building hum, burst release, echo decay
【机械启动】servo motors engaging, hydraulics hissing, metal joints rotating, system boot chime
```

### 完整示例（10秒魔法释放）
```
【音效】
[0s-3s] ancient chanting beginning, energy particles gathering, air crackling with static | 
[3s-5s] energy building louder, wind swirling, objects lifting off ground | 
[5s-7s] spell release burst, shockwave whoosh, blinding flash sound | 
[7s-10s] energy dissipating, particles falling like rain, silence except wind
```

---

## 七、悬疑/恐怖场景

### 环境音
```
【废弃建筑】water dripping rhythmically, wind moaning through broken windows, rats scurrying
【深夜巷弄】distant dog barking, flickering neon buzzing, wind carrying paper scraps
【地下室】pipe groaning, boiler humming irregularly, concrete echo, something scratching
```

### 动作音效
```
【门吱呀开】old door hinge groaning slowly, wood scraping floor, draft of air
【脚步回响】slow footsteps echoing in empty corridor, each step louder, then sudden stop
【手机震动】phone buzzing on hard surface, vibrating across table, sudden in silence
【呼吸】heavy breathing close to microphone, shaky inhale, held breath
```

### 完整示例（10秒深夜巷弄）
```
【音效】
[0s-3s] wind through narrow alley, flickering neon buzzing, distant dog barking | 
[3s-6s] slow footsteps echoing on wet pavement, each step deliberate, water splashing | 
[6s-8s] footsteps suddenly stop, only wind and neon buzz, then phone vibrating loudly | 
[8s-10s] phone picked up, screen lighting sound, then sudden silence - all ambient sound cuts
```

---

## 八、日常/生活场景

### 环境音
```
【早晨家中】alarm clock beeping, coffee maker brewing, birds outside, distant traffic
【办公室】keyboard typing, phone ringing distant, air conditioning hum, pages turning
【厨房】oil sizzling in pan, knife chopping on cutting board, water running, timer ticking
【超市】shopping cart rolling, checkout beeping, announcements over speaker, murmuring crowd
```

### 动作音效
```
【开门-钥匙】key turning in lock, door handle pressing, door swinging open
【放书包】backpack dropping on chair with thud, zipper jingling, books shifting inside
【脱鞋】shoes being kicked off, hitting floor, socks on wood floor
【喝水】glass being picked up, water gulping, glass being set down with soft clink
```

---

## 九、转场音效速查

```
【柔和过渡】gentle whoosh, smooth transition, light airy（画面淡入淡出）
【科技转场】sci-fi transition, digital glitch, electronic sweep（产品/科技）
【翻页转场】page turning, paper rustling（生活场景切换）
【时间流逝】clock ticking accelerating, seasons ambiance changing（蒙太奇）
【闪回切入】high-pitched ring, memory distortion, echo（回忆切入）
【梦境切换】underwater muffled, reversed reverb, ethereal chimes（梦境/幻境）
【黑场过渡】all sound fading to silence, single heartbeat, then new scene（沉重转折）
【冲击转场】deep bass drop, screen shake sound, then new ambient（震撼揭示）
```

---

## 十、音效提示词万能公式

```
主体动作 + 接触材质 + 环境空间 + 远近层次 + 时间变化 + 禁止项
```

### 示例
```
【标准写法】footsteps on wet cobblestone, boots with hard soles, echoing in narrow alley, distant rain, no music, no dialogue
【进阶写法】close footsteps on wet stone, faint leather boot creak, water splashing lightly with each step, distant thunder rolling, slight alley reverb, no vocals, no bgm
【分阶段写法】starting with distant footsteps approaching, building to close heavy boots, then suddenly stopping, followed by only dripping water and wind
```

---

## 十一、音效设计避坑清单

1. **拒绝堆砌**：普通镜头保留1-2个核心音效即可，过多会杂乱
2. **音画同步**：脚步声/开门声必须和画面动作对齐，错位强烈违和
3. **音量层级固定**：配音 > BGM > 音效 > 环境音
4. **时空统一**：古风禁现代音效，室内不加室外嘈杂
5. **善用留白**：高潮反转镜头可完全静音，放大情绪张力
6. **材质第一**：木门/金属门/石门必须区分，材质错=瞬间出戏
7. **力度分级**：轻放/中力/猛摔，力度决定情绪强度

---

*整理时间：2026-07-07*
*资料来源：AI短剧音频设计笔记、AudioLDM-S提示词技巧、Seedance 2.0声画帧锁、可灵八层框架、HunyuanVideo-Foley实战*
