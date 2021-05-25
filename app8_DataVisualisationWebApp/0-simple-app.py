import justpy as jp


def app():
    # Create the Quasar webpage
    wp = jp.QuasarPage()
    # Create QDiv components linked to the webpage
    h1 = jp.QDiv(a=wp, text="Analysis of Course Reviews", classes="text-h3 text-center")
    # Typography classes list in https://quasar.dev/style/typography
    p1 = jp.QDiv(a=wp, text="These graphs represent course review analysis")

    return wp


jp.justpy(app)
