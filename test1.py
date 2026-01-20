import webview

webview.create_window(
    title="test",

    url="easyFileDesk.html",
    transparent=True,
)
webview.start(debug=True)