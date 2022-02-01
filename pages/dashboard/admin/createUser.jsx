import { useState, useRef } from 'react';

import Image from 'next/image';

import moment from 'moment';

import { AdapterMoment, DatePicker, LoadingButton, LocalizationProvider } from '@mui/lab';
import { AccountCircleOutlined, CheckCircleOutlined, InfoOutlined, Visibility, VisibilityOff } from '@mui/icons-material';
import { Alert, Autocomplete, Avatar, Box, Button, Container, FormControl, FormHelperText, IconButton, Input, InputAdornment, InputLabel, MenuItem, OutlinedInput, Select, Snackbar, Step, StepLabel, Stepper, TextField, Typography } from '@mui/material';

import axios from '../../../utils/js/axios';
import { countries } from '../../../utils/js/countries.js';

const steps = [{ label : 'Account Info', icon : AccountCircleOutlined }, { label : 'Personal Details', icon : InfoOutlined }];

const AccountInfoStep = ({ state, display, handleStepperNext }) => {
    const usernameRef = useRef('');
    const emailRef = useRef('');
    const passwordRef = useRef('');
    const confirmPasswordRef = useRef('');

    const [ showPassword, setShowPassword ] = useState(false);

    const [ invalidUsernameError, setInvalidUsernameError ] = useState(false);
    const [ uniqueUsernameError, setUniqueUsernameError ] = useState(false);

    const [ invalidEmailError, setInvalidEmailError ] = useState(false);
    const [ uniqueEmailError, setUniqueEmailError ] = useState(false);

    const [ passwordError, setPasswordError ] = useState(false);
    const [ passwordErrorMessages, setPasswordErrorMessages ] = useState([]);

    const [ confirmPasswordError, setConfirmPasswordError ] = useState(false);

    const checkUniqueUsernameValidation = () => {
        setUniqueUsernameError(false);
        if (usernameRef.current.value !== '') {
            axios.get(
                'api/user/', { params : { username : usernameRef.current.value } }
            ).then(response => {
                if (response.status === 200) {
                    setUniqueUsernameError(true);
                }
            }).catch(e => {
                if (e.response.status === 404) {
                    setUniqueUsernameError(false);
                }
            });
        }
    };

    const checkUsernameStringValidation = () => {
        setInvalidUsernameError(false);
        if (usernameRef.current.value !== '') {
            usernameRef.current.value.split('').map(val => {
                let cc = val.charCodeAt();
                if (!(
                    (48 <= cc && cc <= 57) || // digits
                    (65 <= cc && cc <= 90) || // uppercase alphabets
                    (cc === 95) || // underscore (_)
                    (97 <= cc && cc <= 122) // lowercase alphabets
                )) {
                    setInvalidUsernameError(true);
                }
            });
        }
    };

    const checkUniqueEmailValidation = () => {
        setUniqueEmailError(false);
        if (emailRef.current.value !== '') {
            axios.get(
                'api/user/', { params : { email_id : emailRef.current.value } }
            ).then(response => {
                if (response.status === 200) {
                    setUniqueEmailError(true);
                }
            }).catch(e => {
                if (e.response.status === 404) {
                    setUniqueEmailError(false);
                }
            });
        }
    };

    const checkEmailStringValidation = () => {
        setInvalidEmailError(false);
        if (emailRef.current.value !== '') {
            if (!String(emailRef.current.value)
                .toLowerCase()
                .match(
                    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                )
            ) {
                setInvalidEmailError(true);
            } else {
                setInvalidEmailError(false);
            }
        }
    };

    const checkPasswordValidation = () => {
        if (passwordRef.current.value === '') {
            setPasswordErrorMessages([]);
            setPasswordError(false);
        } else {
            axios.post(
                'auth/password/validate/', { password : passwordRef.current.value }
            ).then(response => {
                if (response.status === 200) {
                    setPasswordErrorMessages([]);
                    setPasswordError(false);
                }
            }).catch(e => {
                if (e.response.status === 400) {
                    setPasswordErrorMessages(e.response.data.error.errors);
                    setPasswordError(true);
                }
            });
        }
    };

    const checkPasswordsEquality = () => {
        if (confirmPasswordRef.current.value === '') {
            setConfirmPasswordError(false);
        } else {
            if (passwordRef.current.value !== confirmPasswordRef.current.value) {
                setConfirmPasswordError(true);
            } else {
                setConfirmPasswordError(false);
            }
        }
    };

    const handleSubmit = e => {
        e.preventDefault();

        state[1]({
            ...state[0],
            username : usernameRef.current.value,
            email    : emailRef.current.value,
            password : passwordRef.current.value
        });

        handleStepperNext();
    };

    return (
        <div style={{ display : display ? 'block' : 'none' }}>
            <form onSubmit={handleSubmit}>
                <FormControl margin="normal" sx={{ width : '100%' }} required>
                    <InputLabel htmlFor="__dashboard_admin__form_createuser_step1__username">Username</InputLabel>
                    <OutlinedInput
                        id="__dashboard_admin__form_createuser_step1__username"
                        aria-describedby="__dashboard_admin__form_createuser_step1__username_helper"
                        type="text"
                        inputRef={usernameRef}
                        inputProps={{ pattern : '[A-Za-z0-9_]+', title : 'Username can only contain alphabets, digits and underscore (_). Eg., John_123.' }}
                        label="Username"
                        error={invalidUsernameError || uniqueUsernameError}
                        onChange={() => {
                            checkUniqueUsernameValidation();
                            checkUsernameStringValidation();
                        }}
                    />
                    <FormHelperText id="__dashboard_admin__form_createuser_step1__username_helper" error={invalidUsernameError || uniqueUsernameError}>
                        {invalidUsernameError ? 'Username can only contain alphabets, digits and underscore (_). Eg., John_123.' : null}
                        {uniqueUsernameError ? 'This Username is already taken, please try another.' : null}
                    </FormHelperText>
                </FormControl>
                <FormControl margin="normal" sx={{ width : '100%' }} required>
                    <InputLabel htmlFor="__dashboard_admin__form_createuser_step1__email">Email ID</InputLabel>
                    <OutlinedInput
                        id="__dashboard_admin__form_createuser_step1__email"
                        aria-describedby="__dashboard_admin__form_createuser_step1__email_helper"
                        type="email"
                        inputRef={emailRef}
                        label="Email ID"
                        error={invalidEmailError || uniqueEmailError}
                        onChange={() => {
                            checkUniqueEmailValidation();
                            checkEmailStringValidation();
                        }}
                    />
                    <FormHelperText id="__dashboard_admin__form_createuser_step1__email_helper" error={invalidEmailError || uniqueEmailError}>
                        {invalidEmailError ? 'Email ID is not valid.' : null}
                        {uniqueEmailError ? 'This Email ID is already in use, please try another.' : null}
                    </FormHelperText>
                </FormControl>
                <FormControl margin="normal" sx={{ width : '100%' }} required>
                    <InputLabel htmlFor="__dashboard_admin__form_createuser_step1__password" error={passwordError}>New Password</InputLabel>
                    <OutlinedInput
                        id="__dashboard_admin__form_createuser_step1__password"
                        aria-describedby="__dashboard_admin__form_createuser_step1__password_helper"
                        type={showPassword ? 'text' : 'password'}
                        inputRef={passwordRef}
                        label="New Password"
                        error={passwordError}
                        onChange={() => {
                            checkPasswordValidation();
                            checkPasswordsEquality();
                        }}
                        endAdornment={
                            <InputAdornment position="end">
                                <IconButton onClick={() => { setShowPassword(!showPassword); }} edge="end">
                                    {showPassword ? <Visibility /> : <VisibilityOff />}
                                </IconButton>
                            </InputAdornment>
                        }
                    />
                    <FormHelperText id="__dashboard_admin__form_createuser_step1__password_helper" error={passwordError}>{passwordErrorMessages.join(' ')}</FormHelperText>
                </FormControl>
                <FormControl margin="normal" sx={{ width : '100%' }} required>
                    <InputLabel htmlFor="__dashboard_admin__form_createuser_step1__reenterpassword" error={confirmPasswordError}>Re-Enter New Password</InputLabel>
                    <OutlinedInput
                        id="__dashboard_admin__form_createuser_step1__reenterpassword"
                        aria-describedby="__dashboard_admin__form_createuser_step1__reenterpassword_helper"
                        type={showPassword ? 'text' : 'password'}
                        inputRef={confirmPasswordRef}
                        label="Re-Enter New Password"
                        error={confirmPasswordError}
                        onChange={checkPasswordsEquality}
                    />
                    <FormHelperText id="__dashboard_admin__form_createuser_step1__reenterpassword_helper" error={confirmPasswordError}>{confirmPasswordError ? 'Passwords does not Match' : ' '}</FormHelperText>
                </FormControl>
                <Container style={{ display : 'flex', flexDirection : 'row', justifyContent : 'space-between', marginTop : '20px' }}>
                    <Button disabled>Back</Button>
                    <Button
                        variant="contained"
                        type="submit"
                        disabled={!([ invalidUsernameError, uniqueUsernameError, invalidEmailError, uniqueEmailError, passwordError, confirmPasswordError ].every(v => v === false))}
                    >
                        Next
                    </Button>
                </Container>
            </form>
        </div>
    );
};

