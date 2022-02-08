import { useEffect, useState, useContext } from 'react';

import Head from 'next/head';
import getConfig from 'next/config';
import { useRouter } from 'next/router';

import { Backdrop, CircularProgress, Container, NoSsr } from '@mui/material';

import { Sidebar } from '../../../components';
import { AuthContext } from '../../../utils/js/context';

import SearchUser from './searchUser';

const { publicRuntimeConfig } = getConfig();

export default function Management() {
    const router = useRouter();
    const authContext = useContext(AuthContext);

    const [ rendering, setRendering ] = useState(true);

    const [ currentComponent, setCurrentComponent ] = useState(null);

    const shallowRedirectToPage = to => {
        return router.push({ pathname : router.pathname, query : { page : to } }, undefined, { shallow : true });
    };

    const pages = {
        // Format of an item element:
        // { id: '', icon : null, avatar : null, text : '', onClick : () => {}, pageComponent : null }
        items: [
            { id : 'search-user', text : 'Search User', pageComponent : <SearchUser /> },
        ],
        defaultItem: { id : 'dashboard', text : 'Dashboard' }
    };

    useEffect(() => {
        if (authContext.documentLoaded) {
            if (rendering) {
                if (!authContext.loggedIn) {
                    router.replace('/login');
                } else if (authContext.userData.user_type !== 'm') {
                    router.replace('/dashboard');
                } else {
                    setRendering(false);
                }
            }
        }
    }, [ authContext.documentLoaded ]); // eslint-disable-line

    useEffect(() => {
        if (!router.query.page) { // No page query exists
            shallowRedirectToPage(pages.defaultItem.id);
            setCurrentComponent(pages.defaultItem.pageComponent);
        } else {
            if (router.query.page === pages.defaultItem.id) { // Page query exists and is equal to default page
                setCurrentComponent(pages.defaultItem.pageComponent);
                return;
            } else {
                for (let i = 0; i <= pages.items.length; i++) { // Page query exists and is equal to one of the pages other than default page
                    if (i < pages.items.length) {
                        if (router.query.page === pages.items[i].id) {
                            setCurrentComponent(pages.items[i].pageComponent);
                            return;
                        }
                    } else { // Page query exists but is invalid
                        shallowRedirectToPage(pages.defaultItem.id);
                        setCurrentComponent(pages.defaultItem.pageComponent);
                        return;
                    }
                }
            }
        }
    }, [ router.query.page ]); // eslint-disable-line

    return (
        <>
            <Head>
                <title>Management Dashboard | {publicRuntimeConfig.SCHOOL_NAME}</title>
            </Head>
            <Container style={{ display : 'flex', flexDirection : 'row', flexGrow : 1, width : '100vw', maxWidth : '100%' }} disableGutters>
                <NoSsr fallback={(
                    <Backdrop open sx={{ color : '#fff' }}>
                        <CircularProgress disableShrink variant="indeterminate" color="inherit" thickness={5.0} />
                    </Backdrop>
                )}>
                    { !rendering ? <Sidebar pages={pages} /> : null }
                    { !rendering ? currentComponent : null }
                </NoSsr>
            </Container>
        </>
    );
}
