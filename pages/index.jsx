import Head from 'next/head';
import getConfig from 'next/config';

import { Container } from '@mui/material';

const { publicRuntimeConfig } = getConfig();

export default function Home() {
    return (
        <>
            <Head>
                <title>Home | {publicRuntimeConfig.SCHOOL_NAME}</title>
            </Head>
            <Container sx={{ margin : 0, display : 'flex', flexDirection : 'column' }}>
                <p>Index</p>
            </Container>
        </>
    );
}
