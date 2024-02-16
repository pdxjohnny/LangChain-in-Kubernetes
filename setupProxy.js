const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use('/apiopenai', createProxyMiddleware({
    target: 'http://localhost:8000', // Change this to match your FastAPI server's URL
    changeOrigin: true,
  }));
};