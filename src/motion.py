plugin = "ahk"
pluginBindings = {}
pluginBindings["goLineStart"] = "{Home}"
pluginBindings["goLineEnd"] = "<end>"
def getPluginBinding(action):
    return pluginBindings[action]
