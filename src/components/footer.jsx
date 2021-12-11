import React from 'react';
import { MDBFooter, MDBContainer, MDBRow, MDBCol } from 'mdb-react-ui-kit';

import { SCHOOL_FOOTER_TEXT, SCHOOL_FOOTER_LINKS, SITE_URL_SHORT } from "../constants.js"

function Footer() {
    var links = [];
    for (const [index, link] of SCHOOL_FOOTER_LINKS.entries()) {
        links.push(
            <li key={index}>
                <a key={index} href={link.href} className='text-light'>
                    {link.name}
                </a>
            </li>
        );
    };

    return (
        <MDBFooter className='text-center text-lg-left bg-dark r-footer'>
            <MDBContainer className='p-4'>
                <MDBRow className="r-footer-row">
                    <MDBCol lg='6' md='12' className='mb-4 mb-md-0'>
                        <h5 className='text-uppercase text-light'>About Us</h5>

                        <p className='text-light'>
                            {SCHOOL_FOOTER_TEXT}
                        </p>
                    </MDBCol>

                    <MDBCol lg='3' md='6' className='mb-4 mb-md-0'>
                        <h5 className='text-uppercase text-light'>Links</h5>

                        <ul className='list-unstyled mb-0'>
                            {links}
                        </ul>
                    </MDBCol>
                </MDBRow>
            </MDBContainer>

            <div className='text-center p-3 text-light' style={{ backgroundColor: 'rgba(255, 255, 255, 0.1)' }}>
                &copy; {new Date().getFullYear()}{' '}
                <a className='text-light' href='/'>
                    {SITE_URL_SHORT}
                </a>
            </div>
        </MDBFooter>
    );
};

export default Footer;
