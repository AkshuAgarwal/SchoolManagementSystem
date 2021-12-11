import axios from 'axios';
import Cookies from 'universal-cookie';
import { BASE_AUTH } from './constants';

const cookie = new Cookies();

export const getDashboardType = userType => {
    switch (userType) {
        case 's':
            return '/student/dashboard';
        case 't':
            return '/teacher/dashboard';
        case 'p':
            return '/parent/dashboard';
        case 'm':
            return '/manager/dashboard';
        case 'a':
            return '/admin/dashboard';
    }
};

export const ManageRouteEntry = (routeName, setLoggedIn, setUserData) => {
    const loader = document.getElementById('r-loading-comp');
    const content = document.getElementById(`r-${routeName}-content`);

    const isAuth = cookie.get('__li');
    const userData = cookie.get('__ud');

    if (isAuth === 't' && userData) {
        setUserData(userData);
        setLoggedIn(true);
        try {
            loader.remove();
        } catch (error) { }
        content.classList.remove('r-content-hide');
    } else if (isAuth === 'f') {
        try {
            loader.remove();
        } catch (error) { }
        content.classList.remove('r-content-hide');
    } else {
        axios.get(
            BASE_AUTH + 'authorize/'
        ).then(response => {
            if (response.status === 200) {
                cookie.set('__li', 't', { path : '/', expires : new Date(Date.now() + (86400 * 1000)), secure : true, sameSite : 'strict' });
                cookie.set('__ud', response.data.data, { path : '/', expires : new Date(Date.now() + (86400 * 1000)), secure : true, sameSite : 'strict' });
                setUserData(response.data.data);
                setLoggedIn(true);
                try {
                    loader.remove();
                } catch (error) { }
                content.classList.remove('r-content-hide');
            }
        }).catch(e => {
            if (e.response.status === 401) {
                cookie.set('__li', 'f', { path : '/', expires : new Date(Date.now() + (86400 * 1000)), secure : true, sameSite : 'strict' });
            }
            try {
                loader.remove();
            } catch (error) { }
            content.classList.remove('r-content-hide');
        });
    }
};
