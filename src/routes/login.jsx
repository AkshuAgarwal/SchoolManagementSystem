import axios from 'axios';
import React from 'react';

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

    const handleSubmit = async e => {
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

function LoginForm() {
    const handleSubmit = data => {
        axios.post(
            'http://localhost:8000/api/authorize/',
            data,
            { 'headers': { 'Content-Type': 'application/json' } }
        ).then(response => {
            console.log(response.data);
        })
    };

    return (
        <div className="loginForm">
            <Form onSubmit={handleSubmit} />
        </div>
    );
};

export default LoginForm;
