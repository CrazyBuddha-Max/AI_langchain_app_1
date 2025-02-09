const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
    devServer: {
    host: '0.0.0.0', // 允许外部访问
    port: 8081,
    allowedHosts: 'all', // 允许所有主机访问
  },
})

