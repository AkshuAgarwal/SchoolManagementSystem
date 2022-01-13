import { Container } from '@mui/material';
import { useContext } from 'react';
import { AuthContext } from '../../utils/js/context';

export default function Dashboars() {
    const authContext = useContext(AuthContext);
    console.log(authContext.userData);
    return <Container></Container>;
}
