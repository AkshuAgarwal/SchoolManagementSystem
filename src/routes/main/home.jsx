import React, { useEffect, useState } from 'react';

import Navbar from "../../components/navbar"
import Footer from '../../components/footer';
import Loading from '../../components/loading';
import { getDashboardType, ManageRouteEntry } from "../../utils";

function Home() {
    const [loggedIn, setLoggedIn] = useState(false);
    const [userData, setUserData] = useState({});

    useEffect(() => {
        ManageRouteEntry('home', setLoggedIn, setUserData);
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

            {/* Content Here */}
            <p id="r-home-content" className="r-content-hide">Test</p>

            <Footer />
        </>
    );
};

export default Home;