import { useContext, useState, useRef } from 'react';

import Link from 'next/link';
import Head from 'next/head';
import getConfig from 'next/config';
import { useRouter } from 'next/router';

import { LoadingButton } from '@mui/lab';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { Alert, Box, Collapse, Container, FormControl, IconButton, InputAdornment, InputLabel, OutlinedInput, Typography } from '@mui/material';

import axios from '../utils/js/axios';
import { AuthContext } from '../utils/js/context';

const { publicRuntimeConfig } = getConfig();

export default function Login() {
    const router = useRouter();
    const authContext = useContext(AuthContext);

    const usernameOrEmailRef = useRef();
    const passwordRef = useRef();

    const [ showPassword, setShowPassword ] = useState(false);
    const [ showAlert, setShowAlert ] = useState(false);
    const [ loading, setLoading ] = useState(false);

    if (authContext.loggedIn) {
        router.push('/dashboard');
    }

    const handleSubmit = e => {
        e.preventDefault();

        setShowAlert(false);
        setLoading(true);

        const isEmail = email => {
            return String(email)
                .toLowerCase()
                .match(
                    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                );
        };

        let data = {};
        if (isEmail(usernameOrEmailRef.current.value)) {
            data['email_id'] = usernameOrEmailRef.current.value;
        } else {
            data['username'] = usernameOrEmailRef.current.value;
        }
        data['password'] = passwordRef.current.value;

        axios.post('auth/authenticate/', data).then(response => {
            if (response.status === 200) {
                setLoading(false);
                authContext.setLoggedIn(true);
                authContext.setUserData(response.data.data);
                router.push('/dashboard');
            }
        }).catch(e => {
            if (e.response.status === 404) {
                setLoading(false);
                setShowAlert(true);
            } else {
                setLoading(false);
            }
        });
    };

    return (
        <>
            <Head>
                <title>Login | {publicRuntimeConfig.SCHOOL_NAME}</title>
            </Head>
            <Container sx={{ display : 'flex', flexDirection : 'column', justifyContent : 'center', alignItems : 'center', padding : '8vh' }}>
                <Box sx={{
                    display         : 'flex',
                    flexDirection   : 'column',
                    alignItems      : 'center',
                    justifyContent  : 'center',
                    flexWrap        : 'wrap',
                    width           : '90%',
                    borderRadius    : '7.5px',
                    padding         : '50px',
                    backgroundColor : 'background.paper'
                }}>
                    <Typography variant="h5">Login</Typography>
                    <div style={{ marginTop : '30px' }}>
                        <Collapse in={showAlert}>
                            <Alert severity="error" variant="filled" onClose={() => { setShowAlert(false); }} sx={{ width : '100%', marginBottom : '8px' }}>
                                Invalid Username/Email ID or Password
                            </Alert>
                        </Collapse>
                        <form onSubmit={handleSubmit}>
                            <FormControl variant="outlined" margin="normal" sx={{ width : '100%' }} required>
                                <InputLabel htmlFor="__login_form__inp_useroremail">Username or Email ID</InputLabel>
                                <OutlinedInput
                                    id="__login_form__inp_useroremail"
                                    type="text"
                                    inputRef={usernameOrEmailRef}
                                    label="Username or Email ID"
                                />
                            </FormControl>
                            <FormControl variant="outlined" margin="normal" sx={{ width : '100%' }} required>
                                <InputLabel htmlFor="__login_form__inp_pass">Password</InputLabel>
                                <OutlinedInput
                                    id="__login_form__inp_pass"
                                    type={showPassword ? 'text' : 'password'}
                                    inputRef={passwordRef}
                                    label="Password"
                                    endAdornment={
                                        <InputAdornment position="end">
                                            <IconButton onClick={() => { setShowPassword(!showPassword); }} edge="end">
                                                {showPassword ? <Visibility /> : <VisibilityOff />}
                                            </IconButton>
                                        </InputAdornment>
                                    }
                                />
                            </FormControl>
                            <Typography variant="body1" sx={{ marginTop : '8px', marginBottom : '4px' }}><Link href="/reset-password"><a>Forgot Password?</a></Link></Typography>
                            <LoadingButton type="submit" color="secondary" variant="contained" loading={loading} sx={{ marginTop : '16px' }}>Submit</LoadingButton>
                        </form>
                    </div>
                </Box>
            </Container>
        </>
    );
}
