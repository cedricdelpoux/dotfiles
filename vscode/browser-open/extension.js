const vscode = require("vscode")

exports.activate = (context) => {
  context.subscriptions.push(
    vscode.window.registerUriHandler({
      handleUri(uri) {
        const url = new URLSearchParams(uri.query).get("url")
        const {origin, pathname} = new URL(url)
        const reuseUrlFilter = origin === "null" ? url : `${origin}${pathname}`
        vscode.commands.executeCommand("workbench.action.browser.open", {url, reuseUrlFilter})
      },
    }),
  )
}
