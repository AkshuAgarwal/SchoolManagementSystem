import React, { useState, useEffect } from "react";
import axios from "axios";

import Navbar from "../../components/navbar";
import Loading from "../../components/loading";
import Footer from "../../components/footer";
import { BASE_AUTH } from "../../constants";
import { getDashboardType } from "../../utils";

function About() {
    const [loggedIn, setLoggedIn] = useState(false);
    const [userData, setUserData] = useState({});

    useEffect(() => {
        const loader = document.getElementById('r-loading-comp');
        const content = document.getElementById('r-about-content');

        axios.get(
            BASE_AUTH + 'authorize/'
        ).then(response => {
            if (response.status === 200) {
                setUserData(response.data.data);
                setLoggedIn(true);
                try {
                    loader.remove();
                } catch (error) { }
                content.classList.remove('r-content-hide');
            };
        }).catch(e => {
            try {
                loader.remove();
            } catch (error) { }
            content.classList.remove('r-content-hide');
        })
    }, []);

    return (
        <>
            <Navbar loggedIn={loggedIn} data={{
                displayDropdown: true,
                userData: userData,
                fieldData: [
                    { name: "Home", href: "/" },
                    { name: "Dashboard", href: getDashboardType(userData.user_type) },
                    { name: "About", href: "/about" },
                    { name: "Contact Us", href: "/contact" },
                ],
                dropdownFieldData: [
                    { name: "Profile", href: "/profile" },
                    { name: "Logout", href: "/logout" },
                ],
            }} />
            <Loading />

            <div id="r-about-content" className="r-content-hide"></div>

            <Footer />
        </>
    );
};

export default About;