import axios from 'axios';
import React from 'react';

import Navbar from '../components/navbar';
import { BASE_API } from '../constants.js';

axios.defaults.withCredentials = true;

const Form = ({ onSubmit }) => {
    const usernameOrEmailRef = React.useRef();
    const passwordRef = React.useRef();

    const validateEmail = email => {
        return String(email)
            .toLowerCase()
            .match(
                /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            );
    };

    const handleSubmit = e => {
        e.preventDefault();

        const usernameOrEmail = usernameOrEmailRef.current.value;
        const data = {};

        if (validateEmail(usernameOrEmail)) {
            data['email_id'] = usernameOrEmail
        } else {
            data['username'] = usernameOrEmail
        }

        data['password'] = passwordRef.current.value;
        onSubmit(data);
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="lf-g">
                <label className="lf-l">Username or Email</label>
                <input ref={usernameOrEmailRef} type="text" className="lf-e-inp" id="lf-e-inp-id" placeholder="Username or Email Address" />
            </div>
            <div className="lf-g">
                <label className="lf-l">Password</label>
                <input ref={passwordRef} type="password" className="lf-p-inp" id="lf-p-inp-id" placeholder="Password" />
            </div>
            <button type="submit" className="lf-btn-sb">Submit</button>
        </form>
    );
};

class Login extends React.Component {
    constructor(props) {
        super(props);

        this.onSubmit = data => {
            axios.post(
                BASE_API + 'api/authorize/',
                data
            ).then(response => {
                if (response.status === 200) {
                    const type = response.data.user_type;
                    if (type === 's') {
                        window.location.href = '/student/dashboard';
                    } else if (type === 't') {
                        window.location.href = '/teacher/dashboard';
                    } else if (type === 'p') {
                        window.location.href = '/parent/dashboard';
                    } else if (type === 'm') {
                        window.location.href = '/manager/dashboard';
                    } else if (type === 'a') {
                        window.location.href = '/admin/dashboard';
                    };
                }
            });
        };
    };

    componentDidMount() {
        axios.get(
            BASE_API + 'api/authorize/',
        ).then(response => {
            if (response.status === 200) {
                const type = response.data.data.user_type;
                if (type === 's') {
                    window.location.href = '/student/dashboard';
                } else if (type === 't') {
                    window.location.href = '/teacher/dashboard';
                } else if (type === 'p') {
                    window.location.href = '/parent/dashboard';
                } else if (type === 'm') {
                    window.location.href = '/manager/dashboard';
                } else if (type === 'a') {
                    window.location.href = '/admin/dashboard';
                };
            };
        });
    };

    render() {
        return (
            <div className="loginForm">
                <Navbar />
                <Form onSubmit={this.onSubmit} />
            </div>
        );
    };
};

export default Login;
