import React from "react";
import axios from "axios";

import { BASE_API } from '../constants';

axios.defaults.withCredentials = true;

class Logout extends React.Component {
    componentDidMount() {
        axios.get(
            BASE_API + 'api/authorize/',
        ).then(response => {
            if (response.status === 200) {
                axios.get(
                    BASE_API + 'api/unauthorize/'
                ).then(response => {
                    if (response.status === 205) {
                        return window.location.href = '/';
                    }
                })
            };
        }).catch(
            e => {
                if (e.response.status === 401) {
                    return window.history.go(-1);
                };
            }
        );
    };

    render() {
        return null;
    };
}

export default Logout;
