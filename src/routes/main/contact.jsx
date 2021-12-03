import axios from "axios";
import React, { useState, useEffect, useRef } from "react";
import { FloatingLabel, Form, Row, Col, Button, Alert } from "react-bootstrap";

import Navbar from "../../components/navbar";
import Loading from "../../components/loading";
import Footer from "../../components/footer";
import { BASE_AUTH, BASE_API } from "../../constants";
import { getDashboardType } from "../../utils";

axios.defaults.withCredentials = true;

const ContactForm = () => {
    const firstNameRef = useRef();
    const lastNameRef = useRef("");
    const emailRef = useRef();
    const messageRef = useRef();

    const [showSuccessAlert, setShowSuccessAlert] = useState(false);
    const [showErrorAlert, setShowErrorAlert] = useState(false);

    const handleSubmit = e => {
        e.preventDefault();

        axios.post(
            BASE_API + 'contact/',
            {
                first_name: firstNameRef.current.value,
                last_name: lastNameRef.current.value,
                email_id: emailRef.current.value,
                message: messageRef.current.value,
            }
        ).then(response => {
            if (response.status === 201) {
                setShowSuccessAlert(true);
            }
        }).catch(e => {
            setShowErrorAlert(true);
        })
    };

    return (
        <>
            {
                showSuccessAlert ? (
                    <Alert variant="success" onClose={() => setShowSuccessAlert(false)} dismissible>
                        <Alert.Heading>Thank you for getting in touch!</Alert.Heading>
                        <p>
                            We appreciate you contacting us. One of our staff will get back in touch with you soon! Have a great day!
                        </p>
                    </Alert>
                ) : (null)
            }
            {
                showErrorAlert ? (
                    <Alert variant="danger" onClose={() => setShowErrorAlert(false)} dismissible>Oops! Some Error Occured. Please try again later...</Alert>
                ) : (null)
            }
            <Form onSubmit={handleSubmit}>
                <Row>
                    <Form.Group as={Col}>
                        <FloatingLabel label="First Name *">
                            <Form.Control required ref={firstNameRef} type="text" placeholder="First Name" />
                        </FloatingLabel>
                    </Form.Group>
                    <Form.Group as={Col}>
                        <FloatingLabel label="Last Name">
                            <Form.Control ref={lastNameRef} type="text" placeholder="Last Name" />
                        </FloatingLabel>
                    </Form.Group>
                </Row>
                <Row>
                    <Form.Group as={Col}>
                        <FloatingLabel label="Email Address *">
                            <Form.Control required ref={emailRef} type="email" placeholder="Email Address" />
                        </FloatingLabel>
                    </Form.Group>
                </Row>
                <Row>
                    <Form.Group as={Col}>
                        <FloatingLabel label="Your Message *">
                            <Form.Control required ref={messageRef} as="textarea" style={{ height: "150px" }} placeholder="Leave your message here" />
                        </FloatingLabel>
                    </Form.Group>
                </Row>
                <Row>
                    <Form.Group as={Col}>
                        <Button varient="light" type="submit">Submit</Button>
                    </Form.Group>
                </Row>
            </Form>
        </>
    );
};

function Contact() {
    const [loggedIn, setLoggedIn] = useState(false);
    const [userData, setUserData] = useState({});

    useEffect(() => {
        const loader = document.getElementById('r-loading-comp');
        const content = document.getElementById('r-contact-content');

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
                    { name: "About", href: "/about" },
                    { name: "Contact Us", href: "/contact" },
                ],
                dropdownFieldData: [
                    { name: "Profile", href: "/profile" },
                    { name: "Logout", href: "/logout" },
                ],
            }} />
            <Loading />
            <div id="r-contact-content" className="r-content-hide r-form bg-dark">
                <h1 className="text-light">Contact Us</h1>
                <ContactForm />
            </div>
            <Footer />
        </>
    );
}

export default Contact;