from violetear import StyleSheet
from violetear.color import Colors
from violetear.units import Unit, px, rem

sheet = StyleSheet(normalize=True)

sheet.select("body").width(max=768).margin("auto")

sheet.select(".btn").rule('cursor', 'pointer').rounded()

font_sizes = Unit.scale(px, 14, 32, 4)
padding_sizes = Unit.scale(px, 5, 8, 4)

for cls, font, pd in zip(["xs", "sm", "md", "lg"], font_sizes, padding_sizes):
    btn_size = (
        sheet.select(f".btn.{cls}")
        .font(size=font)
        .padding(left=pd * 2, top=pd, bottom=pd, right=pd * 2)
    )

colors = [
    Colors.White.lit(0.9),
    Colors.Blue.lit(0.3),
    Colors.Green.lit(0.3),
    Colors.Orange.lit(0.6),
    Colors.Red.lit(0.3),
    Colors.Cyan.lit(0.8),
]

for cls, color in zip(["", ".primary", ".success", ".warning", ".error", ".info"], colors):
    if color.lightness < 0.5:
        text_color = color.lit(0.9)
        accent_color = Colors.White
    else:
        text_color = color.lit(0.1)
        accent_color = Colors.Black

    btn_style = sheet.select(f".btn{cls}").background(color).color(text_color)
    btn_style.on("hover").background(color.brighter(0.1)).color(accent_color)
    btn_style.on("active").background(color.darker(0.1)).color(accent_color)

if __name__ == "__main__":
    sheet.render("semantic-inputs.css")