const PersonalInfoStep = ({ state, display, handleStepperBack, handleStepperNext }) => {
    const [ loading, setLoading ] = useState(false);

    const firstNameRef = useRef();
    const lastNameRef = useRef();
    const userTypeState = useState('');
    const dateOfBirthState = useState(null);
    const genderState = useState('');
    const addressRef = useRef('');

    const [ countryCode, setCountryCode ] = useState('1');
    const [ contactNoWithoutCountryCode, setContactNoWithoutCountryCode ] = useState(null);

    const [ avatarImage, setAvatarImage ] = useState(null);

    const getURLFromFile = file => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });

    const handleSubmit = async e => {
        e.preventDefault();
        setLoading(true);

        state[1]({
            ...state[0],
            firstName   : firstNameRef.current.value,
            lastName    : lastNameRef.current.value,
            userType    : userTypeState[0],
            dateOfBirth : moment(dateOfBirthState[0]).format('YYYY-MM-DD'),
            gender      : genderState[0],
            contactNo   : `+${countryCode}${contactNoWithoutCountryCode}`,
            address     : addressRef.current.value,
            avatar      : avatarImage ? await getURLFromFile(avatarImage) : null,
        });


        let data = {
            username      : state[0].username,
            email_id      : state[0].email,
            password      : state[0].password,
            first_name    : state[0].firstName,
            last_name     : state[0].lastName ? state[0].lastName: null,
            user_type     : state[0].userType,
            date_of_birth : state[0].dateOfBirth,
            gender        : state[0].gender,
            contact_no    : state[0].contactNo,
            address       : state[0].address ? state[0].address : null,
            avatar        : state[0].avatar,
        };

        axios.post('admin/user/', data).then(response => {
            if (response.status === 201) {
                handleStepperNext();
                state[0].success[1](true);
                setLoading(false);
            }
        }).catch(e => {
            if (e.response.status === 400) {
                setLoading(false);
            }
        });
    };

    return (
        <div style={{ display : display ? 'block' : 'none' }}>
            <form onSubmit={handleSubmit}>
                <Container sx={{ display : 'flex', flexDirection : 'row', gap : '20px' }} disableGutters>
                    <FormControl margin="normal" sx={{ width : '100%' }} required>
                        <InputLabel htmlFor="__dashboard_admin__form_createuser_step2__firstname">First Name</InputLabel>
                        <OutlinedInput
                            id="__dashboard_admin__form_createuser_step2__firstname"
                            type="text"
                            inputRef={firstNameRef}
                            label="First Name"
                        />
                    </FormControl>
                    <FormControl margin="normal" sx={{ width : '100%' }}>
                        <InputLabel htmlFor="__dashboard_admin__form_createuser_step2__lastname">Last Name</InputLabel>
                        <OutlinedInput
                            id="__dashboard_admin__form_createuser_step2__lastname"
                            type="text"
                            inputRef={lastNameRef}
                            label="Last Name"
                        />
                    </FormControl>
                </Container>
                <FormControl margin="normal" sx={{ width : '100%' }} required>
                    <LocalizationProvider dateAdapter={AdapterMoment}>
                        <DatePicker
                            label="Date of Birth *"
                            value={dateOfBirthState[0]}
                            onChange={newValue => { dateOfBirthState[1](newValue); }}
                            renderInput={params => <TextField {...params} />}
                        />
                    </LocalizationProvider>
                </FormControl>
                <Container sx={{ display : 'flex', flexDirection : 'row', gap : '20px' }} disableGutters>
                    <FormControl margin="normal" sx={{ width : '100%' }} required>
                        <InputLabel htmlFor="__dashboard_admin__form_createuser_step2__usertype">User Type</InputLabel>
                        <Select
                            labelId="__dashboard_admin__form_createuser_step2__usertype"
                            value={userTypeState[0]}
                            label="User Type"
                            onChange={event => { userTypeState[1](event.target.value); }}
                        >
                            <MenuItem value="s">Student</MenuItem>
                            <MenuItem value="t">Teacher</MenuItem>
                            <MenuItem value="p">Parent</MenuItem>
                            <MenuItem value="m">Management</MenuItem>
                        </Select>
                    </FormControl>
                    <FormControl margin="normal" sx={{ width : '100%' }} required>
                        <InputLabel htmlFor="__dashboard_admin__form_createuser_step2__gender">Gender</InputLabel>
                        <Select
                            labelId="__dashboard_admin__form_createuser_step2__gender"
                            value={genderState[0]}
                            label="Gender"
                            onChange={event => { genderState[1](event.target.value); }}
                        >
                            <MenuItem value="m">Male</MenuItem>
                            <MenuItem value="f">Female</MenuItem>
                            <MenuItem value="o">Other</MenuItem>
                        </Select>
                    </FormControl>
                </Container>
                <Container sx={{ display : 'flex', flexDirection : 'row', gap : '5px' }} disableGutters>
                    <FormControl margin="normal" sx={{ width : '45%' }} required>
                        <Autocomplete
                            autoHighlight
                            options={countries}
                            getOptionLabel={option => option ? `+${option}` : ''}
                            isOptionEqualToValue={(option, value) => option.code === value?.toString()}
                            value={countryCode}
                            onChange={(event, newValue) => setCountryCode(newValue ? newValue.code : null)}
                            renderOption={(props, option) => (
                                <Box {...props} component="div" key={option.abbr}>
                                    <Image
                                        width={15}
                                        height={10}
                                        src={`https://flagcdn.com/${option.abbr.toLowerCase()}.svg`}
                                        srcSet={`https://flagcdn.com/${option.abbr.toLowerCase()}.svg 2x`}
                                        alt=""
                                    />
                                    <Typography variant="subtitle1" sx={{ marginLeft : '10px' }}>
                                            +{option.code}
                                    </Typography>
                                </Box>
                            )}
                            renderInput={params => (
                                <TextField
                                    required
                                    {...params}
                                    label="Code"
                                    inputProps={{
                                        ...params.inputProps,
                                        autoComplete: 'new-password',
                                    }}
                                />
                            )}
                        />
                    </FormControl>
                    <FormControl margin="normal" sx={{ width : '100%' }} required>
                        <InputLabel htmlFor="__dashboard_admin__form_createuser_step2__contactno">Contact No.</InputLabel>
                        <OutlinedInput
                            id="__dashboard_admin__form_createuser_step2__contactno"
                            label="Contact No."
                            type="tel"
                            onChange={event => setContactNoWithoutCountryCode(event.target.value)}
                            inputProps={{ minLength : 10, maxLength : 10 }}
                            sx={{ paddingLeft : 0 }}
                        />
                    </FormControl>
                </Container>
                <FormControl margin="normal" sx={{ width : '100%' }}>
                    <InputLabel htmlFor="__dashboard_admin__form_createuser_step2__address">Address</InputLabel>
                    <OutlinedInput
                        id="__dashboard_admin__form_createuser_step2__address"
                        inputRef={addressRef}
                        label="Address"
                        multiline
                        rows={3}
                        inputProps={{ maxLength : 1000 }}
                    />
                </FormControl>
                <Container sx={{ display : 'flex', flexDirection : 'row', gap : '20px' }} disableGutters>
                    <FormControl margin="normal" sx={{ width : '100%' }}>
                        <Container sx={{ display : 'flex', flexDirection : 'row' }} disableGutters>
                            <Container sx={{ display : 'flex', flexDirection : 'column', gap : '10px', width : '80%' }} disableGutters>
                                <Input
                                    id="__dashboard_admin__form_createuser_step2__avatar_input"
                                    accept="image/*"
                                    type="file"
                                    sx={{ display : 'none' }}
                                    onChange={event => {
                                        let file = event.target.files[0];
                                        if (file) {
                                            file.__blobUrl = URL.createObjectURL(file);
                                            setAvatarImage(file);
                                        }
                                    }}
                                />
                                <Button onClick={() => { document?.getElementById('__dashboard_admin__form_createuser_step2__avatar_input').click(); }}>
                                    {avatarImage ? 'Change Avatar' : 'Upload Avatar'}
                                </Button>
                                {avatarImage ? (
                                    <Button onClick={() => setAvatarImage(null)}>
                                Remove Avatar
                                    </Button>
                                ) : null}
                            </Container>
                            <Container sx={{ display : 'flex', flexDirection : 'row', justifyContent : 'space-evenly' }} disableGutters>
                                {avatarImage ? <Avatar id="__dashboard_admin__form_createuser_step2__avatar_preview" alt="Avatar" src={avatarImage.__blobUrl} sx={{ width : '100px', height : '100px' }} /> : null}
                            </Container>
                        </Container>
                    </FormControl>
                </Container>
                <Container style={{ display : 'flex', flexDirection : 'row', justifyContent : 'space-between', marginTop : '40px' }}>
                    <Button onClick={handleStepperBack}>Back</Button>
                    {/* <Button onClick={() => {  }}>Back</Button> */}
                    <LoadingButton
                        variant="contained"
                        type="submit"
                        loading={loading}
                    >
                        Submit
                    </LoadingButton>
                </Container>
            </form>
        </div>
    );
};

