import json, glob, html as html_lib, base64, io, os, sys
from PIL import Image

def esc(s):
    return html_lib.escape(s or "", quote=False)

def nl2br(s):
    return esc(s).replace("\n", "<br>")

def build(year, country="india", country_label="印度"):
    task_dir = f"data/tasks/{year}"
    img_dir = f"assets/images/{country}/{year}"
    tasks = []
    for f in sorted(glob.glob(f"{task_dir}/*.json")):
        with open(f, encoding="utf-8") as fh:
            tasks.append(json.load(fh))

    b64 = {}
    for f in sorted(glob.glob(f"{img_dir}/*.png")):
        uid = os.path.splitext(os.path.basename(f))[0]
        im = Image.open(f).convert("RGB")
        if im.width > 700:
            ratio = 700 / im.width
            im = im.resize((700, int(im.height*ratio)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=78, optimize=True)
        b64[uid] = base64.b64encode(buf.getvalue()).decode("ascii")

    cards = []
    index_items = []
    for i, t in enumerate(tasks, 1):
        uid = t["task_uid"]
        title_zh = t["title_zh"]; title_en = t["title_en"]
        flag = t.get("source_country_flag") or "🏳️"
        country_name = t.get("source_country") or "未標示出處國"
        lic = t.get("license", "")
        itype = t.get("interaction_type","")
        asset = t.get("asset", {})
        has_img = uid in b64
        cn = t["content_zh"]; ce = t["content_en"]

        index_items.append(f'<a class="idx-item" href="#{uid}"><span class="idx-num">{i:02d}</span><span class="idx-flag">{flag}</span><span class="idx-title">{esc(title_zh)}</span>{"" if has_img else "<span class=\"idx-noimg\">無圖</span>"}</a>')

        if has_img:
            img_html = f'''<figure class="task-figure">
              <img src="data:image/jpeg;base64,{b64[uid]}" alt="{esc(title_en)} 插圖" loading="lazy">
              <figcaption>圖片素材 · {esc(asset.get("path",""))}</figcaption>
            </figure>'''
        else:
            img_html = f'<div class="no-image">此題為純文字題，無需圖片<br><span>{esc(asset.get("status",""))}</span></div>'

        opts_html = ""
        for opt in cn.get("options", []):
            is_ans = opt["key"] == cn.get("answer")
            opts_html += f'''<li class="opt{" opt-answer" if is_ans else ""}">
              <span class="opt-key">{opt["key"]}</span>
              <span class="opt-text">{esc(opt["text"])}</span>
              {"<span class=\"opt-badge\">正解</span>" if is_ans else ""}
            </li>'''

        en_opts = "、".join(f'{o["key"]}) {esc(o["text"])}' for o in ce.get("options", []))

        card = f'''
    <article class="task-card" id="{uid}">
      <header class="task-head">
        <div class="task-head-top">
          <span class="task-uid">{uid}</span>
          <span class="task-badges">
            <span class="badge badge-type">{esc(itype)}</span>
            <span class="badge badge-license">{esc(lic)}</span>
          </span>
        </div>
        <h2 class="task-title">
          <span class="flag">{flag}</span>{esc(title_zh)}
          <span class="task-title-en">{esc(title_en)}</span>
        </h2>
        <div class="task-origin">原始出處：{esc(country_name)} · {esc(t.get("license_source_note",""))}</div>
      </header>

      <div class="task-body">
        {img_html}

        <div class="task-text">
          <p class="prompt">{nl2br(cn["prompt"])}</p>
          <p class="question"><strong>Q.</strong> {esc(cn["question"])}</p>
          <ul class="options">{opts_html}</ul>
          <div class="explain">
            <span class="explain-label">解析</span>
            <p>{nl2br(cn["explanation"])}</p>
          </div>
          <div class="ct-tags">
            <span class="ct-tag">CT技能：{esc(cn.get("ct_skills",""))}</span>
            <span class="ct-tag">領域：{esc(cn.get("cs_domain",""))}</span>
          </div>
        </div>
      </div>

      <details class="en-ref">
        <summary>英文原文對照（校對用）</summary>
        <p class="prompt-en">{nl2br(ce["prompt"])}</p>
        <p class="question-en"><strong>Q.</strong> {esc(ce["question"])}</p>
        <p class="options-en">{en_opts}</p>
        <p class="answer-en"><strong>Answer:</strong> {esc(ce.get("answer",""))}</p>
      </details>
    </article>'''
        cards.append(card)

    n_img = sum(1 for t in tasks if t["task_uid"] in b64)
    n_noimg = len(tasks) - n_img

    with open("scripts/_shell_head_template.html", encoding="utf-8") as f:
        shell = f.read()

    shell = shell.replace("__YEAR__", str(year)).replace("__COUNTRY__", country_label)
    shell = shell.replace("__TOTAL__", str(len(tasks))).replace("__NIMG__", str(n_img)).replace("__NNOIMG__", str(n_noimg))
    out = shell.replace("INDEX_PLACEHOLDER", "\n".join(index_items)).replace("CARDS_PLACEHOLDER", "\n".join(cards))

    outpath = f"review/{year}_review.html"
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"{year}: {len(tasks)} tasks, {n_img} with image, {n_noimg} text-only -> {outpath} ({len(out.encode('utf-8'))/1024/1024:.2f} MB)")

if __name__ == "__main__":
    build(sys.argv[1])
