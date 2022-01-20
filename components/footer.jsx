import { useEffect, useState } from 'react';
import Link from 'next/link';
import getConfig from 'next/config';
import { AppBar, Container, Stack, Typography } from '@mui/material';

const { publicRuntimeConfig } = getConfig();

export default function Footer() {
    const [ host, setHost ] = useState('');

    useEffect(() => {
        setHost(window.location.host);
    }, []);

    return (
        <AppBar component="footer" position="relative" sx={{ backgroundImage : 'initial', marginTop : 'auto' }}>
            <Container sx={{ display : 'flex', flexDirection : 'column', alignItems : 'center', padding : '20px' }}>
                <Container sx={{ display : 'flex', flexDirection : 'row', paddingBottom : '10px' }}>
                    <Container sx={{ display : 'flex', flexDirection : 'column' }}>
                        <Stack spacing={1.5} direction="column" sx={{ alignItems : 'center' }}>
                            <Typography variant="h6">About Us</Typography>
                            <Typography variant="body1" sx={{ textAlign : 'center' }}>
                                {publicRuntimeConfig.FOOTER_TEXT}
                            </Typography>
                        </Stack>
                    </Container>
                    <Container sx={{ display : 'flex', flexDirection : 'column', alignItems : 'center', justifyContent : 'center' }}>
                        <Stack spacing={1.5} direction="column">
                            <Typography variant="h6">Our Links</Typography>
                            <Stack spacing={0.5} direction="column">
                                <Link href="/"><a>Home</a></Link>
                                <Link href="/about"><a>About</a></Link>
                                <Link href="/contact"><a>Contact Us</a></Link>
                                <Link href="/terms-of-use"><a>Terms of Use</a></Link>
                                <Link href="/privacy-policy"><a>Privacy Policy</a></Link>
                            </Stack>
                        </Stack>
                    </Container>
                </Container>
                <Typography variant="body1">
                    &copy; {new Date().getFullYear()}{' '}
                    <Link href="/"><a>{host}</a></Link>
                </Typography>
            </Container>
        </AppBar>
    );
}
