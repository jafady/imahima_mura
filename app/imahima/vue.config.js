module.exports = {
    // docker開発時のホットリロード設定
    devServer: {
      watchOptions: {
        ignored: /node_modules/,
        poll: 500
      }
    }
  }