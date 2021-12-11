import React from "react";
import { MDBSpinner } from "mdb-react-ui-kit";

import { SCHOOL_LOGO } from "../constants";

const messages = [
    "Fetching your Data...",
    "Hold on...",
    "Wait a minute...",
    "Loading..."
];

function Loading() {
    return (
        <div id="r-loading-comp" className="d-flex flex-column justify-content-center align-items-center r-loading">
            <img className="r-loading-img" src={SCHOOL_LOGO} alt="Logo" />
            <p className="r-loading-text">
                {messages[Math.floor(Math.random() * messages.length)]}
            </p>
            <MDBSpinner className="r-spinner">
                <span className="visually-hidden">Loading...</span>
            </MDBSpinner>
        </div>
    );
}

export default Loading;