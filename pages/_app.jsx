import '../styles/globals.scss';

import { useState, useMemo, useEffect } from 'react';
import { useCookies } from 'react-cookie';
import Head from 'next/head';
import App from 'next/app';
import { useRouter } from 'next/router';
import { Backdrop, CircularProgress, CssBaseline, LinearProgress, ThemeProvider } from '@mui/material';

import { lightTheme, darkTheme } from '../utils/js/theme';
import { getCookie as clientCookieGetter, setCookie as clientCookieSetter } from '../utils/js/utils';
import { AuthProvider, ColorModeContext } from '../utils/js/context';
import { Navbar, Footer } from '../components';

function MyApp({ Component, pageProps }) {
    const router = useRouter();
    const [ loading, setLoading ] = useState(false);
    const [ , setCookie ] = useCookies([]);
    const [ mode, setMode ] = useState(pageProps.__darkModeEnabled ? 'dark' : 'light');

    const colorMode = useMemo(() => ({
        toggleColorMode: () => {
            setMode(prevMode => (prevMode === 'light' ? 'dark' : 'light'));
        }
    }), []);

    const _theme = useMemo(() => {
        return mode === 'light' ? lightTheme : darkTheme;
    }, [ mode ]);

    useEffect(() => {
        router.events.on('routeChangeStart', () => setLoading(true));
        router.events.on('routeChangeComplete', () => setLoading(false));
        router.events.on('routeChangeError', () => setLoading(false));
    }, []); // eslint-disable-line

    useEffect(() => {
        if (pageProps.__darkModeEnabled === undefined) {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                setCookie('__darkMode', 't', { expires : new Date(Date.now() + (365*24*60*60*1000)) });
                pageProps.__darkModeEnabled = true;
            } else {
                setCookie('__darkMode', 'f', { expires : new Date(Date.now() + (365*24*60*60*1000)) });
                pageProps.__darkModeEnabled = false;
            }
            router.reload();
        }
    }, []); // eslint-disable-line

    useEffect(() => {
        setCookie('__darkMode', (mode === 'dark' ? 't' : 'f'), { expires : new Date(Date.now() + (365*24*60*60*1000)) });
    }, [ mode ]); // eslint-disable-line

    return (
        <>
            <Head>
                <meta charSet="UTF-8" />
                <meta name="author" content="Akshu Agarwal" />
                <meta name="description" content="A Web Application for a School Management System" />
                <meta name="keywords" content="School Managemenet System, Django, React, Next, JS, Python" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <meta httpEquiv="Content-Type" content="text/html; charset=UTF-8" />
                <meta name="theme-color" media="(prefers-color-scheme: light)" content="white" />
                <meta name="theme-color" media="(prefers-color-scheme: dark)" content="black" />
                <meta name="color-scheme" content="dark light" />
            </Head>
            {
                pageProps.__darkModeEnabled === undefined ? (
                    <Backdrop open sx={{ color : '#fff' }}>
                        <CircularProgress disableShrink variant="indeterminate" color="inherit" thickness={5.0} />
                    </Backdrop>
                ) : (
                    <ColorModeContext.Provider value={colorMode}>
                        <ThemeProvider theme={_theme}>
                            <AuthProvider>
                                <CssBaseline />
                                <div style={{ display : 'flex', flexDirection : 'column', minHeight : '100vh', justifyContent : 'space-between' }}>
                                    {loading ? <LinearProgress color="secondary" /> : null}
                                    <Navbar />
                                    <Component {...pageProps} />
                                    <Footer />
                                </div>
                            </AuthProvider>
                        </ThemeProvider>
                    </ColorModeContext.Provider>
                )
            }
        </>
    );
}

MyApp.getInitialProps = async appContext => {
    const initialProps = await App.getInitialProps(appContext);
    let cookie = null;

    if (appContext.ctx.req) {
        const Cookies = require('cookies');
        const cookies = new Cookies(appContext.ctx.req, appContext.ctx.res);
        cookie = cookies.get('__darkMode');
    } else {
        cookie = clientCookieGetter('__darkMode');
    }

    if (cookie === 't') {
        return { pageProps : { __darkModeEnabled : true, ...initialProps.pageProps } };
    } else if (cookie === 'f') {
        return { pageProps : { __darkModeEnabled : false, ...initialProps.pageProps } };
    } else {
        if (typeof window !== 'undefined') {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                clientCookieSetter('__darkMode', 't', { path : '/', expires : new Date(Date.now() + (365*24*60*60*1000)), samesite : 'strict' });
                return { pageProps : { __darkModeEnabled : true, ...initialProps.pageProps } };
            } else {
                clientCookieSetter('__darkMode', 'f', { path : '/', expires : new Date(Date.now() + (365*24*60*60*1000)), samesite : 'strict' });
                return { pageProps : { __darkModeEnabled : false, ...initialProps.pageProps } };
            }
        } else {
            return { pageProps : { __darkModeEnabled : undefined, ...initialProps.pageProps } };
        }
    }
};

export default MyApp;
