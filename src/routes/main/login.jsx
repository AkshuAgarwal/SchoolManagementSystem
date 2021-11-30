import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Form, Button, FloatingLabel, Alert } from 'react-bootstrap';

import Footer from '../../components/footer.jsx';
import Navbar from '../../components/navbar.jsx';
import { BASE_AUTH } from '../../constants.js';

axios.defaults.withCredentials = true;

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
    const usernameOrEmailRef = React.useRef();
    const passwordRef = React.useRef();

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
                redirectToDashboard(response.data.user_type);
            };
        }).catch(e => {
            if (e.response.status === 404) {
                setShowAlert(true);
            }
        });
    };

    return (
        <Form notValidated validated={validated} onSubmit={handleSubmit}>
            {showAlert ? (<Alert variant="danger">Invalid Credentials</Alert>) : null}
            <Form.Group>
                <FloatingLabel label="Username or Email">
                    <Form.Control required ref={usernameOrEmailRef} type="text" placeholder="Username or Email" />
                </FloatingLabel>
            </Form.Group>
            <Form.Group>
                <FloatingLabel label="Password">
                    <Form.Control required ref={passwordRef} type="password" placeholder="Password" />
                </FloatingLabel>
            </Form.Group>
            <Form.Group>
                <Button variant="light" type="submit">Submit</Button>
            </Form.Group>
        </Form>
    );
};

function Login() {
    useEffect(() => {
        axios.get(
            BASE_AUTH + 'authorize/',
        ).then(response => {
            if (response.status === 200) {
                redirectToDashboard(response.data.data.user_type);
            };
        });
    });

    return (
        <>
            <Navbar loggedIn={true} data={{
                displayDropdown: false,
                fieldData: [
                    {
                        name: "Home",
                        href: "/"
                    }
                ]
            }} />
            <div className="r-login-form bg-dark">
                <h1 className="text-light">Login</h1>
                <LoginForm />
            </div>
            <Footer />
        </>
    );
};

export default Login;