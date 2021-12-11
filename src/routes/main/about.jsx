import React, { useState, useEffect } from 'react';

import Navbar from '../../components/navbar';
import Loading from '../../components/loading';
import Footer from '../../components/footer';
import { getDashboardType, ManageRouteEntry } from '../../utils';

function About() {
    const [ loggedIn, setLoggedIn ] = useState(false);
    const [ userData, setUserData ] = useState({});

    useEffect(() => {
        ManageRouteEntry('about', setLoggedIn, setUserData);
    }, []);

    return (
        <>
            <Navbar loggedIn={loggedIn} data={{
                displayDropdown : true,
                userData        : userData,
                fieldData       : [
                    { name : 'Home', href : '/' },
                    { name : 'Dashboard', href : getDashboardType(userData.user_type) },
                    { name : 'About', href : '/about' },
                    { name : 'Contact Us', href : '/contact' },
                ],
                dropdownFieldData: [
                    { name : 'Profile', href : '/profile' },
                    { name : 'Logout', href : '/logout' },
                ],
            }} />
            <Loading />

            <div id="r-about-content" className="r-content-hide"></div>

            <Footer />
        </>
    );
}

export default About;
