import { useContext, useEffect } from 'react';

import { useRouter } from 'next/router';

import { DoubleArrow as DoubleArrowIcon } from '@mui/icons-material';
import { IconButton, List, ListItem, ListItemAvatar, ListItemButton, ListItemIcon, ListItemText, ListSubheader, SwipeableDrawer, useMediaQuery } from '@mui/material';

import { SidebarContext } from '../utils/js/context';

export default function Sidebar({ subheader, pages }) {
    const router = useRouter();
    const sidebarContext = useContext(SidebarContext);

    const upSm = useMediaQuery(theme => theme.breakpoints.up('sm'), { noSsr : true });

    useEffect(() => {
        sidebarContext.setSelected(router.query.page);
    }, [router.query.page]); // eslint-disable-line

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
                <ListItem dense>
                    <ListItemButton
                        selected={sidebarContext.selected === pages.defaultItem.id}
                        onClick={() => {
                            pages.defaultItem.onClick?.();
                            router.push({ pathname : router.pathname, query : { page : pages.defaultItem.id } }, undefined, { shallow : true });
                            // sidebarContext.setSelected(value.id);
                            sidebarContext.setOpen(false);
                        }}
                    >
                        { pages.defaultItem.icon ? <ListItemIcon>{pages.defaultItem.icon}</ListItemIcon> : null }
                        { pages.defaultItem.avatar ? <ListItemAvatar>{pages.defaultItem.avatar}</ListItemAvatar> : null }
                        <ListItemText>{pages.defaultItem.text}</ListItemText>
                    </ListItemButton>
                </ListItem>
                {
                    pages.items.map((value, index) => (
                        <ListItem key={index} dense>
                            <ListItemButton
                                key={index}
                                selected={sidebarContext.selected === value.id}
                                onClick={() => {
                                    value.onClick?.();
                                    router.push({ pathname : router.pathname, query : { page : value.id } }, undefined, { shallow : true });
                                    // sidebarContext.setSelected(value.id);
                                    sidebarContext.setOpen(false);
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
