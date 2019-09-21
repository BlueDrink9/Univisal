plugin = "ahk"
pluginBindings = {}
pluginBindings["goLineStart"] = "{Home}"
pluginBindings["goLineEnd"] = "{End}"
def getPluginBinding(action):
    return pluginBindings[action]