const SuccessStep = ({ handleStart }) => {
    return (
        <Container sx={{ display : 'flex', flexDirection : 'column', gap : '40px', alignItems : 'center' }}>
            <Alert severity="success" sx={{ width : '100%' }}>
                User Created Successfully
            </Alert>
            <Button onClick={handleStart}>Create Another</Button>
        </Container>
    );
};

export default function CreateUser() {
    const [ activeStep, setActiveStep ] = useState(1);

    const state = useState({
        username    : undefined,
        email       : undefined,
        password    : undefined,
        firstName   : undefined,
        lastName    : undefined,
        userType    : undefined,
        dateOfBirth : undefined,
        gender      : undefined,
        contactNo   : undefined,
        address     : undefined,
        avatar      : undefined,
        success     : useState(false),
    });

    const handleStart = () => {
        setActiveStep(1);
    };

    const handleStepperBack = () => {
        setActiveStep(activeStep - 1);
    };

    const handleStepperNext = () => {
        setActiveStep(activeStep + 1);
    };

    return (
        <Container sx={{ display : 'flex', flexDirection : 'column', justifyContent : 'center', alignItems : 'center', padding : '8vh 0' }}>
            <Box sx={{
                display         : 'flex',
                flexDirection   : 'column',
                alignItems      : 'center',
                justifyContent  : 'center',
                flexWrap        : 'wrap',
                width           : { xs : '100%', sm : '90%' },
                borderRadius    : '7.5px',
                padding         : '50px 30px',
                backgroundColor : 'background.paper'
            }}>
                <Typography variant="h5">Create User</Typography>
                <Container sx={{ marginTop : '30px', width : { xs : '100%', sm : '75%' } }} disableGutters>
                    <Stepper activeStep={activeStep} alternativeLabel>
                        {
                            steps.map((value, index) => {
                                return (
                                    <Step key={index} index={index}>
                                        <StepLabel StepIconComponent={
                                            activeStep > index + 1 ?
                                                () => { return <CheckCircleOutlined color="success" />; } :
                                                (activeStep === index + 1 ? () => { return <value.icon color="info" />; } : value.icon )
                                        }>
                                            {value.label}
                                        </StepLabel>
                                    </Step>
                                );
                            })
                        }
                    </Stepper>
                </Container>
                <Container sx={{ marginTop : '30px', maxWidth : { xs : '100%', sm : '95%', md : '70%', lg : '55%' } }}>
                    {
                        activeStep !== 3 ? (
                            <>
                                <AccountInfoStep display={activeStep === 1} state={state} handleStepperNext={handleStepperNext} />
                                <PersonalInfoStep display={activeStep === 2} state={state} handleStepperBack={handleStepperBack} handleStepperNext={handleStepperNext} />
                            </>
                        ) : <SuccessStep handleStart={handleStart} />
                    }
                </Container>
                <Snackbar open={state[0].success[0]} autoHideDuration={6000} onClose={() => { state[0].success[1](false); }}>
                    <Alert severity="success" onClose={() => { state[0].success[1](false); }} sx={{ width : '100%' }}>User Created Successfully</Alert>
                </Snackbar>
            </Box>
        </Container>
    );
}
