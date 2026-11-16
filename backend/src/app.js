
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const swaggerUi = require('swagger-ui-express');
const yaml = require('js-yaml');
const fs = require('fs');
const path = require('path');

const authRoutes = require('./routes/auth');
const onboardingRoutes = require('./routes/onboarding');
const mentorRoutes = require('./routes/mentor');
const metricsRoutes = require('./routes/metrics');

const { notFound, errorHandler } = require('./middleware/errors');

const app = express();

app.use(helmet());

app.use(
    cors({
        origin: process.env.CORS_ORIGIN
            ? process.env.CORS_ORIGIN.split(',')
            : true
    })
);

app.use(express.json({ limit: '1mb' }));

app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        service: 'RampUp API'
    });
});

app.use('/api/v1/auth', authRoutes);
app.use('/api/v1/onboarding', onboardingRoutes);
app.use('/api/v1/mentor', mentorRoutes);
app.use('/api/v1/metrics', metricsRoutes);

// Carrega a especificação OpenAPI
const openApiPath = path.join(__dirname, 'openapi.yaml');
const spec = yaml.load(fs.readFileSync(openApiPath, 'utf8'));

app.use('/docs', swaggerUi.serve, swaggerUi.setup(spec));

app.use(notFound);
app.use(errorHandler);

module.exports = app;
