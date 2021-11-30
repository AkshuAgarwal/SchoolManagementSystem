import React from "react";
import {
    Navbar as NavbarBS,
    Container as ContainerBS,
    Nav as NavBS,
    NavDropdown as NavDropdownBS
} from "react-bootstrap";

import { SCHOOL_NAME } from "../constants.js";

/*
data = {
    userData: {
        username: "A"
    },
    fieldData: [
        {
            fieldName: "field",
            fieldHref: "/"
        },
        {
            fieldName: "field",
            fieldHref: "/"
        },
    ],
    dropdownFieldData: [
        {
            fieldName: "dpfield",
            fieldHref: "/ok"
        }
    ]
}
*/

function Navbar({ loggedIn = false, data = {} }) {
    var fields = [];
    if (data.fieldData) {
        for (const field of data.fieldData) {
            fields.push(
                <NavBS.Link href={field.fieldHref}>{field.fieldName}</NavBS.Link>
            );
        };
    };

    var dropdownFields = [];
    if (data.dropdownFieldData) {
        for (const field of data.dropdownFieldData) {
            dropdownFields.push(
                <NavDropdownBS.Item href={field.fieldHref}>{field.fieldName}</NavDropdownBS.Item>
            );
        };
    };



    if (loggedIn) {
        return (
            <NavbarBS bg="dark" variant="dark" expand="md" sticky="top">
                <ContainerBS>
                    <NavbarBS.Brand href="/">{SCHOOL_NAME}</NavbarBS.Brand>
                    <NavbarBS.Toggle aria-controls="basic-navbar-nav" />
                    <NavbarBS.Collapse id="basic-navbar-nav">
                        <NavBS className="ms-auto">
                            {fields}
                            <NavDropdownBS title="More" id="basic-nav-dropdown">
                                <NavDropdownBS.Item disabled>Hi, {data.userData.username}!</NavDropdownBS.Item>
                                <NavDropdownBS.Divider />
                                {dropdownFields}
                            </NavDropdownBS>
                        </NavBS>
                    </NavbarBS.Collapse>
                </ContainerBS>
            </NavbarBS>
        );
    } else {
        return (
            <NavbarBS bg="dark" variant="dark" expand="md" sticky="top">
                <ContainerBS>
                    <NavbarBS.Brand href="/">{SCHOOL_NAME}</NavbarBS.Brand>
                    <NavbarBS.Toggle aria-controls="basic-navbar-nav" />
                    <NavbarBS.Collapse id="basic-navbar-nav">
                        <NavBS className="ms-auto">
                            <NavBS.Link href="/">Home</NavBS.Link>
                            <NavBS.Link href="/login">Login</NavBS.Link>
                        </NavBS>
                    </NavbarBS.Collapse>
                </ContainerBS>
            </NavbarBS>
        );
    };
};

export default Navbar;
