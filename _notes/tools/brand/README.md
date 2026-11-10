# The official logos, cut from the St. Bernard Brand Guide (9.10.2024)

The guide is a 12-page PDF from the abbey (St_Bernard_Brand_Guide_2024.pdf; not kept in the repo; ask Br. Augustine for it).
Its logos are vectors, so these scripts cut them out as small SVG files instead of tracing pictures:

    pdftocairo -svg -f 2 -l 2 guide.pdf p2.svg      # also pages 3 (reversed, on navy) and 6 (with "Abbey" / "Preparatory School")
    python3 mk.py      # writes out/*.svg: primary, horizontal and cross, light and dark, cropped by page regions in points
    python3 mk2.py     # the "Abbey" and "Preparatory School" versions, plus white-on-navy copies (navy text -> white, shield outlined)

`crop.py` holds the helpers (drop the page's background panels, keep only what falls inside the region, keep only the glyphs used).
Results in use: assets/img/brand/ here, and images/brand/ in munkachy/sbp. Colours and fonts from the same guide:
navy #004069, gold #D8B95C, white #FEFEFE; accents #01253D, #4D81A7, #537889, #A7C4D2; Libre Baskerville (display), Noto Sans (text).
