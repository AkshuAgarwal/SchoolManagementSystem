import { createTheme } from '@mui/material/styles';

const lightThemeOptions = {
    palette: {
        mode    : 'light',
        type    : 'light',
        primary : {
            main: '#105190',
        },
        secondary: {
            main: '#3a3b3f',
        },
        success: {
            main: '#4caf50',
        },
    },
};

const darkThemeOptions = {
    palette: {
        mode    : 'dark',
        type    : 'dark',
        primary : {
            main         : '#0a0a0a',
            light        : 'rgb(59, 59, 59)',
            dark         : '#de4949',
            contrastText : '#fff',
        },
        secondary: {
            main         : '#f92d2f',
            light        : '#f5494a',
            dark         : 'rgb(174, 31, 32)',
            contrastText : '#fff',
        },
        background: {
            default : '#2b2a2a',
            paper   : '#0a0a0a',
        },
        text: {
            primary   : '#fff',
            secondary : 'rgba(255, 255, 255, 0.7)',
            disabled  : 'rgba(255, 255, 255, 0.5)',
            hint      : 'rgba(255,16,16,0.5)',
        },
        error: {
            main         : '#f44336',
            light        : 'rgb(246, 104, 94)',
            dark         : 'rgb(170, 46, 37)',
            contrastText : '#fff',
        },
        warning: {
            main         : '#ff9800',
            light        : '#ffb74d',
            dark         : '#f57c00',
            contrastText : 'rgba(0, 0, 0, 0.87)',
        },
        info: {
            main         : '#2196f3',
            light        : '#64b5f6',
            dark         : '#1976d2',
            contrastText : '#fff',
        },
        success: {
            main         : '#4caf50',
            light        : '#81c784',
            dark         : '#388e3c',
            contrastText : 'rgba(0, 0, 0, 0.87)',
        },
        divider: 'rgba(255, 255, 255, 0.12)',
    },
};

export const lightTheme = createTheme(lightThemeOptions);
export const darkTheme = createTheme(darkThemeOptions);
