import { useEffect, useState, useContext } from 'react';

import Head from 'next/head';
import getConfig from 'next/config';
import { useRouter } from 'next/router';

import { Container } from '@mui/material';

import { Sidebar } from '../../../components';
import { AuthContext } from '../../../utils/js/context';

import CreateUser from './createUser';

const { publicRuntimeConfig } = getConfig();

export default function Admin() {
    const router = useRouter();
    const authContext = useContext(AuthContext);

    const [ currentBody, setCurrentBody ] = useState(<CreateUser />);

    const [ rendering, setRendering ] = useState(true);

    useEffect(() => {
        if (authContext.documentLoaded) {
            console.log(8);
            if (rendering) {
                if (!authContext.loggedIn) {
                    router.replace('/login');
                } else if (authContext.userData.user_type !== 'a') {
                    router.replace('/dashboard');
                } else {
                    setRendering(false);
                }
            }
        }
    }, [ authContext.documentLoaded ]); // eslint-disable-line

    return (
        <>
            <Head>
                <title>Admin Dashboard | {publicRuntimeConfig.SCHOOL_NAME}</title>
            </Head>
            <Container style={{ display : 'flex', flexDirection : 'row', flexGrow : 1, width : '100vw', maxWidth : '100%' }} disableGutters>
                {
                    !rendering ? (
                        <Sidebar items={[
                        // Format of an item element:
                        // { icon : null, avatar : null, text : '', onClick : () => {}, defaultSelected : true }
                            { text : 'Create User', onClick : () => { setCurrentBody(<CreateUser />); }, defaultSelected : true },
                        ]} />
                    ) : null
                }
                {currentBody}
            </Container>
        </>
    );
}
