import { useEffect, useContext } from 'react';

import { useRouter } from 'next/router';

import { AuthContext } from '../utils/js/context';

export default function Logout() {
    const router = useRouter();
    const authContext = useContext(AuthContext);

    useEffect(() => {
        authContext.logoutUser();
        router.push('/');
    }, []); // eslint-disable-line

    return null;
}
