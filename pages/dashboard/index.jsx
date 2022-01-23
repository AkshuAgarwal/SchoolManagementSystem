import { useEffect, useContext } from 'react';
import { useRouter } from 'next/router';

import { AuthContext } from '../../utils/js/context';

export default function Dashboars() {
    const router = useRouter();
    const authContext = useContext(AuthContext);

    useEffect(() => {
        authContext.setLoading(true);
        if (!authContext.loggedIn) {
            router.replace('/login');
        } else {
            switch (authContext.userData.user_type) {
                case 's':
                    router.replace('/dashboard/student');
                    break;
                case 't':
                    router.replace('/dashboard/teacher');
                    break;
                case 'p':
                    router.replace('/dashboard/parent');
                    break;
                case 'm':
                    router.replace('/dashboard/management');
                    break;
                case 'a':
                    router.replace('/dashboard/admin');
                    break;
            }
        }
        authContext.setLoading(false);
    }, []); // eslint-disable-line

    return null;
}
