import { useContext, useEffect } from 'react';

import { DoubleArrow as DoubleArrowIcon } from '@mui/icons-material';
import { IconButton, List, ListItem, ListItemAvatar, ListItemButton, ListItemIcon, ListItemText, ListSubheader, SwipeableDrawer, useMediaQuery } from '@mui/material';

import { SidebarContext } from '../utils/js/context';

export default function Sidebar({ subheader, items=[] }) {
    const sidebarContext = useContext(SidebarContext);

    const upSm = useMediaQuery(theme => theme.breakpoints.up('sm'), { noSsr : true });

    useEffect(() => {
        if (!sidebarContext.selected) {
            items.map((value, index) => {
                if (value.defaultSelected) {
                    sidebarContext.setSelected(index);
                }
            });
        }
    }, []); // eslint-disable-line

    return (
        <SwipeableDrawer
            variant={upSm ? 'permanent' : 'temporary'}
            open={sidebarContext.open}
            onOpen={() => { sidebarContext.setOpen(true); }}
            onClose={() => { sidebarContext.setOpen(false); }}
            sx={{
                position               : upSm ? 'relative' : 'fixed',
                left                   : 0,
                width                  : { xs : '43vw', sm : '28vw', md : '20vw', lg : '15vw', xl : '10vw' },
                zIndex                 : upSm ? 1000 : 1200,
                [`& .MuiDrawer-paper`] : {
                    position        : upSm ? 'relative' : 'fixed',
                    left            : 0,
                    width           : { xs : '43vw', sm : '28vw', md : '20vw', lg : '15vw', xl : '10vw' },
                    backgroundColor : 'primary.main',
                    boxShadow       : '1px 2px 6px -1px rgb(0 0 0 / 20%)'
                }
            }}
        >
            <List
                aria-labelledby="sidebar-list-subheader-text"
                subheader={
                    subheader ? (
                        <ListSubheader component="div" id="sidebar-list-subheader-text">
                            {subheader}
                        </ListSubheader>
                    ) : null
                }
                sx={{
                    [`& .MuiListItemButton-root.Mui-selected`]: {
                        backgroundColor : 'secondary.main',
                        color           : 'secondary.contrastText',
                        '&:hover'       : {
                            backgroundColor: 'secondary.dark'
                        }
                    }
                }}
            >
                {
                    !upSm ? (
                        <ListItem dense divider sx={{ marginBottom : '10px' }}>
                            <IconButton onClick={() => { sidebarContext.setOpen(false); }}>
                                <DoubleArrowIcon sx={{ transform : 'scale(-1, 1)' }} />
                            </IconButton>
                        </ListItem>
                    ) : null
                }
                {
                    items.map((value, index) => (
                        <ListItem
                            key={index}
                            dense
                        >
                            <ListItemButton
                                key={index}
                                selected={sidebarContext.selected === index}
                                onClick={() => {
                                    value.onClick();
                                    sidebarContext.setSelected(index);
                                }}
                            >
                                { value.icon ? <ListItemIcon key={index}>{value.icon}</ListItemIcon> : null }
                                { value.avatar ? <ListItemAvatar key={index}>{value.avatar}</ListItemAvatar> : null }
                                <ListItemText key={index}>{value.text}</ListItemText>
                            </ListItemButton>
                        </ListItem>
                    ))
                }
            </List>
        </SwipeableDrawer>
    );
}
