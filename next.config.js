require('dotenv').config();
let constants = require('./constants.json');

const withBundleAnalyzer = require('@next/bundle-analyzer')({
    enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
    reactStrictMode     : true,
    publicRuntimeConfig : {
        BACKEND_BASE_URL : `${process.env.DJANGO_PROTOCOL}://${process.env.DJANGO_HOSTNAME}:${process.env.DJANGO_PORT}/`,
        FRONTEND_URL     : process.env.SITE_URL,
        SCHOOL_NAME      : constants['SCHOOL_NAME'],
        FOOTER_TEXT      : constants['FOOTER_TEXT'],
    },
    images: {
        domains: [ 'flagcdn.com' ],
    },
});
