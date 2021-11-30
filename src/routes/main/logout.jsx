import React, { useEffect } from "react";
import axios from "axios";

import { BASE_AUTH } from "../../constants";

axios.defaults.withCredentials = true;

function Logout() {
    useEffect(() => {
        axios.get(
            BASE_AUTH + 'unauthorize/'
        ).then(response => {
            if (response.status === 205) {
                return window.location.href = '/';
            };
        }).catch(e => {
            if (e.response.status === 401) {
                return window.history.go(-1);
            };
        });
    });

    return null;
}

export default Logout;
