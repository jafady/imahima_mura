module.exports = {
    // docker開発時のホットリロード設定
    devServer: {
      watchOptions: {
        ignored: /node_modules/,
        poll: 500
      }
    },
    pwa: {
      name: "イマヒマ村",
      themeColor: "#3abe27",
      msTileColor: "#3abe27",
      workboxPluginMode: "InjectManifest",
      workboxOptions: {
        swSrc: "src/service-worker.js",
        swDest: "service-worker.js"
      },
      manifestOptions: {
        theme_color: "#3abe27",
        background_color: "#3abe27",
        description: "直近の予定をぱっと埋められるアプリ"
      }
    }
  }