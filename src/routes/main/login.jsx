import axios from 'axios';
import React, { useEffect, useState, useRef } from 'react';
import Cookies from "universal-cookie";
import { Form, Button, FloatingLabel, Alert } from 'react-bootstrap';

import Footer from '../../components/footer.jsx';
import Navbar from '../../components/navbar.jsx';
import { BASE_AUTH } from '../../constants.js';

axios.defaults.withCredentials = true;

const cookie = new Cookies();

const redirectToDashboard = type => {
    if (type === 's') {
        return window.location.href = '/student/dashboard';
    } else if (type === 't') {
        return window.location.href = '/teacher/dashboard';
    } else if (type === 'p') {
        return window.location.href = '/parent/dashboard';
    } else if (type === 'm') {
        return window.location.href = '/manager/dashboard';
    } else if (type === 'a') {
        return window.location.href = '/admin/dashboard';
    };
};

const LoginForm = () => {
    const usernameOrEmailRef = useRef();
    const passwordRef = useRef();

    const [validated, setValidated] = useState(false);
    const [showAlert, setShowAlert] = useState(false);

    const validateEmail = email => {
        return String(email)
            .toLowerCase()
            .match(
                /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            );
    };

    const handleSubmit = e => {
        e.preventDefault();

        setShowAlert(false);

        const usernameOrEmail = usernameOrEmailRef.current.value;
        const data = {};

        if (validateEmail(usernameOrEmail)) {
            data['email_id'] = usernameOrEmail
        } else {
            data['username'] = usernameOrEmail
        }
        data['password'] = passwordRef.current.value;

        setValidated(true);

        axios.post(
            BASE_AUTH + 'authorize/',
            data
        ).then(response => {
            if (response.status === 200) {
                cookie.set('__li', 't', { path: '/', expires: new Date(Date.now() + (86400 * 1000)), secure: true, sameSite: 'strict' });
                cookie.set('__ud', response.data, { path: '/', expires: new Date(Date.now() + (86400 * 1000)), secure: true, sameSite: 'strict' });
                redirectToDashboard(response.data.user_type);
            };
        }).catch(e => {
            if (e.response.status === 404) {
                cookie.set('__li', 'f', { path: '/', expires: new Date(Date.now() + (86400 * 1000)), secure: true, sameSite: 'strict' });
                setShowAlert(true);
            };
        });
    };

    return (
        <>
            {showAlert ? (<Alert dismissible variant="danger" onClose={() => setShowAlert(false)}>Invalid Credentials</Alert>) : null}
            <Form noValidate validated={validated} onSubmit={handleSubmit}>
                <Form.Group>
                    <FloatingLabel label="Username or Email *">
                        <Form.Control required ref={usernameOrEmailRef} type="text" placeholder="Username or Email" />
                    </FloatingLabel>
                </Form.Group>
                <Form.Group>
                    <FloatingLabel label="Password *">
                        <Form.Control required ref={passwordRef} type="password" placeholder="Password" />
                    </FloatingLabel>
                </Form.Group>
                <Form.Group>
                    <Button variant="light" type="submit">Submit</Button>
                </Form.Group>
            </Form>
        </>
    );
};

function Login() {
    useEffect(() => {
        const isAuth = cookie.get('__li');
        const userData = cookie.get('__ud');

        if (isAuth === 't' && userData) {
            redirectToDashboard(userData.user_type);
        } else {
            axios.get(
                BASE_AUTH + 'authorize/'
            ).then(response => {
                if (response.status === 200) {
                    cookie.set('__li', 't', { path: '/', expires: new Date(Date.now() + (86400 * 1000)), secure: true, sameSite: 'strict' });
                    cookie.set('__ud', response.data.data, { path: '/', expires: new Date(Date.now() + (86400 * 1000)), secure: true, sameSite: 'strict' });
                    redirectToDashboard(response.data.data.user_type);
                };
            }).catch(e => {
                if (e.response.status === 401) {
                    cookie.set('__li', 'f', { path: '/', expires: new Date(Date.now() + (86400 * 1000)), secure: true, sameSite: 'strict' });
                };
            });
        };
    });

    return (
        <>
            <Navbar loggedIn={true} data={{
                displayDropdown: false,
                fieldData: [
                    { name: "Home", href: "/" },
                    { name: "About", href: "/about" },
                    { name: "Contact Us", href: "/contact" },
                ]
            }} />
            <div className="r-form bg-dark">
                <h1 className="text-light">Login</h1>
                <LoginForm />
            </div>
            <Footer />
        </>
    );
};

export default Login;