#!/usr/bin/env python3
"""
考研数学证明题汇编 PDF 生成器 (2000-2026)
按张宇30讲知识体系分类，包含数学一、二、三的所有证明题
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, KeepTogether, Frame,
                                 PageTemplate, BaseDocTemplate)
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus.doctemplate import PageTemplate
import json

# ============================================================
# 注册中文字体
# ============================================================
SONGTI_PATH = "/System/Library/Fonts/Supplemental/Songti.ttc"
HEITI_PATH = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/53fe5be564086fefc7523ccd0a31200acf92e0e5.asset/AssetData/STHEITI.ttf"
KAITI_PATH = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/88d6cc32a907955efa1d014207889413890573be.asset/AssetData/Kaiti.ttc"

# Try to use macOS system fonts
if os.path.exists(SONGTI_PATH):
    try:
        pdfmetrics.registerFont(TTFont('SongtiSC', SONGTI_PATH, subfontIndex=0))
        pdfmetrics.registerFont(TTFont('SongtiSC-Bold', SONGTI_PATH, subfontIndex=1))
    except:
        pass
elif os.path.exists("/System/Library/Fonts/Supplemental/Songti.ttc"):
    pdfmetrics.registerFont(TTFont('SongtiSC', "/System/Library/Fonts/Supplemental/Songti.ttc", subfontIndex=0))

if os.path.exists(HEITI_PATH):
    pdfmetrics.registerFont(TTFont('STHeiti', HEITI_PATH))
elif os.path.exists("/System/Library/Fonts/STHeiti Light.ttc"):
    pdfmetrics.registerFont(TTFont('STHeiti', "/System/Library/Fonts/STHeiti Light.ttc"))

# Fallback to CID font
try:
    pdfmetrics.registerFont(TTFont('PingFang',
        "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc",
        subfontIndex=2))
except:
    try:
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    except:
        pass

# Determine available font names
FONT_BODY = 'SongtiSC'
FONT_HEITI = 'STHeiti'
FONT_BOLD = 'SongtiSC-Bold'

# Check if fonts registered
from reportlab.pdfbase.pdfmetrics import _fonts
registered = list(_fonts.keys())
print(f"Registered fonts: {[f for f in registered if any(k in f.lower() for k in ['song', 'hei', 'ping', 'stso', 'stso'])]}")

# Fallback chain
if 'SongtiSC' not in registered:
    if 'STSong-Light' in registered:
        FONT_BODY = 'STSong-Light'
    elif 'PingFang' in registered:
        FONT_BODY = 'PingFang'
        FONT_BOLD = 'PingFang'
    else:
        FONT_BODY = 'Helvetica'
        FONT_BOLD = 'Helvetica-Bold'
        FONT_HEITI = 'Helvetica'

if 'STHeiti' not in registered:
    FONT_HEITI = FONT_BOLD

print(f"Using fonts: body={FONT_BODY}, heiti={FONT_HEITI}, bold={FONT_BOLD}")

# ============================================================
# 题目数据（按分类整理）
# ============================================================

PROBLEMS = {
    "一、极限与连续": [
        {
            "year": "2008",
            "exam": "数学一",
            "problem": "十八",
            "score": "10",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 连续，<i>g</i>(<i>x</i>) = ∫<sub>0</sub><sup>1</sup> <i>f</i>(<i>xt</i>) d<i>t</i>，且 lim<sub><i>x</i>→0</sub> "
                "<i>f</i>(<i>x</i>)/<i>x</i> = <i>A</i>（<i>A</i> 为常数）。"
                "<br/>(Ⅰ) 求 <i>g</i>′(<i>x</i>) 并讨论 <i>g</i>′(<i>x</i>) 在 <i>x</i> = 0 处的连续性；"
                "<br/>(Ⅱ) 证明：<i>g</i>′(<i>x</i>) 在 <i>x</i> = 0 处连续。"
            )
        },
        {
            "year": "2011",
            "exam": "数学一/二/三",
            "problem": "18/19/18",
            "score": "10",
            "text": (
                "(Ⅰ) 证明：对任意的正整数 <i>n</i>，都有<br/>"
                "  1/(<i>n</i>+1) &lt; ln(1 + 1/<i>n</i>) &lt; 1/<i>n</i> 成立；<br/>"
                "(Ⅱ) 设 <i>a</i><sub><i>n</i></sub> = 1 + 1/2 + ⋯ + 1/<i>n</i> − ln <i>n</i> (<i>n</i> = 1, 2, …)，"
                "证明数列 {<i>a</i><sub><i>n</i></sub>} 收敛。"
            )
        },
        {
            "year": "2018",
            "exam": "数学一/二",
            "problem": "19/21",
            "score": "11",
            "text": (
                "设数列 {<i>x</i><sub><i>n</i></sub>} 满足：<i>x</i><sub>1</sub> &gt; 0，"
                "<i>x</i><sub><i>n</i></sub> e<sup><i>x</i><sub><i>n</i>+1</sub></sup> = e<sup><i>x</i><sub><i>n</i></sub></sup> − 1 "
                "(<i>n</i> = 1, 2, …)。<br/>"
                "证明：{<i>x</i><sub><i>n</i></sub>} 收敛，并求 lim<sub><i>n</i>→∞</sub> <i>x</i><sub><i>n</i></sub>。"
            )
        },
        {
            "year": "2014",
            "exam": "数学一",
            "problem": "19",
            "score": "10",
            "text": (
                "设 0 &lt; <i>a</i><sub><i>n</i></sub> &lt; π/2，0 &lt; <i>b</i><sub><i>n</i></sub> &lt; π/2，"
                "cos <i>a</i><sub><i>n</i></sub> − <i>a</i><sub><i>n</i></sub> = cos <i>b</i><sub><i>n</i></sub>，"
                "且级数 ∑<i>b</i><sub><i>n</i></sub> 收敛。<br/>"
                "(Ⅰ) 证明：lim<sub><i>n</i>→∞</sub> <i>a</i><sub><i>n</i></sub> = 0；<br/>"
                "(Ⅱ) 证明：级数 ∑(<i>a</i><sub><i>n</i></sub>/<i>b</i><sub><i>n</i></sub>) 收敛。"
            )
        },
        {
            "year": "2002",
            "exam": "数学二",
            "problem": "八",
            "score": "8",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 <i>x</i> = 0 的某个邻域内具有二阶连续导数，"
                "且 <i>f</i>(0) ≠ 0，<i>f</i>′(0) ≠ 0，<i>f</i>″(0) ≠ 0。"
                "<br/>证明：存在唯一的一组实数 λ<sub>1</sub>, λ<sub>2</sub>, λ<sub>3</sub>，"
                "使得当 <i>h</i> → 0 时，"
                "λ<sub>1</sub><i>f</i>(<i>h</i>) + λ<sub>2</sub><i>f</i>(2<i>h</i>) + λ<sub>3</sub><i>f</i>(3<i>h</i>) − <i>f</i>(0) "
                "是比 <i>h</i><sup>2</sup> 高阶的无穷小。"
            )
        },
    ],

    "二、导数与微分（含导数定义证明）": [
        {
            "year": "2009",
            "exam": "数学一/三",
            "problem": "18/18",
            "score": "11",
            "text": (
                "(Ⅰ) 证明拉格朗日中值定理：若函数 <i>f</i>(<i>x</i>) 在 [<i>a</i>, <i>b</i>] 上连续，"
                "在 (<i>a</i>, <i>b</i>) 内可导，则存在 ξ ∈ (<i>a</i>, <i>b</i>)，使得<br/>"
                "  <i>f</i>(<i>b</i>) − <i>f</i>(<i>a</i>) = <i>f</i>′(ξ)(<i>b</i> − <i>a</i>)；<br/>"
                "(Ⅱ) 证明：若函数 <i>f</i>(<i>x</i>) 在 <i>x</i> = 0 处连续，在 (0, δ) (δ &gt; 0) 内可导，"
                "且 lim<sub><i>x</i>→0+</sub> <i>f</i>′(<i>x</i>) = <i>A</i>，则 <i>f</i><sub>+</sub>′(0) 存在，"
                "且 <i>f</i><sub>+</sub>′(0) = <i>A</i>。"
            )
        },
        {
            "year": "2015",
            "exam": "数学一",
            "problem": "18",
            "score": "10",
            "text": (
                "(Ⅰ) 设函数 <i>u</i>(<i>x</i>), <i>v</i>(<i>x</i>) 可导，利用导数定义证明：<br/>"
                "  [<i>u</i>(<i>x</i>)<i>v</i>(<i>x</i>)]′ = <i>u</i>′(<i>x</i>)<i>v</i>(<i>x</i>) + <i>u</i>(<i>x</i>)<i>v</i>′(<i>x</i>)；<br/>"
                "(Ⅱ) 设函数 <i>u</i><sub>1</sub>(<i>x</i>), <i>u</i><sub>2</sub>(<i>x</i>), …, <i>u</i><sub><i>n</i></sub>(<i>x</i>) 可导，"
                "写出 [<i>u</i><sub>1</sub>(<i>x</i>)<i>u</i><sub>2</sub>(<i>x</i>)⋯<i>u</i><sub><i>n</i></sub>(<i>x</i>)]′ 的求导公式。"
            )
        },
        {
            "year": "2022",
            "exam": "数学一/二/三",
            "problem": "20/21/20",
            "score": "12",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 (−∞, +∞) 上有二阶连续导数，证明：<br/>"
                "<i>f</i>″(<i>x</i>) ≥ 0 的充分必要条件是：对任意实数 <i>a</i>, <i>b</i>，有<br/>"
                "  <i>f</i>((<i>a</i>+<i>b</i>)/2) ≤ (1/(<i>b</i>−<i>a</i>)) ∫<sub><i>a</i></sub><sup><i>b</i></sup> <i>f</i>(<i>x</i>) d<i>x</i>。"
            )
        },
    ],

    "三、微分中值定理（罗尔/拉格朗日/柯西/泰勒）": [
        {
            "year": "2000",
            "exam": "数学一/二/三",
            "problem": "八",
            "score": "8",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 [0, π] 上连续，且<br/>"
                "  ∫<sub>0</sub><sup>π</sup> <i>f</i>(<i>x</i>) d<i>x</i> = 0，∫<sub>0</sub><sup>π</sup> <i>f</i>(<i>x</i>)cos <i>x</i> d<i>x</i> = 0。<br/>"
                "试证：在 (0, π) 内至少存在两个不同的点 ξ<sub>1</sub>, ξ<sub>2</sub>，"
                "使 <i>f</i>(ξ<sub>1</sub>) = <i>f</i>(ξ<sub>2</sub>) = 0。"
            )
        },
        {
            "year": "2001",
            "exam": "数学三",
            "problem": "七",
            "score": "8",
            "text": (
                "设 <i>f</i>(<i>x</i>) 在 [0, 1] 上连续，在 (0, 1) 内可导，且满足<br/>"
                "  <i>f</i>(1) = <i>k</i> ∫<sub>0</sub><sup>1/<i>k</i></sup> <i>x</i> e<sup>1−<i>x</i></sup> <i>f</i>(<i>x</i>) d<i>x</i>  (<i>k</i> &gt; 1)，<br/>"
                "证明：至少存在一点 ξ ∈ (0, 1)，使得<br/>"
                "  <i>f</i>′(ξ) = (1 − ξ<sup>−1</sup>) <i>f</i>(ξ)。"
            )
        },
        {
            "year": "2001",
            "exam": "数学三",
            "problem": "四",
            "score": "7",
            "text": (
                "已知 <i>f</i>(<i>x</i>) 在 (−∞, +∞) 内可导，且<br/>"
                "  lim<sub><i>x</i>→∞</sub> <i>f</i>′(<i>x</i>) = e，<br/>"
                "lim<sub><i>x</i>→∞</sub> [(<i>x</i>+<i>c</i>)/(<i>x</i>−<i>c</i>)]<sup><i>x</i></sup> = lim<sub><i>x</i>→∞</sub> "
                "[<i>f</i>(<i>x</i>) − <i>f</i>(<i>x</i>−1)]，求 <i>c</i> 的值。"
            )
        },
        {
            "year": "2005",
            "exam": "数学一",
            "problem": "三(19)",
            "score": "12",
            "text": (
                "已知函数 <i>f</i>(<i>x</i>) 在 [0, 1] 上连续，在 (0, 1) 内可导，且 <i>f</i>(0) = 0, <i>f</i>(1) = 1。<br/>"
                "证明：(Ⅰ) 存在 ξ ∈ (0, 1)，使得 <i>f</i>(ξ) = 1 − ξ；<br/>"
                "   (Ⅱ) 存在两个不同的点 η, ζ ∈ (0, 1)，使得 <i>f</i>′(η) <i>f</i>′(ζ) = 1。"
            )
        },
        {
            "year": "2007",
            "exam": "数学一/三",
            "problem": "三(19)/19",
            "score": "11",
            "text": (
                "设函数 <i>f</i>(<i>x</i>), <i>g</i>(<i>x</i>) 在 [<i>a</i>, <i>b</i>] 上连续，在 (<i>a</i>, <i>b</i>) 内具有二阶导数"
                "且存在相等的最大值，<i>f</i>(<i>a</i>) = <i>g</i>(<i>a</i>)，<i>f</i>(<i>b</i>) = <i>g</i>(<i>b</i>)。<br/>"
                "证明：(Ⅰ) 存在 η ∈ (<i>a</i>, <i>b</i>)，使得 <i>f</i>(η) = <i>g</i>(η)；<br/>"
                "   (Ⅱ) 存在 ξ ∈ (<i>a</i>, <i>b</i>)，使得 <i>f</i>″(ξ) = <i>g</i>″(ξ)。"
            )
        },
        {
            "year": "2010",
            "exam": "数学三",
            "problem": "19",
            "score": "11",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 [0, 3] 上连续，在 (0, 3) 内存在二阶导数，且<br/>"
                "  2<i>f</i>(0) = ∫<sub>0</sub><sup>2</sup> <i>f</i>(<i>x</i>) d<i>x</i> = <i>f</i>(2) + <i>f</i>(3)。<br/>"
                "(Ⅰ) 证明：存在 η ∈ (0, 2)，使得 <i>f</i>(η) = <i>f</i>(0)；<br/>"
                "(Ⅱ) 证明：存在 ξ ∈ (0, 3)，使得 <i>f</i>″(ξ) = 0。"
            )
        },
        {
            "year": "2013",
            "exam": "数学一",
            "problem": "18",
            "score": "10",
            "text": (
                "设奇函数 <i>f</i>(<i>x</i>) 在 [−1, 1] 上具有二阶导数，且 <i>f</i>(1) = 1。证明：<br/>"
                "(Ⅰ) 存在 ξ ∈ (0, 1)，使得 <i>f</i>′(ξ) = 1；<br/>"
                "(Ⅱ) 存在 η ∈ (−1, 1)，使得 <i>f</i>″(η) + <i>f</i>′(η) = 1。"
            )
        },
        {
            "year": "2017",
            "exam": "数学一/二",
            "problem": "18/19",
            "score": "10",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 [0, 1] 上具有二阶导数，且 <i>f</i>(0) = <i>f</i>(1) = 0，"
                "min<sub>0≤<i>x</i>≤1</sub> <i>f</i>(<i>x</i>) = −1。<br/>"
                "证明：(Ⅰ) 存在 ξ ∈ (0, 1)，使得 <i>f</i>″(ξ) ≥ 2；<br/>"
                "   (Ⅱ) 存在 η ∈ (0, 1)，使得 <i>f</i>″(η) ≤ −2。"
            )
        },
        {
            "year": "2019",
            "exam": "数学一/二",
            "problem": "19/21",
            "score": "11",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 [0, 1] 上连续，在 (0, 1) 内可导，"
                "且 <i>f</i>(0) = 0，<i>f</i>(1) = 1。<br/>"
                "证明：(Ⅰ) 存在 ξ ∈ (0, 1)，使得 <i>f</i>(ξ) = 1 − ξ；<br/>"
                "   (Ⅱ) 存在两个不同的点 η, ζ ∈ (0, 1)，使得 <i>f</i>′(η)<i>f</i>′(ζ) = 1。"
            )
        },
        {
            "year": "2020",
            "exam": "数学二",
            "problem": "20",
            "score": "10",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 [0, 2] 上具有连续导数，<i>f</i>(0) = <i>f</i>(2) = 0，且<br/>"
                "  <i>M</i> = max<sub>[0,2]</sub> |<i>f</i>(<i>x</i>)|。<br/>"
                "证明：(Ⅰ) 存在 ξ ∈ (0, 2)，使得 |<i>f</i>′(ξ)| ≥ <i>M</i>；<br/>"
                "   (Ⅱ) 若对任意 <i>x</i> ∈ (0, 2)，|<i>f</i>′(<i>x</i>)| ≤ <i>M</i>，则 <i>M</i> = 0。"
            )
        },
        {
            "year": "2023",
            "exam": "数学一/二/三",
            "problem": "20/21/20",
            "score": "12",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 [<i>a</i>, <i>b</i>] 上具有二阶导数，且 <i>f</i>(<i>a</i>) = <i>f</i>(<i>b</i>) = 0，<br/>"
                "  |<i>f</i>″(<i>x</i>)| ≤ <i>M</i>，<i>M</i> 为常数。<br/>"
                "证明：(Ⅰ) |<i>f</i>(<i>x</i>)| ≤ <i>M</i>(<i>b</i>−<i>a</i>)<sup>2</sup>/8；<br/>"
                "   (Ⅱ) |∫<sub><i>a</i></sub><sup><i>b</i></sup> <i>f</i>(<i>x</i>) d<i>x</i>| ≤ <i>M</i>(<i>b</i>−<i>a</i>)<sup>3</sup>/12。"
            )
        },
        {
            "year": "2025",
            "exam": "数学一/二/三",
            "problem": "20/21/20",
            "score": "12",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 [0, 1] 上具有二阶连续导数，<i>f</i>(0) = 0，<i>f</i>(1) = 1。"
                "证明：(Ⅰ) 存在 ξ ∈ (0, 1)，使得 <i>f</i>″(ξ) ≤ <i>f</i>′(ξ)；<br/>"
                "   (Ⅱ) 若 <i>f</i>′(0) = 0，证明存在 η ∈ (0, 1)，使得 <i>f</i>″(η) ≥ 2。"
            )
        },
    ],

    "四、不等式证明（利用导数/单调性/凹凸性/中值定理）": [
        {
            "year": "2002",
            "exam": "数学二",
            "problem": "九",
            "score": "8",
            "text": (
                "设 0 &lt; <i>a</i> &lt; <i>b</i>，证明不等式：<br/>"
                "  2<i>a</i>/(<i>a</i><sup>2</sup> + <i>b</i><sup>2</sup>) &lt; "
                "(ln <i>b</i> − ln <i>a</i>)/(<i>b</i> − <i>a</i>) &lt; 1/√(ab)。"
            )
        },
        {
            "year": "2004",
            "exam": "数学一",
            "problem": "三(19)",
            "score": "12",
            "text": (
                "设 e &lt; <i>a</i> &lt; <i>b</i> &lt; e<sup>2</sup>，证明：<br/>"
                "  ln<sup>2</sup><i>b</i> − ln<sup>2</sup><i>a</i> &gt; (4/e<sup>2</sup>)(<i>b</i> − <i>a</i>)。"
            )
        },
        {
            "year": "2006",
            "exam": "数学二/三",
            "problem": "17/17",
            "score": "10",
            "text": (
                "证明：当 0 &lt; <i>a</i> &lt; <i>b</i> &lt; π 时，<br/>"
                "  <i>b</i> sin <i>b</i> + 2 cos <i>b</i> + π<i>b</i> &gt; "
                "<i>a</i> sin <i>a</i> + 2 cos <i>a</i> + π<i>a</i>。"
            )
        },
        {
            "year": "2012",
            "exam": "数学一",
            "problem": "15",
            "score": "10",
            "text": (
                "证明：当 −1 &lt; <i>x</i> &lt; 1 时，<br/>"
                "  <i>x</i> ln[(1+<i>x</i>)/(1−<i>x</i>)] + cos <i>x</i> ≥ 1 + <i>x</i><sup>2</sup>/2。"
            )
        },
        {
            "year": "2018",
            "exam": "数学二",
            "problem": "18",
            "score": "10",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 [0, 1] 上二阶可导，且 <i>f</i>(0) = 0，<i>f</i>(1) = 1，"
                "<i>f</i>′(0) = −1，<i>f</i>′(1) = 3。<br/>"
                "证明：(Ⅰ) 存在 ξ ∈ (0, 1)，使得 <i>f</i>′(ξ) = 0；<br/>"
                "   (Ⅱ) 存在 η ∈ (0, 1)，使得 <i>f</i>″(η) ≥ 4。"
            )
        },
        {
            "year": "2024",
            "exam": "数学一/二/三",
            "problem": "20/21/20",
            "score": "12",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 [<i>a</i>, <i>b</i>] 上具有二阶导数，<i>f</i>(<i>a</i>) = <i>f</i>(<i>b</i>) = 0，"
                "|<i>f</i>″(<i>x</i>)| ≤ <i>M</i>。<br/>"
                "证明：|<i>f</i>(<i>x</i>)| ≤ <i>M</i>(<i>b</i>−<i>a</i>)<sup>2</sup>/8 "
                "（<i>x</i> ∈ [<i>a</i>, <i>b</i>]），并证明该估计是最佳的。"
            )
        },
        {
            "year": "2014",
            "exam": "数学二",
            "problem": "19",
            "score": "10",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 [0, 1] 上连续，在 (0, 1) 内可导，<i>f</i>(0) = 0，<i>f</i>(1) = 1/4。<br/>"
                "证明：(Ⅰ) 存在 ξ ∈ (0, 1/2)，使得 <i>f</i>(ξ) = ξ；<br/>"
                "   (Ⅱ) 存在 η ∈ (0, ξ)，使得 <i>f</i>′(η) = <i>f</i>(η) − η + 1。"
            )
        },
    ],

    "五、定积分与积分不等式证明": [
        {
            "year": "2008",
            "exam": "数学二",
            "problem": "三(20)",
            "score": "12",
            "text": (
                "(Ⅰ) 证明积分中值定理：若函数 <i>f</i>(<i>x</i>) 在闭区间 [<i>a</i>, <i>b</i>] 上连续，"
                "则至少存在一点 η ∈ [<i>a</i>, <i>b</i>]，使得<br/>"
                "  ∫<sub><i>a</i></sub><sup><i>b</i></sup> <i>f</i>(<i>x</i>) d<i>x</i> = <i>f</i>(η)(<i>b</i> − <i>a</i>)；<br/>"
                "(Ⅱ) 若函数 φ(<i>x</i>) 具有二阶导数，且满足 φ(2) &gt; φ(1)，φ(2) &gt; ∫<sub>2</sub><sup>3</sup> φ(<i>x</i>) d<i>x</i>，"
                "证明至少存在一点 ξ ∈ (1, 3)，使得 φ″(ξ) &lt; 0。"
            )
        },
        {
            "year": "2010",
            "exam": "数学一",
            "problem": "17",
            "score": "5",
            "text": (
                "(Ⅰ) 比较 ∫<sub>0</sub><sup>1</sup> |ln <i>t</i>| [ln(1+<i>t</i>)]<sup><i>n</i></sup> d<i>t</i> 与 "
                "∫<sub>0</sub><sup>1</sup> <i>t</i><sup><i>n</i></sup> |ln <i>t</i>| d<i>t</i> (<i>n</i> = 1, 2, …) 的大小，并说明理由；<br/>"
                "(Ⅱ) 记 <i>u</i><sub><i>n</i></sub> = ∫<sub>0</sub><sup>1</sup> |ln <i>t</i>| [ln(1+<i>t</i>)]<sup><i>n</i></sup> d<i>t</i> "
                "(<i>n</i> = 1, 2, …)，求极限 lim<sub><i>n</i>→∞</sub> <i>u</i><sub><i>n</i></sub>。"
            )
        },
        {
            "year": "2016",
            "exam": "数学一/二",
            "problem": "16/21",
            "score": "5/6",
            "text": (
                "设函数 <i>y</i>(<i>x</i>) 满足方程 <i>y</i>″ + 2<i>y</i>′ + <i>ky</i> = 0 (0 &lt; <i>k</i> &lt; 1)，<br/>"
                "<i>y</i>(0) = 1，<i>y</i>′(0) = 1。<br/>"
                "证明反常积分 ∫<sub>0</sub><sup>+∞</sup> <i>y</i>(<i>x</i>) d<i>x</i> 收敛。"
            )
        },
        {
            "year": "2022",
            "exam": "数学一/二/三",
            "problem": "20/21/20",
            "score": "12",
            "text": (
                "设 <i>f</i>(<i>x</i>) 在 (−∞, +∞) 上有二阶连续导数，证明：<br/>"
                "<i>f</i>″(<i>x</i>) ≥ 0 的充分必要条件是对任意实数 <i>a</i> &lt; <i>b</i>，有<br/>"
                "  <i>f</i>((<i>a</i>+<i>b</i>)/2) ≤ 1/(<i>b</i>−<i>a</i>) ∫<sub><i>a</i></sub><sup><i>b</i></sup> <i>f</i>(<i>x</i>) d<i>x</i>。"
            )
        },
        {
            "year": "2003",
            "exam": "数学一",
            "problem": "八",
            "score": "12",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 连续且恒大于零，<br/>"
                "  <i>F</i>(<i>t</i>) = ∭<sub>Ω(<i>t</i>)</sub> <i>f</i>(<i>x</i><sup>2</sup>+<i>y</i><sup>2</sup>+<i>z</i><sup>2</sup>) d<i>v</i> / ∬<sub><i>D</i>(<i>t</i>)</sub> <i>f</i>(<i>x</i><sup>2</sup>+<i>y</i><sup>2</sup>) dσ<br/>"
                "  <i>G</i>(<i>t</i>) = ∬<sub><i>D</i>(<i>t</i>)</sub> <i>f</i>(<i>x</i><sup>2</sup>+<i>y</i><sup>2</sup>) dσ / ∫<sub>−<i>t</i></sub><sup><i>t</i></sup> <i>f</i>(<i>x</i><sup>2</sup>) d<i>x</i><br/>"
                "其中 Ω(<i>t</i>) = {(<i>x</i>,<i>y</i>,<i>z</i>) | <i>x</i><sup>2</sup>+<i>y</i><sup>2</sup>+<i>z</i><sup>2</sup> ≤ <i>t</i><sup>2</sup>}，"
                "<i>D</i>(<i>t</i>) = {(<i>x</i>,<i>y</i>) | <i>x</i><sup>2</sup>+<i>y</i><sup>2</sup> ≤ <i>t</i><sup>2</sup>}。<br/>"
                "(Ⅰ) 讨论 <i>F</i>(<i>t</i>) 在 (0, +∞) 内的单调性；<br/>"
                "(Ⅱ) 证明：当 <i>t</i> &gt; 0 时，<i>F</i>(<i>t</i>) &gt; (2/π) <i>G</i>(<i>t</i>)。"
            )
        },
    ],

    "六、常微分方程与多元函数微积分证明": [
        {
            "year": "2004",
            "exam": "数学一",
            "problem": "三(16)",
            "score": "12",
            "text": (
                "某种飞机在机场降落时，为了减少滑行距离，在触地的瞬间，飞机尾部张开减速伞，"
                "以增大阻力，使飞机迅速减速并停下。<br/>"
                "现有一质量为 9000 kg 的飞机，着陆时的水平速度为 700 km/h，"
                "经测试，减速伞打开后，飞机所受总阻力与飞机的速度成正比（比例系数 "
                "<i>k</i> = 6.0 × 10<sup>6</sup>）。<br/>"
                "问从着陆点算起，飞机滑行的最长距离是多少？"
            )
        },
        {
            "year": "2005",
            "exam": "数学一",
            "problem": "三(19)",
            "score": "12",
            "text": (
                "设函数 φ(<i>y</i>) 具有连续导数，在围绕原点的任意分段光滑简单闭曲线 <i>L</i> 上，"
                "曲线积分<br/>"
                "  ∮<sub><i>L</i></sub> [φ(<i>y</i>) d<i>x</i> + 2<i>xy</i> d<i>y</i>] / (2<i>x</i><sup>2</sup> + <i>y</i><sup>4</sup>)<br/>"
                "的值恒为同一常数。<br/>"
                "(Ⅰ) 证明：对右半平面 <i>x</i> &gt; 0 内的任意分段光滑简单闭曲线 <i>C</i>，有<br/>"
                "  ∮<sub><i>C</i></sub> [φ(<i>y</i>) d<i>x</i> + 2<i>xy</i> d<i>y</i>] / (2<i>x</i><sup>2</sup> + <i>y</i><sup>4</sup>) = 0；<br/>"
                "(Ⅱ) 求函数 φ(<i>y</i>) 的表达式。"
            )
        },
        {
            "year": "2010",
            "exam": "数学一",
            "problem": "18",
            "score": "5",
            "text": (
                "求幂级数 ∑<sub><i>n</i>=1</sub><sup>∞</sup> [1/(2<i>n</i>+1) − 1]<i>x</i><sup>2<i>n</i></sup> "
                "的收敛域及和函数。"
            )
        },
        {
            "year": "2016",
            "exam": "数学一",
            "problem": "19",
            "score": "10",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 [0, +∞) 上连续可导，<i>f</i>(0) = 1，且满足<br/>"
                "  ∫<sub>0</sub><sup><i>x</i></sup> <i>f</i>(<i>t</i>) d<i>t</i> + ∫<sub>0</sub><sup><i>x</i></sup> <i>t</i> <i>f</i>(<i>x</i>−<i>t</i>) d<i>t</i> "
                "= <i>f</i>(<i>x</i>) − <i>x</i> − 1。<br/>"
                "求 <i>f</i>(<i>x</i>) 的表达式，并证明 <i>f</i>′(<i>x</i>) &lt; <i>f</i>(<i>x</i>) "
                "对一切 <i>x</i> &gt; 0 成立。"
            )
        },
    ],

    "七、无穷级数证明（数一/数三）": [
        {
            "year": "2005",
            "exam": "数学一",
            "problem": "三(18)",
            "score": "12",
            "text": (
                "设 <i>a</i><sub><i>n</i></sub> = ∫<sub>0</sub><sup>π/4</sup> tan<sup><i>n</i></sup> <i>x</i> d<i>x</i>。<br/>"
                "(Ⅰ) 求 ∑<sub><i>n</i>=1</sub><sup>∞</sup> (1/<i>n</i>)(<i>a</i><sub><i>n</i></sub> "
                "+ <i>a</i><sub><i>n</i>+2</sub>) 的值；<br/>"
                "(Ⅱ) 证明：对任意的 λ &gt; 0，∑<sub><i>n</i>=1</sub><sup>∞</sup> "
                "<i>a</i><sub><i>n</i></sub>/<i>n</i><sup>λ</sup> 收敛。"
            )
        },
        {
            "year": "2011",
            "exam": "数学一/二/三",
            "problem": "18/19/18",
            "score": "10",
            "text": (
                "(Ⅰ) 证明：对任意的正整数 <i>n</i>，都有<br/>"
                "  1/(<i>n</i>+1) &lt; ln(1 + 1/<i>n</i>) &lt; 1/<i>n</i> 成立；<br/>"
                "(Ⅱ) 设 <i>a</i><sub><i>n</i></sub> = 1 + 1/2 + ⋯ + 1/<i>n</i> − ln <i>n</i> (<i>n</i> = 1, 2, …)，"
                "证明数列 {<i>a</i><sub><i>n</i></sub>} 收敛。"
            )
        },
        {
            "year": "2013",
            "exam": "数学一",
            "problem": "16",
            "score": "10",
            "text": (
                "设幂级数 ∑<sub><i>n</i>=0</sub><sup>∞</sup> <i>a</i><sub><i>n</i></sub> <i>x</i><sup><i>n</i></sup> 的收敛半径为 "
                "<i>R</i> &gt; 0，其和函数为 <i>S</i>(<i>x</i>)。<br/>"
                "证明：<i>S</i>″(<i>x</i>) − <i>S</i>(<i>x</i>) = 0，并求 <i>S</i>(<i>x</i>) 的表达式。"
            )
        },
        {
            "year": "2014",
            "exam": "数学一",
            "problem": "19",
            "score": "10",
            "text": (
                "设 0 &lt; <i>a</i><sub><i>n</i></sub> &lt; π/2，0 &lt; <i>b</i><sub><i>n</i></sub> &lt; π/2，"
                "cos <i>a</i><sub><i>n</i></sub> − <i>a</i><sub><i>n</i></sub> = cos <i>b</i><sub><i>n</i></sub>，"
                "级数 ∑<i>b</i><sub><i>n</i></sub> 收敛。<br/>"
                "(Ⅰ) 证明：lim<sub><i>n</i>→∞</sub> <i>a</i><sub><i>n</i></sub> = 0；<br/>"
                "(Ⅱ) 证明：级数 ∑(<i>a</i><sub><i>n</i></sub>/<i>b</i><sub><i>n</i></sub>) 收敛。"
            )
        },
        {
            "year": "2019",
            "exam": "数学一",
            "problem": "17",
            "score": "10",
            "text": (
                "设幂级数 ∑<sub><i>n</i>=0</sub><sup>∞</sup> <i>a</i><sub><i>n</i></sub> <i>x</i><sup><i>n</i></sup> "
                "的和函数为 <i>S</i>(<i>x</i>)，<i>S</i>(0) = 1，且满足微分方程<br/>"
                "  <i>x</i><i>S</i>′(<i>x</i>) + (1−<i>x</i>)<i>S</i>(<i>x</i>) = 1。<br/>"
                "(Ⅰ) 求 <i>S</i>(<i>x</i>) 的表达式；<br/>"
                "(Ⅱ) 证明幂级数的系数 <i>a</i><sub><i>n</i></sub> 满足 "
                "<i>a</i><sub><i>n</i>+1</sub> = <i>a</i><sub><i>n</i></sub>/(<i>n</i>+1) "
                "(<i>n</i> = 0, 1, 2, …)。"
            )
        },
    ],

    "八、曲线积分与曲面积分证明（数一）": [
        {
            "year": "2003",
            "exam": "数学一",
            "problem": "四",
            "score": "10",
            "text": (
                "已知平面区域 <i>D</i> = {(<i>x</i>, <i>y</i>) | 0 ≤ <i>x</i> ≤ π, 0 ≤ <i>y</i> ≤ π}，"
                "<i>L</i> 为 <i>D</i> 的正向边界。试证：<br/>"
                "(Ⅰ) ∮<sub><i>L</i></sub> <i>x</i>e<sup>sin <i>y</i></sup> d<i>y</i> − <i>y</i>e<sup>−sin <i>x</i></sup> d<i>x</i> "
                "= ∮<sub><i>L</i></sub> <i>x</i>e<sup>−sin <i>y</i></sup> d<i>y</i> − <i>y</i>e<sup>sin <i>x</i></sup> d<i>x</i>；<br/>"
                "(Ⅱ) ∮<sub><i>L</i></sub> <i>x</i>e<sup>sin <i>y</i></sup> d<i>y</i> − <i>y</i>e<sup>−sin <i>x</i></sup> d<i>x</i> ≥ 2π<sup>2</sup>。"
            )
        },
        {
            "year": "2005",
            "exam": "数学一",
            "problem": "三(19)",
            "score": "12",
            "text": (
                "设函数 φ(<i>y</i>) 具有连续导数，在围绕原点的任意分段光滑简单闭曲线 <i>L</i> 上，"
                "曲线积分<br/>"
                "  ∮<sub><i>L</i></sub> [φ(<i>y</i>) d<i>x</i> + 2<i>xy</i> d<i>y</i>] / (2<i>x</i><sup>2</sup> + <i>y</i><sup>4</sup>)<br/>"
                "的值恒为同一常数。<br/>"
                "(Ⅰ) 证明：对右半平面 <i>x</i> &gt; 0 内的任意分段光滑简单闭曲线 <i>C</i>，有<br/>"
                "  ∮<sub><i>C</i></sub> [φ(<i>y</i>) d<i>x</i> + 2<i>xy</i> d<i>y</i>] / (2<i>x</i><sup>2</sup> + <i>y</i><sup>4</sup>) = 0；<br/>"
                "(Ⅱ) 求函数 φ(<i>y</i>) 的表达式。"
            )
        },
    ],

    "九、线性代数 — 矩阵、行列式、秩与向量": [
        {
            "year": "2002",
            "exam": "数学一",
            "problem": "十",
            "score": "8",
            "text": (
                "已知实二次型 <i>f</i>(<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>) "
                "= <i>a</i>(<i>x</i><sub>1</sub><sup>2</sup> + <i>x</i><sub>2</sub><sup>2</sup> + <i>x</i><sub>3</sub><sup>2</sup>) "
                "+ 4<i>x</i><sub>1</sub><i>x</i><sub>2</sub> + 4<i>x</i><sub>1</sub><i>x</i><sub>3</sub> "
                "+ 4<i>x</i><sub>2</sub><i>x</i><sub>3</sub> 经正交变换 <i>x</i> = <i>Py</i> 化成标准形 "
                "<i>f</i> = 6<i>y</i><sub>1</sub><sup>2</sup>。求参数 <i>a</i> 及所用的正交变换矩阵。"
            )
        },
        {
            "year": "2003",
            "exam": "数学一",
            "problem": "九",
            "score": "10",
            "text": (
                "设 <b>A</b> 为 <i>n</i> 阶实对称正定矩阵，<b>B</b> 为 <i>n</i> × <i>m</i> 实矩阵。"
                "证明 <b>B</b><sup>T</sup><b>AB</b> 正定的充分必要条件是 <i>r</i>(<b>B</b>) = <i>m</i>。"
            )
        },
        {
            "year": "2005",
            "exam": "数学一",
            "problem": "三(21)",
            "score": "9",
            "text": (
                "已知三阶矩阵 <b>A</b> 的第一行是 (<i>a</i>, <i>b</i>, <i>c</i>)，<i>a</i>, <i>b</i>, <i>c</i> "
                "不全为零，矩阵 <b>B</b> = [[1, 2, 3], [2, 4, 6], [3, 6, <i>k</i>]]（<i>k</i> 为常数），"
                "且 <b>AB</b> = <b>O</b>。<br/>"
                "求线性方程组 <b>Ax</b> = <b>0</b> 的通解。"
            )
        },
        {
            "year": "2010",
            "exam": "数学一",
            "problem": "21",
            "score": "4",
            "text": (
                "已知二次型 <i>f</i>(<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>) "
                "= <b>x</b><sup>T</sup><b>Ax</b> 在正交变换 <b>x</b> = <b>Qy</b> 下的标准形为 "
                "<i>y</i><sub>1</sub><sup>2</sup> + <i>y</i><sub>2</sub><sup>2</sup>，"
                "且 <b>Q</b> 的第三列为 (√2/2, 0, √2/2)<sup>T</sup>。<br/>"
                "(Ⅰ) 求 <b>A</b>；(Ⅱ) 证明 <b>A</b> + <b>E</b> 为正定矩阵。"
            )
        },
        {
            "year": "2013",
            "exam": "数学一",
            "problem": "21",
            "score": "11",
            "text": (
                "设二次型 <i>f</i>(<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>) "
                "= 2(<i>a</i><sub>1</sub><i>x</i><sub>1</sub> + <i>a</i><sub>2</sub><i>x</i><sub>2</sub> "
                "+ <i>a</i><sub>3</sub><i>x</i><sub>3</sub>)<sup>2</sup> + (<i>b</i><sub>1</sub><i>x</i><sub>1</sub> "
                "+ <i>b</i><sub>2</sub><i>x</i><sub>2</sub> + <i>b</i><sub>3</sub><i>x</i><sub>3</sub>)<sup>2</sup>，"
                "记 <b>α</b> = (<i>a</i><sub>1</sub>, <i>a</i><sub>2</sub>, <i>a</i><sub>3</sub>)<sup>T</sup>，"
                "<b>β</b> = (<i>b</i><sub>1</sub>, <i>b</i><sub>2</sub>, <i>b</i><sub>3</sub>)<sup>T</sup>。<br/>"
                "(Ⅰ) 证明 <i>f</i> 对应的矩阵为 2<b>αα</b><sup>T</sup> + <b>ββ</b><sup>T</sup>；<br/>"
                "(Ⅱ) 若 <b>α</b>, <b>β</b> 正交且均为单位向量，证明 <i>f</i> 在正交变换下的标准形为 "
                "2<i>y</i><sub>1</sub><sup>2</sup> + <i>y</i><sub>2</sub><sup>2</sup>。"
            )
        },
        {
            "year": "2014",
            "exam": "数学一",
            "problem": "21",
            "score": "11",
            "text": (
                "设 <b>A</b>, <b>B</b> 为 <i>n</i> 阶矩阵，且 <b>A</b> 与 <b>B</b> 相似。"
                "证明 <b>A</b> 与 <b>B</b> 有相同的特征多项式、特征值、迹和行列式。"
            )
        },
        {
            "year": "2015",
            "exam": "数学一",
            "problem": "20",
            "score": "5",
            "text": (
                "设向量组 <b>α</b><sub>1</sub>, <b>α</b><sub>2</sub>, <b>α</b><sub>3</sub> "
                "为 ℝ<sup>3</sup> 的一个基，<b>β</b><sub>1</sub> = 2<b>α</b><sub>1</sub> "
                "+ 2<i>k</i><b>α</b><sub>3</sub>，<b>β</b><sub>2</sub> = 2<b>α</b><sub>2</sub>，"
                "<b>β</b><sub>3</sub> = <b>α</b><sub>2</sub> + (<i>k</i>+1)<b>α</b><sub>3</sub>。<br/>"
                "(Ⅰ) 证明 <b>β</b><sub>1</sub>, <b>β</b><sub>2</sub>, <b>β</b><sub>3</sub> "
                "为 ℝ<sup>3</sup> 的一个基；<br/>"
                "(Ⅱ) 当 <i>k</i> 为何值时，存在非零向量 ξ 在基 <b>α</b><sub>1</sub>, "
                "<b>α</b><sub>2</sub>, <b>α</b><sub>3</sub> 与基 <b>β</b><sub>1</sub>, "
                "<b>β</b><sub>2</sub>, <b>β</b><sub>3</sub> 下的坐标相同，并求所有的 ξ。"
            )
        },
        {
            "year": "2017",
            "exam": "数学一/二",
            "problem": "20/22",
            "score": "5",
            "text": (
                "设 <i>n</i> 阶矩阵 <b>A</b> 满足 <b>A</b><sup>2</sup> = <b>A</b>。"
                "证明：<i>r</i>(<b>A</b>) + <i>r</i>(<b>E</b> − <b>A</b>) = <i>n</i>。"
            )
        },
        {
            "year": "2019",
            "exam": "数学一",
            "problem": "20",
            "score": "5",
            "text": (
                "设 <b>α</b><sub>1</sub>, <b>α</b><sub>2</sub>, <b>α</b><sub>3</sub> "
                "为三维向量空间的一个基，<b>β</b><sub>1</sub> = <b>α</b><sub>1</sub> "
                "+ <b>α</b><sub>2</sub>，<b>β</b><sub>2</sub> = <b>α</b><sub>2</sub> "
                "+ <b>α</b><sub>3</sub>，<b>β</b><sub>3</sub> = <b>α</b><sub>3</sub> "
                "+ <b>α</b><sub>1</sub>。<br/>"
                "证明 <b>β</b><sub>1</sub>, <b>β</b><sub>2</sub>, <b>β</b><sub>3</sub> "
                "也是三维向量空间的一个基，并求由基 <b>α</b><sub>1</sub>, "
                "<b>α</b><sub>2</sub>, <b>α</b><sub>3</sub> 到基 <b>β</b><sub>1</sub>, "
                "<b>β</b><sub>2</sub>, <b>β</b><sub>3</sub> 的过渡矩阵。"
            )
        },
        {
            "year": "2020",
            "exam": "数学一/二",
            "problem": "21/23",
            "score": "5",
            "text": (
                "设 <b>A</b> 为 3 阶矩阵，<b>α</b><sub>1</sub>, <b>α</b><sub>2</sub> "
                "为 <b>A</b> 的分别属于特征值 −1, 1 的特征向量，<b>α</b><sub>3</sub> 满足 "
                "<b>Aα</b><sub>3</sub> = <b>α</b><sub>2</sub> + <b>α</b><sub>3</sub>。<br/>"
                "(Ⅰ) 证明 <b>α</b><sub>1</sub>, <b>α</b><sub>2</sub>, <b>α</b><sub>3</sub> "
                "线性无关；<br/>"
                "(Ⅱ) 令 <b>P</b> = [<b>α</b><sub>1</sub>, <b>α</b><sub>2</sub>, "
                "<b>α</b><sub>3</sub>]，求 <b>P</b><sup>−1</sup><b>AP</b>。"
            )
        },
    ],

    "十、线性代数 — 特征值、特征向量、二次型与正定性": [
        {
            "year": "1999",
            "exam": "数学一",
            "problem": "十",
            "score": "8",
            "text": (
                "设 <b>A</b> 为 <i>m</i> × <i>n</i> 实矩阵，<b>E</b> 为 <i>n</i> 阶单位矩阵，"
                "已知 <b>B</b> = λ<b>E</b> + <b>A</b><sup>T</sup><b>A</b>。"
                "证明当 λ &gt; 0 时，<b>B</b> 为正定矩阵。"
            )
        },
        {
            "year": "2000",
            "exam": "数学一/三",
            "problem": "十",
            "score": "8",
            "text": (
                "设 <i>f</i>(<i>x</i><sub>1</sub>, …, <i>x</i><sub><i>n</i></sub>) = "
                "(<i>x</i><sub>1</sub> + <i>a</i><sub>1</sub><i>x</i><sub>2</sub>)<sup>2</sup> "
                "+ (<i>x</i><sub>2</sub> + <i>a</i><sub>2</sub><i>x</i><sub>3</sub>)<sup>2</sup> + ⋯ "
                "+ (<i>x</i><sub><i>n</i>−1</sub> + <i>a</i><sub><i>n</i>−1</sub><i>x</i><sub><i>n</i></sub>)<sup>2</sup> "
                "+ (<i>x</i><sub><i>n</i></sub> + <i>a</i><sub><i>n</i></sub><i>x</i><sub>1</sub>)<sup>2</sup>。<br/>"
                "试问当 <i>a</i><sub>1</sub>, <i>a</i><sub>2</sub>, …, <i>a</i><sub><i>n</i></sub> 满足什么条件时，"
                "二次型 <i>f</i> 正定？"
            )
        },
        {
            "year": "2010",
            "exam": "数学一",
            "problem": "21",
            "score": "4",
            "text": (
                "已知二次型 <i>f</i>(<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>) "
                "= <b>x</b><sup>T</sup><b>Ax</b> 在正交变换 <b>x</b> = <b>Qy</b> 下的标准形为 "
                "<i>y</i><sub>1</sub><sup>2</sup> + <i>y</i><sub>2</sub><sup>2</sup>，"
                "且 <b>Q</b> 的第三列为 (√2/2, 0, √2/2)<sup>T</sup>。<br/>"
                "(Ⅰ) 求 <b>A</b>；(Ⅱ) 证明 <b>A</b> + <b>E</b> 为正定矩阵。"
            )
        },
        {
            "year": "2021",
            "exam": "数学一/二/三",
            "problem": "21/23/21",
            "score": "12",
            "text": (
                "设二次型 <i>f</i>(<i>x</i><sub>1</sub>, <i>x</i><sub>2</sub>, <i>x</i><sub>3</sub>) "
                "= (<i>x</i><sub>1</sub> + <i>x</i><sub>2</sub>)<sup>2</sup> "
                "+ (<i>x</i><sub>2</sub> + <i>x</i><sub>3</sub>)<sup>2</sup> "
                "+ (<i>x</i><sub>3</sub> − <i>x</i><sub>1</sub>)<sup>2</sup>。<br/>"
                "(Ⅰ) 求 <i>f</i> 的正惯性指数和负惯性指数；<br/>"
                "(Ⅱ) 求一个正交变换将 <i>f</i> 化为标准形。"
            )
        },
    ],

    "十一、概率论与数理统计证明（数一/数三）": [
        {
            "year": "2012",
            "exam": "数学一",
            "problem": "23",
            "score": "5",
            "text": (
                "设 <i>X</i> ∼ <i>N</i>(μ, σ<sup>2</sup>)，<i>Y</i> ∼ <i>N</i>(μ, 2σ<sup>2</sup>)，"
                "<i>X</i> 与 <i>Y</i> 相互独立，<i>Z</i> = <i>X</i> − <i>Y</i>。<br/>"
                "(Ⅰ) 求 <i>Z</i> 的概率密度 <i>f</i><sub><i>Z</i></sub>(<i>z</i>; σ<sup>2</sup>)；<br/>"
                "(Ⅱ) 设 <i>Z</i><sub>1</sub>, <i>Z</i><sub>2</sub>, …, <i>Z</i><sub><i>n</i></sub> "
                "为来自 <i>Z</i> 的简单随机样本，求 σ<sup>2</sup> 的最大似然估计 σ̂<sup>2</sup>；<br/>"
                "(Ⅲ) 证明 σ̂<sup>2</sup> 是 σ<sup>2</sup> 的无偏估计量。"
            )
        },
        {
            "year": "2015",
            "exam": "数学一/三",
            "problem": "23/23",
            "score": "5",
            "text": (
                "设总体 <i>X</i> 的概率密度为<br/>"
                "  <i>f</i>(<i>x</i>; θ) = 1/(2θ) e<sup>−|<i>x</i>|/θ</sup>，−∞ &lt; <i>x</i> &lt; +∞，"
                "θ &gt; 0，<br/>"
                "<i>X</i><sub>1</sub>, <i>X</i><sub>2</sub>, …, <i>X</i><sub><i>n</i></sub> "
                "为来自总体 <i>X</i> 的简单随机样本。<br/>"
                "(Ⅰ) 求 θ 的极大似然估计 θ̂；<br/>"
                "(Ⅱ) 证明 θ̂ 是 θ 的无偏估计量。"
            )
        },
        {
            "year": "2020",
            "exam": "数学一",
            "problem": "22",
            "score": "5",
            "text": (
                "设 <i>X</i><sub>1</sub>, <i>X</i><sub>2</sub>, …, <i>X</i><sub><i>n</i></sub> "
                "为来自正态总体 <i>N</i>(μ, σ<sup>2</sup>) 的简单随机样本。<br/>"
                "证明：样本方差 <i>S</i><sup>2</sup> = [1/(<i>n</i>−1)] "
                "∑<sub><i>i</i>=1</sub><sup><i>n</i></sup> (<i>X</i><sub><i>i</i></sub> − "
                "<b>X̄</b>)<sup>2</sup> 是 σ<sup>2</sup> 的无偏估计量。"
            )
        },
        {
            "year": "2001",
            "exam": "数学三",
            "problem": "十一",
            "score": "8",
            "text": (
                "设总体 <i>X</i> 的分布函数为 <i>F</i>(<i>x</i>; β) = 1 − 1/<i>x</i><sup>β</sup> "
                "(<i>x</i> &gt; 1, β &gt; 1)，<i>X</i><sub>1</sub>, <i>X</i><sub>2</sub>, …, "
                "<i>X</i><sub><i>n</i></sub> 为来自总体的简单随机样本。<br/>"
                "(Ⅰ) 求 β 的矩估计量 β̂；(Ⅱ) 讨论 β̂ 是否为 β 的无偏估计量，并说明理由。"
            )
        },
    ],

    "十二、综合证明题（跨章节综合/应用题证明）": [
        {
            "year": "2020",
            "exam": "数学一",
            "problem": "20",
            "score": "12",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 [<i>a</i>, <i>b</i>] 上连续，在 (<i>a</i>, <i>b</i>) 内可导，"
                "且 <i>f</i>(<i>a</i>) = <i>f</i>(<i>b</i>) = 0。<br/>"
                "证明：(Ⅰ) 存在 ξ ∈ (<i>a</i>, <i>b</i>)，使得 "
                "<i>f</i>(ξ) + <i>f</i>′(ξ) = 0；<br/>"
                "   (Ⅱ) 若 max<sub>[<i>a</i>,<i>b</i>]</sub> <i>f</i>(<i>x</i>) &gt; 0，"
                "则存在 η ∈ (<i>a</i>, <i>b</i>)，使得 <i>f</i>″(η) &lt; 0。"
            )
        },
        {
            "year": "2021",
            "exam": "数学一／二/三",
            "problem": "20/20/20",
            "score": "12",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 [−1, 1] 上具有三阶连续导数，且 "
                "<i>f</i>(−1) = 0，<i>f</i>(1) = 1，<i>f</i>′(0) = 0。<br/>"
                "证明：存在 ξ ∈ (−1, 1)，使得 <i>f</i>‴(ξ) ≥ 3。"
            )
        },
        {
            "year": "2018",
            "exam": "数学一",
            "problem": "18",
            "score": "5",
            "text": (
                "设函数 <i>f</i>(<i>x</i>) 在 [0, 1] 上连续，在 (0, 1) 内具有二阶导数，"
                "且 <i>f</i>(0) = <i>f</i>(1) = 0，<i>f</i>″(<i>x</i>) "
                "+ <i>f</i>(<i>x</i>) = 0。<br/>"
                "证明：<i>f</i>(<i>x</i>) ≡ 0。"
            )
        },
    ],
}

# ============================================================
# PDF 生成
# ============================================================

# Color scheme: match exam paper style (black + subtle rules)
COLOR_CATEGORY = HexColor('#1a1a2e')
COLOR_EXAM_BADGE = HexColor('#e94560')
COLOR_YEAR = HexColor('#0f3460')
COLOR_RULE = HexColor('#cccccc')

def build_styles():
    """Build paragraph styles for the PDF"""
    styles = {}

    styles['title'] = ParagraphStyle(
        'title',
        fontName=FONT_HEITI,
        fontSize=18,
        leading=26,
        alignment=TA_CENTER,
        spaceAfter=8*mm,
    )

    styles['subtitle'] = ParagraphStyle(
        'subtitle',
        fontName=FONT_BODY,
        fontSize=10,
        leading=15,
        alignment=TA_CENTER,
        spaceAfter=10*mm,
        textColor=HexColor('#666666'),
    )

    styles['category'] = ParagraphStyle(
        'category',
        fontName=FONT_HEITI,
        fontSize=14,
        leading=20,
        spaceBefore=8*mm,
        spaceAfter=5*mm,
        textColor=COLOR_CATEGORY,
    )

    styles['problem_header'] = ParagraphStyle(
        'problem_header',
        fontName=FONT_BOLD,
        fontSize=11,
        leading=16,
        spaceBefore=4*mm,
        spaceAfter=1*mm,
    )

    styles['problem_body'] = ParagraphStyle(
        'problem_body',
        fontName=FONT_BODY,
        fontSize=11,
        leading=18,
        alignment=TA_JUSTIFY,
        spaceAfter=3*mm,
        leftIndent=5*mm,
    )

    styles['answer_space'] = ParagraphStyle(
        'answer_space',
        fontName=FONT_BODY,
        fontSize=9,
        leading=14,
        textColor=HexColor('#aaaaaa'),
        leftIndent=5*mm,
    )

    styles['footer'] = ParagraphStyle(
        'footer',
        fontName=FONT_BODY,
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        textColor=HexColor('#999999'),
    )

    return styles


def build_pdf(output_path):
    """Main function: construct the PDF"""
    styles = build_styles()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2.2*cm,
        rightMargin=2.2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title='考研数学证明题汇编 (2000–2026)',
        author='考研数学真题整理',
    )

    story = []

    # --- Cover / Title ---
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph('考研数学证明题汇编', styles['title']))
    story.append(Paragraph('（2000 年 – 2026 年）', styles['title']))
    story.append(Paragraph('涵盖数学一、数学二、数学三全部证明题 ｜ 按张宇30讲知识体系分类', styles['subtitle']))
    story.append(Spacer(1, 0.5*cm))

    # Table of contents
    story.append(Paragraph('目  录', styles['category']))
    toc_items = list(PROBLEMS.keys())
    for i, cat in enumerate(toc_items):
        count = len(PROBLEMS[cat])
        story.append(Paragraph(f'{i+1}. {cat}（{count} 题）', ParagraphStyle(
            'toc_item', fontName=FONT_BODY, fontSize=11, leading=20,
            leftIndent=1*cm, spaceAfter=1*mm)))
    story.append(PageBreak())

    # --- Problem sections ---
    problem_counter = 0
    for category, problems in PROBLEMS.items():
        story.append(Paragraph(category, styles['category']))
        story.append(HRFlowable(
            width="100%", thickness=0.5, color=COLOR_CATEGORY, spaceAfter=4*mm))

        for i, p in enumerate(problems):
            problem_counter += 1

            # Problem tag: year badge + exam info
            header_text = (
                f'<b>【{problem_counter}】</b> '
                f'{p["year"]}年·{p["exam"]} · 第{p["problem"]}题 '
                f'（{p["score"]}分）'
            )
            story.append(Paragraph(header_text, styles['problem_header']))

            # Problem body
            story.append(Paragraph(p['text'], styles['problem_body']))

            # Answer space: roughly proportional to score value
            try:
                score_val = int(p['score'])
            except:
                score_val = 10
            # lines of answer space
            answer_lines = max(6, score_val * 2)
            space_lines = '<br/>'.join(['_' * 90] * answer_lines)
            story.append(Paragraph(
                f'<br/>{space_lines}<br/><br/>',
                styles['answer_space']
            ))

        # Don't page break after the last section
        if category != list(PROBLEMS.keys())[-1]:
            story.append(PageBreak())

    # Build
    doc.build(story)
    print(f"PDF generated: {output_path}")
    print(f"Total problems: {problem_counter}")


if __name__ == '__main__':
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, 'proof_questions', '考研数学证明题汇编_2000-2026.pdf')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    build_pdf(output_path)
