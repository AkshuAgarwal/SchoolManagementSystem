import axios from "axios";
import { useEffect } from "react";
import Cookies from "universal-cookie";

import { BASE_AUTH } from "../../constants";

axios.defaults.withCredentials = true;

const cookie = new Cookies();

function Logout() {
    useEffect(() => {
        axios.get(
            BASE_AUTH + "unauthorize/"
        ).then(response => {
            if (response.status === 205) {
                cookie.set("__li", "f", { path: "/", expires: new Date(Date.now() + (86400 * 1000)), secure: true, sameSite: "strict" });
                cookie.remove("__ud");
                return window.location.href = "/";
            }
        }).catch(e => {
            if (e.response.status === 401) {
                return window.history.go(-1);
            }
        });
    });

    return null;
}

export default Logout;
