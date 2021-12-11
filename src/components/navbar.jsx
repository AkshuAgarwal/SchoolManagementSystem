import React from "react";
import {
    Navbar as NavbarBS,
    Container as ContainerBS,
    Nav as NavBS,
    NavDropdown as NavDropdownBS
} from "react-bootstrap";

import { SCHOOL_NAME } from "../constants";

/*
data = {
    displayDropdown: true,
    userData: {
        username: "A"
    },
    fieldData: [
        {
            name: "field",
            href: "/"
        },
        {
            name: "field",
            href: "/"
        },
    ],
    dropdownFieldData: [
        {
            name: "dpfield",
            href: "/ok"
        }
    ]
}
*/

function Navbar({ loggedIn = false, data = { displayDropdown: false } }) {
    var fields = [];
    if (data.fieldData) {
        for (const [index, field] of data.fieldData.entries()) {
            fields.push(
                <NavBS.Link key={index} href={field.href}>{field.name}</NavBS.Link>
            );
        }
    }

    if (data.displayDropdown) {
        var dropdownFields = [];
        if (data.dropdownFieldData) {
            for (const [index, field] of data.dropdownFieldData.entries()) {
                dropdownFields.push(
                    <NavDropdownBS.Item key={index} href={field.href}>{field.name}</NavDropdownBS.Item>
                );
            }
        }
    }



    if (loggedIn) {
        return (
            <NavbarBS bg="dark" variant="dark" expand="md" sticky="top">
                <ContainerBS>
                    <NavbarBS.Brand href="/">{SCHOOL_NAME}</NavbarBS.Brand>
                    <NavbarBS.Toggle aria-controls="basic-navbar-nav" />
                    <NavbarBS.Collapse id="basic-navbar-nav">
                        <NavBS className="ms-auto">
                            {fields}
                            {
                                data.displayDropdown ? (
                                    <NavDropdownBS title="More" id="basic-nav-dropdown">
                                        <NavDropdownBS.Item disabled>Hi, {data.userData.username}!</NavDropdownBS.Item>
                                        <NavDropdownBS.Divider />
                                        {dropdownFields}
                                    </NavDropdownBS>
                                ) : (null)
                            }
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
                            <NavBS.Link href="/about">About</NavBS.Link>
                            <NavBS.Link href="/contact">Contact Us</NavBS.Link>
                            <NavBS.Link href="/login">Login</NavBS.Link>
                        </NavBS>
                    </NavbarBS.Collapse>
                </ContainerBS>
            </NavbarBS>
        );
    }
}

export default Navbar;
