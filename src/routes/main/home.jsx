import React, { useEffect, useState } from 'react';
import axios from 'axios';

import Navbar from "../../components/navbar"
import Footer from '../../components/footer';
import Loading from '../../components/loading';
import { BASE_AUTH } from '../../constants';

const getDashboardType = userType => {
    if (userType === 's') {
        return '/student/dashboard';
    } else if (userType === 't') {
        return '/teacher/dashboard';
    } else if (userType === 'p') {
        return '/parent/dashboard';
    } else if (userType === 'm') {
        return '/manager/dashboard';
    } else if (userType === 'a') {
        return '/admin/dashboard';
    };
}

function Home() {
    const [loggedIn, setLoggedIn] = useState(false);
    const [userData, setUserData] = useState({});

    useEffect(() => {
        const loader = document.getElementById('r-loading-comp');
        const content = document.getElementById('r-home-content');

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
                ],
                dropdownFieldData: [{ name: "Logout", href: "/logout" }]
            }} />
            <Loading />

            {/* Content Here */}
            <p id="r-home-content" className="r-content-hide">Test</p>

            <Footer />
        </>
    );
};

export default Home;