import React, { useState, useEffect } from 'react';

import Navbar from '../../components/navbar';
import Loading from '../../components/loading';
import Footer from '../../components/footer';
import { ManageRouteEntry } from '../../utils';

function Dashboard() {
    const [ loggedIn, setLoggedIn ] = useState(false);
    const [ userData, setUserData ] = useState({});

    useEffect(() => {
        ManageRouteEntry('student-dashboard', setLoggedIn, setUserData);
    }, []);

    return (
        <>
            <Navbar loggedIn={loggedIn} data={{
                displayDropdown : true,
                userData        : userData,
                fieldData       : [
                    { name : 'Home', href : '/' },
                    { name : 'About', href : '/about' },
                    { name : 'Contact Us', href : '/contact' },
                ],
                dropdownFieldData: [
                    {
                        name : 'Profile',
                        href : '/profile'
                    },
                    { name : 'Logout', href : '/logout' },
                ],
            }} />
            <Loading />
            <div id="r-student-dashboard-content" className="r-content-hide"></div>
            <Footer />
        </>
    );
}

export default Dashboard;
