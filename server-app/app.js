const express = require('express');
const basicAuth = require('express-basic-auth');
const apiMetrics = require('prometheus-api-metrics');
const Prometheus = require('prom-client');
const { v4: uuid } = require('uuid');
const app = express();
const port = 80;

// Some fake users
const users = {
  admin: 'admin',
  employee: 'employee',
  user: 'user',
};

// Basic auth middleware
const authMiddleware = basicAuth({
  authorizer: (username, password) => {
    return users[username] && users[username] === password;
  },
  challenge: true,
  unauthorizedResponse: 'Unauthorized',
});

// Custom metric to record forbidden accesses
const forbiddenAccessMetric = new Prometheus.Counter({
  name: 'forbidden_access_total',
  help: 'Total number of forbidden access attempts',
  labelNames: ['path', 'user', '_id'],
});

// middleware that will check if the user is authorized to access that endpoint
const checkAccess = (allowedUsers) => (req, res, next) => {
  const username = req.auth.user;
  if (allowedUsers.includes(username)) {
    return next();
  }
  forbiddenAccessMetric.inc({ path: req.path, user: username, _id: uuid() });
  return res.status(403).send('Forbidden');
};

// expose prometheus metrics
app.use(apiMetrics());

// reset the custom metric  every 60s
setInterval(
  () => {
    forbiddenAccessMetric.reset();
  },
  parseInt(process.env.RESET_ACESS_METRIC || '60000')
);

// Routes
app.get('/admin', authMiddleware, checkAccess(['admin']), (_, res) => {
  res.json({ message: 'Hello Admin' });
});

app.get('/employee', authMiddleware, checkAccess(['admin', 'employee']), (_, res) => {
  res.json({ message: 'Hello Employee or Admin' });
});

app.get('/user', authMiddleware, checkAccess(['admin', 'employee', 'user']), (_, res) => {
  res.json({ message: 'Hello User or Employee or Admin' });
});

// Server start
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
